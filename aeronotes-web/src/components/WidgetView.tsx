/* eslint-disable react-hooks/purity */
'use client';

import React, { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../lib/db';
import { Plus, X, Pin, FileText } from 'lucide-react';


interface WidgetViewProps {
  userId: string;
}

export default function WidgetView({ userId }: WidgetViewProps) {
  const [newNoteText, setNewNoteText] = useState('');

  // Fetch recent active notes
  const notes = useLiveQuery(async () => {
    const activeNotes = await db.notes.where('is_deleted').equals(0).toArray();
    // Sort: pinned first, then by updated_at descending
    return activeNotes.sort((a, b) => {
      if (a.is_pinned !== b.is_pinned) {
        return b.is_pinned - a.is_pinned;
      }
      return b.updated_at - a.updated_at;
    }).slice(0, 5); // Only display top 5 notes in the widget
  }, []) || [];

  const handleQuickAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNoteText.trim()) return;

    await db.notes.put({
      id: crypto.randomUUID(),
      user_id: userId,
      folder_id: null,
      title: newNoteText.trim().substring(0, 30),
      content: `<div>${newNoteText.trim()}</div>`,
      canvas_data: null,
      is_pinned: 0,
      is_locked: 0,
      tags: ['quick-note'],
      is_deleted: 0,
      version: 1,
      updated_at: Date.now()
    });

    setNewNoteText('');
  };

  const handleTogglePin = async (noteId: string, currentPin: number) => {
    await db.notes.update(noteId, {
      is_pinned: currentPin === 1 ? 0 : 1,
      updated_at: Date.now()
    });
  };

  const handleCloseWidget = () => {
    // Call standard browser window close (supported by Tauri custom webviews)
    window.close();
  };

  return (
    <div className="w-full h-full flex flex-col bg-zinc-950/90 border border-zinc-850 rounded-2xl overflow-hidden shadow-2xl text-zinc-50 select-none animate-fade-in backdrop-blur-md">
      
      {/* Draggable Title Bar */}
      <div 
        data-tauri-drag-region
        className="h-10 bg-zinc-900 border-b border-zinc-850 px-4 flex items-center justify-between cursor-move"
      >
        <div data-tauri-drag-region className="flex items-center gap-2 text-xs font-bold text-amber-500 uppercase tracking-widest">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-ping" />
          AeroWidget
        </div>
        <button 
          onClick={handleCloseWidget}
          className="p-1 hover:bg-zinc-800 rounded-full transition-colors text-zinc-400 hover:text-white"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Input Panel for Quick Notes */}
      <form onSubmit={handleQuickAdd} className="p-3 border-b border-zinc-850">
        <div className="relative">
          <input
            type="text"
            placeholder="Jot down a quick note..."
            value={newNoteText}
            onChange={(e) => setNewNoteText(e.target.value)}
            className="w-full text-xs bg-zinc-900 border border-zinc-800 rounded-xl pl-3 pr-10 py-2.5 focus:outline-none focus:ring-1 focus:ring-amber-500 text-zinc-150"
          />
          <button 
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-amber-500 hover:text-amber-400"
          >
            <Plus className="h-4 w-4" />
          </button>
        </div>
      </form>

      {/* Checklist / Recent Notes List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest px-1">Recent Notes</span>
        
        <div className="space-y-1">
          {notes.map(note => (
            <div 
              key={note.id}
              className="flex items-center justify-between p-2 rounded-xl bg-zinc-900/40 border border-zinc-900/60 hover:bg-zinc-900/80 transition-colors"
            >
              <div className="flex items-center gap-2 min-w-0">
                <FileText className="h-4 w-4 text-amber-500 shrink-0" />
                <span className="text-xs truncate font-medium text-zinc-200">
                  {note.title || 'Untitled Note'}
                </span>
              </div>

              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => handleTogglePin(note.id, note.is_pinned)}
                  className={`p-1 hover:bg-zinc-800 rounded ${note.is_pinned === 1 ? 'text-amber-500' : 'text-zinc-650 hover:text-zinc-400'}`}
                >
                  <Pin className="h-3.5 w-3.5 fill-current" />
                </button>
              </div>
            </div>
          ))}

          {notes.length === 0 && (
            <p className="text-xs text-zinc-500 italic text-center py-6">No quick notes yet</p>
          )}
        </div>
      </div>

      {/* Widget Footer */}
      <div className="h-8 bg-zinc-900/40 border-t border-zinc-850/50 flex items-center justify-center text-[10px] font-semibold text-zinc-500">
        Double click border to pin
      </div>

    </div>
  );
}
