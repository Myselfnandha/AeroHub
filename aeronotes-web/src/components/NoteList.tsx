'use client';

import React, { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db, type LocalNote } from '../lib/db';
import { Search, Pin, Plus, ShieldAlert } from 'lucide-react';

interface NoteListProps {
  activeFolderId: string | null;
  activeTag: string | null;
  showTrash: boolean;
  activeNoteId: string | null;
  setActiveNoteId: (id: string | null) => void;
  onCreateNote: () => void;
}

export default function NoteList({
  activeFolderId,
  activeTag,
  showTrash,
  activeNoteId,
  setActiveNoteId,
  onCreateNote
}: NoteListProps) {
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch and filter notes using Dexie live query
  const notes = useLiveQuery(async () => {
    let queryNotes: LocalNote[] = [];

    if (showTrash) {
      // Show soft-deleted notes
      queryNotes = await db.notes.where('is_deleted').equals(1).toArray();
    } else {
      // Show active notes
      queryNotes = await db.notes.where('is_deleted').equals(0).toArray();
      
      // Filter by folder if specified
      if (activeFolderId) {
        queryNotes = queryNotes.filter(n => n.folder_id === activeFolderId);
      }
      
      // Filter by tag if specified
      if (activeTag) {
        queryNotes = queryNotes.filter(n => n.tags && n.tags.includes(activeTag));
      }
    }

    // Apply client-side search query across title, content, and tags
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      queryNotes = queryNotes.filter(
        n => 
          n.title.toLowerCase().includes(q) || 
          (n.content && n.content.toLowerCase().includes(q)) ||
          (n.tags && n.tags.some(t => t.toLowerCase().includes(q)))
      );
    }

    // Sort notes: pinned notes first, then by updated_at descending
    return queryNotes.sort((a, b) => {
      if (a.is_pinned !== b.is_pinned) {
        return b.is_pinned - a.is_pinned; // 1 (pinned) comes before 0
      }
      return b.updated_at - a.updated_at;
    });
  }, [activeFolderId, activeTag, showTrash, searchQuery]) || [];

  const formatNoteDate = (timestamp: number) => {
    const date = new Date(timestamp);
    const now = new Date();
    
    // Check if it was today
    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Check if yesterday
    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1);
    if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    }

    // Else return formatted date
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
  };

  // Strip HTML tags for preview snippet (server-safe)
  const getPlainSnippet = (htmlContent: string) => {
    if (!htmlContent) return 'No additional text';
    const text = htmlContent.replace(/<[^>]*>/g, '');
    return text.substring(0, 60).trim() || 'No additional text';
  };

  // Separate pinned and regular notes
  const pinnedNotes = notes.filter(n => n.is_pinned === 1 && !showTrash);
  const regularNotes = notes.filter(n => n.is_pinned === 0 || showTrash);

  return (
    <div className="w-80 border-r border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 flex flex-col h-full">
      
      {/* Search and Action Bar */}
      <div className="p-4 space-y-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-extrabold tracking-tight text-zinc-950 dark:text-zinc-50">
            {showTrash ? 'Trash Bin' : activeTag ? `#${activeTag}` : 'Notes'}
          </h2>
          {!showTrash && (
            <button
              onClick={onCreateNote}
              className="flex items-center justify-center p-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-zinc-950 font-bold transition-all hover:scale-105 active:scale-95 shadow-md shadow-amber-500/10"
              title="New note"
            >
              <Plus className="h-5 w-5" />
            </button>
          )}
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400 dark:text-zinc-600" />
          <input
            type="text"
            placeholder="Search notes, tags, titles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl focus:outline-none focus:ring-1 focus:ring-amber-500 focus:border-amber-500 dark:text-zinc-100 dark:placeholder-zinc-650"
          />
        </div>
      </div>

      {/* Scrollable Notes List */}
      <div className="flex-1 overflow-y-auto divide-y divide-zinc-100 dark:divide-zinc-900/50">
        
        {/* Pinned Section */}
        {pinnedNotes.length > 0 && (
          <div className="p-2 space-y-0.5">
            <div className="flex items-center gap-1.5 px-3 py-1.5 text-[10px] font-bold text-amber-600 dark:text-amber-500 uppercase tracking-widest">
              <Pin className="h-3 w-3 fill-current" /> Pinned Notes
            </div>
            {pinnedNotes.map((note) => (
              <NoteCard
                key={note.id}
                note={note}
                isActive={activeNoteId === note.id}
                onClick={() => setActiveNoteId(note.id)}
                formatDate={formatNoteDate}
                getSnippet={getPlainSnippet}
              />
            ))}
          </div>
        )}

        {/* Regular Notes Section */}
        <div className="p-2 space-y-0.5">
          {pinnedNotes.length > 0 && regularNotes.length > 0 && (
            <div className="px-3 py-1.5 text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-widest">
              Notes
            </div>
          )}
          {regularNotes.map((note) => (
            <NoteCard
              key={note.id}
              note={note}
              isActive={activeNoteId === note.id}
              onClick={() => setActiveNoteId(note.id)}
              formatDate={formatNoteDate}
              getSnippet={getPlainSnippet}
            />
          ))}

          {notes.length === 0 && (
            <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
              <ShieldAlert className="h-8 w-8 text-zinc-300 dark:text-zinc-700 mb-2" />
              <p className="text-sm font-medium text-zinc-400 dark:text-zinc-600">No notes found</p>
            </div>
          )}
        </div>

      </div>

      {/* Footer Notes Counter */}
      <div className="p-3 text-center border-t border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 text-xs font-semibold text-zinc-500 dark:text-zinc-400">
        {notes.length} {notes.length === 1 ? 'Note' : 'Notes'}
      </div>

    </div>
  );
}

interface NoteCardProps {
  note: LocalNote;
  isActive: boolean;
  onClick: () => void;
  formatDate: (timestamp: number) => string;
  getSnippet: (htmlContent: string) => string;
}

function NoteCard({ note, isActive, onClick, formatDate, getSnippet }: NoteCardProps) {
  const snippet = getSnippet(note.content);

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-3.5 rounded-xl transition-all flex flex-col gap-1.5 ${isActive ? 'bg-amber-500/10 border-amber-500/10' : 'hover:bg-zinc-100 dark:hover:bg-zinc-900/40'}`}
    >
      <div className="flex items-center justify-between gap-2">
        <h3 className={`font-bold text-sm tracking-tight truncate ${isActive ? 'text-amber-600 dark:text-amber-500' : 'text-zinc-800 dark:text-zinc-200'}`}>
          {note.title || 'Untitled Note'}
        </h3>
        {note.is_pinned === 1 && (
          <Pin className="h-3 w-3 text-amber-500 fill-current shrink-0" />
        )}
      </div>

      <div className="flex items-baseline gap-2">
        <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-400 shrink-0">
          {formatDate(note.updated_at)}
        </span>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 truncate flex-1">
          {snippet}
        </p>
      </div>

      {note.tags && note.tags.length > 0 && (
        <div className="flex gap-1 overflow-hidden">
          {note.tags.slice(0, 2).map(t => (
            <span key={t} className="text-[10px] font-semibold text-amber-600 dark:text-amber-500 bg-amber-500/5 px-2 py-0.5 rounded-full border border-amber-500/10">
              #{t}
            </span>
          ))}
          {note.tags.length > 2 && (
            <span className="text-[10px] font-semibold text-zinc-400 dark:text-zinc-600">
              +{note.tags.length - 2}
            </span>
          )}
        </div>
      )}
    </button>
  );
}
