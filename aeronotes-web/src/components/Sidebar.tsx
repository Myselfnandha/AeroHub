'use client';

import React, { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../lib/db';
import { runSync } from '../lib/sync';
import { 
  Folder, 
  FolderPlus, 
  Tag, 
  Trash2, 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  Sparkles,
  BookOpen
} from 'lucide-react';

interface SidebarProps {
  userId: string;
  activeFolderId: string | null;
  setActiveFolderId: (id: string | null) => void;
  activeTag: string | null;
  setActiveTag: (tag: string | null) => void;
  showTrash: boolean;
  setShowTrash: (show: boolean) => void;
}

export default function Sidebar({
  userId,
  activeFolderId,
  setActiveFolderId,
  activeTag,
  setActiveTag,
  showTrash,
  setShowTrash
}: SidebarProps) {
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState('Synced');
  const [isOnline, setIsOnline] = useState(typeof navigator !== 'undefined' ? navigator.onLine : true);
  
  const [newFolderName, setNewFolderName] = useState('');
  const [showNewFolderInput, setShowNewFolderInput] = useState(false);

  // Sync state tracking
  React.useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Fetch folders using Dexie live query
  const folders = useLiveQuery(async () => {
    return await db.folders.where('is_deleted').equals(0).toArray();
  }) || [];

  // Extract all unique tags from active notes
  const tags = useLiveQuery(async () => {
    const activeNotes = await db.notes.where('is_deleted').equals(0).toArray();
    const allTags = new Set<string>();
    activeNotes.forEach(n => {
      if (n.tags) n.tags.forEach(t => allTags.add(t));
    });
    return Array.from(allTags);
  }) || [];

  const handleCreateFolder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFolderName.trim()) return;

    const folderId = crypto.randomUUID();
    await db.folders.put({
      id: folderId,
      user_id: userId,
      name: newFolderName.trim(),
      parent_folder_id: null,
      is_deleted: 0,
      updated_at: Date.now()
    });

    setNewFolderName('');
    setShowNewFolderInput(false);
    setActiveFolderId(folderId);
    setShowTrash(false);
    setActiveTag(null);
  };

  const handleSync = async () => {
    if (isSyncing) return;
    setIsSyncing(true);
    setSyncMessage('Syncing...');
    
    const status = await runSync(userId);
    setIsSyncing(false);
    setSyncMessage(status.success ? 'Synced' : 'Failed');
    
    setTimeout(() => {
      setSyncMessage(status.success ? 'Synced' : 'Retry Sync');
    }, 3000);
  };

  const selectAllNotes = () => {
    setActiveFolderId(null);
    setActiveTag(null);
    setShowTrash(false);
  };

  const selectFolder = (id: string) => {
    setActiveFolderId(id);
    setActiveTag(null);
    setShowTrash(false);
  };

  const selectTag = (tag: string) => {
    setActiveTag(tag);
    setActiveFolderId(null);
    setShowTrash(false);
  };

  const selectTrash = () => {
    setShowTrash(true);
    setActiveFolderId(null);
    setActiveTag(null);
  };

  return (
    <aside className="w-64 border-r border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 flex flex-col h-full select-none">
      
      {/* App Logo & Header */}
      <div className="flex h-16 items-center justify-between px-6 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-amber-500" />
          <h1 className="font-bold text-lg text-zinc-900 dark:text-zinc-50 tracking-tight">AeroNotes</h1>
        </div>
        
        {/* Sync Status Button */}
        <button 
          onClick={handleSync}
          disabled={isSyncing}
          className="flex items-center justify-center p-2 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-900 text-zinc-600 dark:text-zinc-400 transition-colors"
          title="Manual sync"
        >
          {isSyncing ? (
            <RefreshCw className="h-4 w-4 animate-spin text-amber-500" />
          ) : isOnline ? (
            <Wifi className="h-4 w-4 text-emerald-500" />
          ) : (
            <WifiOff className="h-4 w-4 text-red-500" />
          )}
        </button>
      </div>

      {/* Main Sidebar Navigation Tree */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6">
        
        {/* Pinned / Global Views */}
        <div className="space-y-1">
          <button 
            onClick={selectAllNotes}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-sm font-medium transition-colors ${!activeFolderId && !activeTag && !showTrash ? 'bg-amber-500/10 text-amber-600 dark:text-amber-500 font-semibold' : 'text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200/50 dark:hover:bg-zinc-900/50'}`}
          >
            <span className="flex items-center gap-2.5">
              <Sparkles className="h-4 w-4" /> All iCloud Notes
            </span>
          </button>

          <button 
            onClick={selectTrash}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-sm font-medium transition-colors ${showTrash ? 'bg-amber-500/10 text-amber-600 dark:text-amber-500 font-semibold' : 'text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200/50 dark:hover:bg-zinc-900/50'}`}
          >
            <span className="flex items-center gap-2.5">
              <Trash2 className="h-4 w-4" /> Recently Deleted
            </span>
          </button>
        </div>

        {/* Folders List */}
        <div>
          <div className="flex items-center justify-between px-3 mb-2 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
            <span>Folders</span>
            <button 
              onClick={() => setShowNewFolderInput(!showNewFolderInput)}
              className="p-1 hover:bg-zinc-200 dark:hover:bg-zinc-900 rounded text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-100"
            >
              <FolderPlus className="h-4 w-4" />
            </button>
          </div>

          {/* New Folder Inline Form */}
          {showNewFolderInput && (
            <form onSubmit={handleCreateFolder} className="px-3 mb-2">
              <input
                autoFocus
                type="text"
                value={newFolderName}
                onChange={(e) => setNewFolderName(e.target.value)}
                placeholder="New Folder..."
                className="w-full text-sm bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-800 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-amber-500 dark:text-zinc-50"
              />
            </form>
          )}

          <div className="space-y-0.5">
            {folders.map(folder => (
              <button
                key={folder.id}
                onClick={() => selectFolder(folder.id)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-sm transition-colors ${activeFolderId === folder.id ? 'bg-amber-500/10 text-amber-600 dark:text-amber-500 font-semibold' : 'text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200/50 dark:hover:bg-zinc-900/50'}`}
              >
                <span className="flex items-center gap-2.5">
                  <Folder className="h-4 w-4 text-amber-600 dark:text-amber-500" />
                  <span className="truncate">{folder.name}</span>
                </span>
              </button>
            ))}
            
            {folders.length === 0 && !showNewFolderInput && (
              <p className="text-xs text-zinc-400 dark:text-zinc-600 px-3 py-1 italic">No folders yet</p>
            )}
          </div>
        </div>

        {/* Tags Section */}
        <div>
          <h2 className="px-3 mb-2 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Tags</h2>
          <div className="flex flex-wrap gap-1.5 px-3">
            {tags.map(tag => (
              <button
                key={tag}
                onClick={() => selectTag(tag)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-all ${activeTag === tag ? 'bg-amber-500 border-amber-500 text-zinc-950 shadow-md font-semibold scale-105' : 'bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}
              >
                <Tag className="h-3 w-3" />
                <span>#{tag}</span>
              </button>
            ))}

            {tags.length === 0 && (
              <p className="text-xs text-zinc-400 dark:text-zinc-600 italic">No tags in notes</p>
            )}
          </div>
        </div>

      </div>

      {/* Sync Status / User Profile Section */}
      <div className="p-4 border-t border-zinc-200 dark:border-zinc-800 bg-zinc-100/50 dark:bg-zinc-950 flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
        <span className="flex items-center gap-1.5 font-medium">
          <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-red-500'}`} />
          {syncMessage}
        </span>
        <span className="opacity-80">Phase 1 Personal</span>
      </div>

    </aside>
  );
}
