import Dexie, { type Table } from 'dexie';

export interface LocalFolder {
  id: string; // UUID generated locally
  user_id: string;
  name: string;
  parent_folder_id: string | null;
  is_deleted: number; // 0 = false, 1 = true (Dexie indexing works better with numbers)
  updated_at: number; // Unix timestamp in ms
}

export interface LocalNote {
  id: string;
  user_id: string;
  folder_id: string | null;
  title: string;
  content: string; // HTML Rich Text
  canvas_data: string | null; // Base64 drawing
  is_pinned: number; // 0 = false, 1 = true
  is_locked: number; // 0 = false, 1 = true
  tags: string[]; // List of tags
  is_deleted: number;
  version: number;
  updated_at: number;
}

export interface LocalAttachment {
  id: string;
  note_id: string;
  user_id: string;
  filename: string;
  file_path: string; // Local ObjectURL or remote Supabase Storage URL
  file_type: string; // MIME type
  annotations: string | null; // SVG/JSON markups
  created_at: number;
  is_local_only?: number; // 1 if not uploaded to Supabase yet
}

export interface LocalNoteHistory {
  id: string;
  note_id: string;
  user_id: string;
  title: string;
  content: string;
  canvas_data: string | null;
  saved_at: number;
}

export interface SyncMetadata {
  key: string;
  value: string;
}

export class AeroNotesDB extends Dexie {
  folders!: Table<LocalFolder>;
  notes!: Table<LocalNote>;
  attachments!: Table<LocalAttachment>;
  noteHistory!: Table<LocalNoteHistory>;
  syncMeta!: Table<SyncMetadata>;

  constructor() {
    super('AeroNotesDB');
    this.version(1).stores({
      folders: 'id, user_id, parent_folder_id, is_deleted, updated_at',
      notes: 'id, user_id, folder_id, is_pinned, is_locked, *tags, is_deleted, updated_at',
      attachments: 'id, note_id, user_id, created_at, is_local_only',
      noteHistory: 'id, note_id, user_id, saved_at',
      syncMeta: 'key',
    });
  }
}

export const db = new AeroNotesDB();
