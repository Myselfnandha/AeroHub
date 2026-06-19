'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '../lib/supabase';
import { type Session } from '@supabase/supabase-js';
import { db } from '../lib/db';
import Sidebar from '../components/Sidebar';
import NoteList from '../components/NoteList';
import Editor from '../components/Editor';
import WidgetView from '../components/WidgetView';
import { BookOpen, LogOut, Loader2, ArrowLeft } from 'lucide-react';


export default function Home() {
  const router = useRouter();
  
  // Auth state
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  // Layout navigation state
  const [activeFolderId, setActiveFolderId] = useState<string | null>(null);
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [showTrash, setShowTrash] = useState(false);
  const [activeNoteId, setActiveNoteId] = useState<string | null>(null);
  const [isWidget] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.location.search.includes('widget=true');
    }
    return false;
  });

  // Mobile layout state ('sidebar' | 'list' | 'editor')
  const [mobileView, setMobileView] = useState<'sidebar' | 'list' | 'editor'>('sidebar');

  // Verify auth session on mount
  useEffect(() => {

    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
      if (!session) {
        router.push('/auth');
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setLoading(false);
      if (!session) {
        router.push('/auth');
      }
    });

    return () => subscription.unsubscribe();
  }, [router]);

  // Handle note creation
  const handleCreateNote = async () => {
    if (!session?.user) return;

    const noteId = crypto.randomUUID();
    await db.notes.put({
      id: noteId,
      user_id: session.user.id,
      folder_id: activeFolderId,
      title: 'Untitled Note',
      content: '<div>Start typing here...</div>',
      canvas_data: null,
      is_pinned: 0,
      is_locked: 0,
      tags: activeTag ? [activeTag] : [],
      is_deleted: 0,
      version: 1,
      updated_at: Date.now()
    });

    setActiveNoteId(noteId);
    setMobileView('editor');
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    router.push('/auth');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-50 dark:bg-zinc-950">
        <Loader2 className="h-8 w-8 animate-spin text-amber-500" />
        <span className="text-xs font-semibold text-zinc-500 mt-3 uppercase tracking-wider">Restoring Session</span>
      </div>
    );
  }

  if (!session) return null;

  if (isWidget) {
    return <WidgetView userId={session.user.id} />;
  }


  return (
    <div className="flex h-screen overflow-hidden bg-zinc-100 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-50 font-sans">
      
      {/* 1. Sidebar - Desktop: show always, Mobile: conditional */}
      <div className={`h-full shrink-0 lg:block ${mobileView === 'sidebar' ? 'block w-full lg:w-64' : 'hidden lg:w-64'}`}>
        <Sidebar
          userId={session.user.id}
          activeFolderId={activeFolderId}
          setActiveFolderId={(id) => {
            setActiveFolderId(id);
            setActiveTag(null);
            setMobileView('list');
          }}
          activeTag={activeTag}
          setActiveTag={(tag) => {
            setActiveTag(tag);
            setActiveFolderId(null);
            setMobileView('list');
          }}
          showTrash={showTrash}
          setShowTrash={(show) => {
            setShowTrash(show);
            setMobileView('list');
          }}
        />
        
        {/* Sign out helper floating over sidebar for custom ease */}
        <div className="lg:hidden p-4 bg-zinc-50 dark:bg-zinc-950">
          <button 
            onClick={handleSignOut}
            className="w-full flex items-center justify-center gap-2 py-2.5 bg-zinc-200 dark:bg-zinc-900 hover:bg-red-500/10 hover:text-red-500 text-sm font-semibold rounded-xl transition-colors"
          >
            <LogOut className="h-4 w-4" /> Sign Out
          </button>
        </div>
      </div>

      {/* 2. Middle Notes list pane - Desktop: show always, Mobile: conditional */}
      <div className={`h-full shrink-0 border-r border-zinc-200 dark:border-zinc-800 lg:block ${mobileView === 'list' ? 'block w-full lg:w-80' : 'hidden lg:w-80'}`}>
        
        {/* Mobile top-bar back to Sidebar */}
        <div className="lg:hidden flex h-14 items-center px-4 bg-zinc-50 dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800">
          <button 
            onClick={() => setMobileView('sidebar')}
            className="flex items-center gap-1.5 text-amber-500 text-sm font-semibold"
          >
            <ArrowLeft className="h-4 w-4" /> Folders
          </button>
        </div>

        <NoteList
          activeFolderId={activeFolderId}
          activeTag={activeTag}
          showTrash={showTrash}
          activeNoteId={activeNoteId}
          setActiveNoteId={(id) => {
            setActiveNoteId(id);
            setMobileView('editor');
          }}
          onCreateNote={handleCreateNote}
        />
      </div>

      {/* 3. Editor right workspace pane - Desktop: flex-1, Mobile: conditional */}
      <div className={`h-full flex-1 lg:flex flex-col ${mobileView === 'editor' ? 'flex w-full' : 'hidden'}`}>
        {activeNoteId ? (
          <Editor
            noteId={activeNoteId}
            onBackToList={() => setMobileView('list')}
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center bg-zinc-50 dark:bg-zinc-900/10 p-6 text-zinc-500">
            {/* Mobile top-bar back to List when no active note is loaded */}
            <div className="lg:hidden absolute top-0 left-0 w-full flex h-14 items-center px-4 bg-zinc-50 dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800">
              <button 
                onClick={() => setMobileView('list')}
                className="flex items-center gap-1.5 text-amber-500 text-sm font-semibold"
              >
                <ArrowLeft className="h-4 w-4" /> Notes
              </button>
            </div>
            
            <BookOpen className="h-14 w-14 opacity-25 mb-4 text-amber-500 animate-bounce" />
            <h3 className="text-lg font-bold text-zinc-800 dark:text-zinc-200">AeroNotes Workspace</h3>
            <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1.5">Select a note or folder from the sidebar, or make a new one.</p>
            
            {/* Desktop sign-out helper button */}
            <button 
              onClick={handleSignOut}
              className="mt-8 flex items-center gap-2 px-4 py-2 border border-zinc-200 dark:border-zinc-850 hover:bg-red-500/10 hover:text-red-500 text-xs font-bold rounded-xl text-zinc-500 transition-all"
            >
              <LogOut className="h-4 w-4" /> Sign Out from Account
            </button>
          </div>
        )}
      </div>

    </div>
  );
}
