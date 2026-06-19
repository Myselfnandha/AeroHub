import { db } from './db';
import { supabase } from './supabase';

// Helper to get client device ID
export async function getDeviceId(): Promise<string> {
  const meta = await db.syncMeta.get('device_id');
  if (meta) return meta.value;

  // Generate unique UUID-like device id
  const newId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  await db.syncMeta.put({ key: 'device_id', value: newId });
  return newId;
}

// Get last successful sync timestamp
export async function getLastSyncTime(): Promise<number> {
  const meta = await db.syncMeta.get('last_sync_time');
  return meta ? parseInt(meta.value, 10) : 0;
}

// Update last sync time
export async function setLastSyncTime(timestamp: number) {
  await db.syncMeta.put({ key: 'last_sync_time', value: timestamp.toString() });
}

export interface SyncStatus {
  success: boolean;
  message: string;
  pushedNotes: number;
  pulledNotes: number;
}

export async function runSync(userId: string): Promise<SyncStatus> {
  try {
    const lastSync = await getLastSyncTime();
    const now = Date.now();

    console.log(`Starting Delta Sync: lastSync=${lastSync}, userId=${userId}`);

    // ==========================================
    // 1. PUSH FOLDERS
    // ==========================================
    const unsyncedFolders = await db.folders
      .where('updated_at')
      .above(lastSync)
      .toArray();

    if (unsyncedFolders.length > 0) {
      const foldersToPush = unsyncedFolders.map(f => ({
        id: f.id,
        user_id: userId,
        name: f.name,
        parent_folder_id: f.parent_folder_id,
        is_deleted: f.is_deleted === 1,
        updated_at: new Date(f.updated_at).toISOString(),
      }));

      const { error } = await supabase.from('folders').upsert(foldersToPush);
      if (error) throw new Error(`Push folders failed: ${error.message}`);
    }

    // ==========================================
    // 2. PUSH NOTES
    // ==========================================
    const unsyncedNotes = await db.notes
      .where('updated_at')
      .above(lastSync)
      .toArray();

    if (unsyncedNotes.length > 0) {
      const notesToPush = unsyncedNotes.map(n => ({
        id: n.id,
        user_id: userId,
        folder_id: n.folder_id,
        title: n.title,
        content: n.content,
        canvas_data: n.canvas_data,
        is_pinned: n.is_pinned === 1,
        is_locked: n.is_locked === 1,
        tags: n.tags,
        is_deleted: n.is_deleted === 1,
        version: n.version,
        updated_at: new Date(n.updated_at).toISOString(),
      }));

      const { error } = await supabase.from('notes').upsert(notesToPush);
      if (error) throw new Error(`Push notes failed: ${error.message}`);
    }

    // ==========================================
    // 3. PUSH ATTACHMENTS (upload files if local_only)
    // ==========================================
    const unsyncedAttachments = await db.attachments
      .where('is_local_only')
      .equals(1)
      .toArray();

    for (const att of unsyncedAttachments) {
      // If we have a local ObjectURL, we would typically upload the blob to Supabase Storage first.
      // For this implementation, we assume upload handling is done on save or we skip if blank.
      if (att.file_path.startsWith('blob:')) {
        try {
          const blob = await fetch(att.file_path).then(r => r.blob());
          const fileExt = att.filename.split('.').pop();
          const supabasePath = `${userId}/${att.id}.${fileExt}`;

          const { error: uploadError } = await supabase.storage
            .from('notes-attachments')
            .upload(supabasePath, blob);

          if (!uploadError) {
            // Get public URL
            const { data } = supabase.storage
              .from('notes-attachments')
              .getPublicUrl(supabasePath);

            att.file_path = data.publicUrl;
            att.is_local_only = 0;
            await db.attachments.put(att);
          } else {
            console.error(`File upload failed for ${att.filename}: ${uploadError.message}`);
          }
        } catch (err) {
          console.error(`File conversion failed for ${att.filename}:`, err);
        }
      }
    }

    // Upsert metadata changes for attachments
    const updatedAttachments = await db.attachments
      .where('created_at')
      .above(lastSync)
      .toArray();

    const attachmentsToPush = updatedAttachments
      .filter(a => a.is_local_only !== 1)
      .map(a => ({
        id: a.id,
        note_id: a.note_id,
        user_id: userId,
        filename: a.filename,
        file_path: a.file_path,
        file_type: a.file_type,
        annotations: a.annotations,
        created_at: new Date(a.created_at).toISOString(),
      }));

    if (attachmentsToPush.length > 0) {
      const { error } = await supabase.from('attachments').upsert(attachmentsToPush);
      if (error) throw new Error(`Push attachments failed: ${error.message}`);
    }

    // ==========================================
    // 4. PULL FOLDERS
    // ==========================================
    const { data: remoteFolders, error: pullFolderErr } = await supabase
      .from('folders')
      .select('*')
      .gt('updated_at', new Date(lastSync).toISOString());

    if (pullFolderErr) throw new Error(`Pull folders failed: ${pullFolderErr.message}`);

    if (remoteFolders) {
      for (const rf of remoteFolders) {
        const localFolder = await db.folders.get(rf.id);
        const remoteFolderUpdatedAt = new Date(rf.updated_at).getTime();

        if (!localFolder || remoteFolderUpdatedAt > localFolder.updated_at) {
          await db.folders.put({
            id: rf.id,
            user_id: rf.user_id,
            name: rf.name,
            parent_folder_id: rf.parent_folder_id,
            is_deleted: rf.is_deleted ? 1 : 0,
            updated_at: remoteFolderUpdatedAt,
          });
        }
      }
    }

    // ==========================================
    // 5. PULL NOTES & RESOLVE CONFLICTS
    // ==========================================
    const { data: remoteNotes, error: pullNotesErr } = await supabase
      .from('notes')
      .select('*')
      .gt('updated_at', new Date(lastSync).toISOString());

    if (pullNotesErr) throw new Error(`Pull notes failed: ${pullNotesErr.message}`);

    let pulledCount = 0;
    if (remoteNotes) {
      for (const rn of remoteNotes) {
        const localNote = await db.notes.get(rn.id);
        const remoteNoteUpdatedAt = new Date(rn.updated_at).getTime();

        if (!localNote) {
          // No local copy, save immediately
          await db.notes.put({
            id: rn.id,
            user_id: rn.user_id,
            folder_id: rn.folder_id,
            title: rn.title,
            content: rn.content,
            canvas_data: rn.canvas_data,
            is_pinned: rn.is_pinned ? 1 : 0,
            is_locked: rn.is_locked ? 1 : 0,
            tags: rn.tags || [],
            is_deleted: rn.is_deleted ? 1 : 0,
            version: rn.version,
            updated_at: remoteNoteUpdatedAt,
          });
          pulledCount++;
        } else if (remoteNoteUpdatedAt > localNote.updated_at) {
          // Remote is newer. Check if local had unsynced changes
          const isLocalModified = localNote.updated_at > lastSync;

          if (!isLocalModified) {
            // No conflict: local wasn't modified, overwrite safely
            await db.notes.put({
              id: rn.id,
              user_id: rn.user_id,
              folder_id: rn.folder_id,
              title: rn.title,
              content: rn.content,
              canvas_data: rn.canvas_data,
              is_pinned: rn.is_pinned ? 1 : 0,
              is_locked: rn.is_locked ? 1 : 0,
              tags: rn.tags || [],
              is_deleted: rn.is_deleted ? 1 : 0,
              version: rn.version,
              updated_at: remoteNoteUpdatedAt,
            });
            pulledCount++;
          } else {
            // CONFLICT! Both were modified. Last-Write-Wins (LWW) with History saving.
            console.warn(`[SYNC] Conflict detected on note ${rn.id}`);

            const localIsNewer = localNote.updated_at > remoteNoteUpdatedAt;
            
            // Backup the older one to history first
            const olderVersion = localIsNewer ? rn : localNote;
            await db.noteHistory.put({
              id: Math.random().toString(36).substring(2, 15),
              note_id: rn.id,
              user_id: userId,
              title: olderVersion.title,
              content: olderVersion.content || '',
              canvas_data: olderVersion.canvas_data,
              saved_at: localIsNewer ? remoteNoteUpdatedAt : localNote.updated_at,
            });

            // Upsert the history log to Supabase too
            await supabase.from('note_history').upsert({
              note_id: rn.id,
              user_id: userId,
              title: olderVersion.title,
              content: olderVersion.content || '',
              canvas_data: olderVersion.canvas_data,
              saved_at: new Date(localIsNewer ? remoteNoteUpdatedAt : localNote.updated_at).toISOString(),
            });

            if (localIsNewer) {
              // Local wins: push local again to override remote
              // (will be pushed on the next sync cycle automatically since updated_at > lastSync)
              console.log(`[SYNC] Local version wins for ${rn.id}`);
            } else {
              // Remote wins: overwrite local note
              console.log(`[SYNC] Remote version wins for ${rn.id}`);
              await db.notes.put({
                id: rn.id,
                user_id: rn.user_id,
                folder_id: rn.folder_id,
                title: rn.title,
                content: rn.content,
                canvas_data: rn.canvas_data,
                is_pinned: rn.is_pinned ? 1 : 0,
                is_locked: rn.is_locked ? 1 : 0,
                tags: rn.tags || [],
                is_deleted: rn.is_deleted ? 1 : 0,
                version: rn.version,
                updated_at: remoteNoteUpdatedAt,
              });
              pulledCount++;
            }
          }
        }
      }
    }

    // ==========================================
    // 6. PULL ATTACHMENTS
    // ==========================================
    const { data: remoteAttachments, error: pullAttErr } = await supabase
      .from('attachments')
      .select('*')
      .gt('created_at', new Date(lastSync).toISOString());

    if (pullAttErr) throw new Error(`Pull attachments failed: ${pullAttErr.message}`);

    if (remoteAttachments) {
      for (const ra of remoteAttachments) {
        const localAtt = await db.attachments.get(ra.id);
        const remoteAttCreatedAt = new Date(ra.created_at).getTime();

        if (!localAtt) {
          await db.attachments.put({
            id: ra.id,
            note_id: ra.note_id,
            user_id: ra.user_id,
            filename: ra.filename,
            file_path: ra.file_path,
            file_type: ra.file_type,
            annotations: ra.annotations,
            created_at: remoteAttCreatedAt,
          });
        } else if (ra.annotations !== localAtt.annotations) {
          // If annotations changed, merge
          localAtt.annotations = ra.annotations;
          await db.attachments.put(localAtt);
        }
      }
    }

    // Set new sync time to 'now'
    await setLastSyncTime(now);

    return {
      success: true,
      message: 'Sync complete!',
      pushedNotes: unsyncedNotes.length,
      pulledNotes: pulledCount,
    };
  } catch (error: unknown) {
    const errMsg = error instanceof Error ? error.message : 'Unknown sync error';
    console.error('[SYNC ERROR]:', error);
    return {
      success: false,
      message: errMsg,
      pushedNotes: 0,
      pulledNotes: 0,
    };
  }
}
