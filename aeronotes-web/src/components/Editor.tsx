/* eslint-disable react-hooks/purity */
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Underline } from '@tiptap/extension-underline';
import { Highlight } from '@tiptap/extension-highlight';
import { Table } from '@tiptap/extension-table';
import { TableRow } from '@tiptap/extension-table-row';
import { TableCell } from '@tiptap/extension-table-cell';
import { TableHeader } from '@tiptap/extension-table-header';
import { TaskList } from '@tiptap/extension-task-list';
import { TaskItem } from '@tiptap/extension-task-item';


import { useLiveQuery } from 'dexie-react-hooks';
import { db, type LocalAttachment } from '../lib/db';
import DrawingCanvas from './DrawingCanvas';
import PDFAnnotator from './PDFAnnotator';
import DocumentScanner from './DocumentScanner';

import {
  Bold,
  Italic,
  Underline as UnderlineIcon,
  Heading1,
  Heading2,
  Heading3,
  List,
  ListOrdered,
  CheckSquare,
  Table as TableIcon,
  Palette,
  FileText,
  Camera,
  Trash2,
  Pin,
  Lock,
  Unlock,
  Plus,
  Tag,
  Paperclip,
  Download,
  ArrowLeft
} from 'lucide-react';

interface EditorProps {
  noteId: string;
  onBackToList?: () => void;
}

export default function Editor({ noteId, onBackToList }: EditorProps) {
  const [activeCanvas, setActiveCanvas] = useState(false);
  const [activeScanner, setActiveScanner] = useState(false);
  const [activePdfAnnotator, setActivePdfAnnotator] = useState<LocalAttachment | null>(null);
  const [showTagInput, setShowTagInput] = useState(false);
  const [newTag, setNewTag] = useState('');
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch active note
  const note = useLiveQuery(async () => {
    return await db.notes.get(noteId);
  }, [noteId]);

  // Fetch folders for relocation option
  const folders = useLiveQuery(async () => {
    return await db.folders.where('is_deleted').equals(0).toArray();
  }) || [];

  // Fetch attachments for this note
  const attachments = useLiveQuery(async () => {
    return await db.attachments.where('note_id').equals(noteId).toArray();
  }, [noteId]) || [];

  // Initialize TipTap editor
  const editor = useEditor({
    extensions: [
      StarterKit,
      Underline,
      Highlight,
      Table.configure({ resizable: true }),
      TableRow,
      TableHeader,
      TableCell,
      TaskList,
      TaskItem.configure({ nested: true }),
    ],
    content: '',
    onUpdate: ({ editor }) => {
      // Auto-save debounced content edit
      const html = editor.getHTML();
      debounceSave(html);
    },
    editorProps: {
      attributes: {
        class: 'prose dark:prose-invert max-w-none focus:outline-none min-h-[300px] text-zinc-800 dark:text-zinc-200 text-base leading-relaxed',
      },
    },
  }, [noteId]);

  // Sync editor content with database note selection
  useEffect(() => {
    if (editor && note) {
      if (editor.getHTML() !== note.content) {
        editor.commands.setContent(note.content || '');
      }
    }
  }, [note, editor]);

  // Debounced auto-save handler
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const debounceSave = (htmlContent: string) => {
    if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);

    saveTimeoutRef.current = setTimeout(async () => {
      if (!note) return;
      await db.notes.update(noteId, {
        content: htmlContent,
        version: note.version + 1,
        updated_at: Date.now(),
      });
    }, 800);
  };

  if (!note) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-zinc-50 dark:bg-zinc-950 p-6 text-zinc-500">
        <FileText className="h-12 w-12 opacity-30 mb-2" />
        <p className="text-sm font-semibold">Select a note to start writing</p>
      </div>
    );
  }

  const handleTitleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = e.target.value;
    await db.notes.update(noteId, {
      title: newTitle,
      version: note.version + 1,
      updated_at: Date.now(),
    });
  };

  const handleTogglePin = async () => {
    await db.notes.update(noteId, {
      is_pinned: note.is_pinned === 1 ? 0 : 1,
      version: note.version + 1,
      updated_at: Date.now(),
    });
  };

  const handleToggleLock = async () => {
    await db.notes.update(noteId, {
      is_locked: note.is_locked === 1 ? 0 : 1,
      version: note.version + 1,
      updated_at: Date.now(),
    });
  };

  const handleDelete = async () => {
    await db.notes.update(noteId, {
      is_deleted: note.is_deleted === 1 ? 0 : 1, // toggle or delete
      version: note.version + 1,
      updated_at: Date.now(),
    });
    if (onBackToList) onBackToList();
  };

  const handleMoveFolder = async (folderId: string | null) => {
    await db.notes.update(noteId, {
      folder_id: folderId ? folderId : null,
      version: note.version + 1,
      updated_at: Date.now(),
    });
  };

  const handleAddTag = async (e: React.FormEvent) => {
    e.preventDefault();
    const tag = newTag.trim().toLowerCase();
    if (!tag) return;

    const currentTags = note.tags || [];
    if (!currentTags.includes(tag)) {
      const updatedTags = [...currentTags, tag];
      await db.notes.update(noteId, {
        tags: updatedTags,
        version: note.version + 1,
        updated_at: Date.now(),
      });
    }

    setNewTag('');
    setShowTagInput(false);
  };

  const handleRemoveTag = async (tagToRemove: string) => {
    const updatedTags = (note.tags || []).filter(t => t !== tagToRemove);
    await db.notes.update(noteId, {
      tags: updatedTags,
      version: note.version + 1,
      updated_at: Date.now(),
    });
  };

  // Upload/Add local attachments
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const attId = crypto.randomUUID();
      const localUrl = URL.createObjectURL(file);

      await db.attachments.put({
        id: attId,
        note_id: noteId,
        user_id: note.user_id,
        filename: file.name,
        file_path: localUrl,
        file_type: file.type || 'application/octet-stream',
        annotations: null,
        created_at: Date.now(),
        is_local_only: 1 // Upload mediator will sync this online
      });
    }
  };

  // Saved sketches from DrawingCanvas
  const handleSaveCanvas = async (dataUrl: string) => {
    await db.notes.update(noteId, {
      canvas_data: dataUrl,
      version: note.version + 1,
      updated_at: Date.now(),
    });
    setActiveCanvas(false);
  };

  // Saved scans from DocumentScanner
  const handleSaveScanner = async (scannedDataUrl: string, filename: string) => {
    const attId = crypto.randomUUID();
    await db.attachments.put({
      id: attId,
      note_id: noteId,
      user_id: note.user_id,
      filename: filename,
      file_path: scannedDataUrl,
      file_type: 'image/png',
      annotations: null,
      created_at: Date.now(),
      is_local_only: 1
    });
    setActiveScanner(false);
  };

  // Saved PDF markups from PDFAnnotator
  const handleSavePDFAnnotations = async (annotationsDataUrl: string) => {
    if (activePdfAnnotator) {
      await db.attachments.update(activePdfAnnotator.id, {
        annotations: annotationsDataUrl
      });
      setActivePdfAnnotator(null);
    }
  };

  // Styles for file attachment cards (especially Apple formats)
  const getAttachmentStyles = (filename: string, fileType: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    
    // Keynote (.key)
    if (ext === 'key' || fileType.includes('iwork-keynote')) {
      return { bg: 'bg-blue-500/10 dark:bg-blue-500/5', border: 'border-blue-500/30', label: 'Keynote', color: 'text-blue-500' };
    }
    // Numbers (.numbers)
    if (ext === 'numbers' || fileType.includes('iwork-numbers')) {
      return { bg: 'bg-emerald-500/10 dark:bg-emerald-500/5', border: 'border-emerald-500/30', label: 'Numbers', color: 'text-emerald-500' };
    }
    // Pages (.pages)
    if (ext === 'pages' || fileType.includes('iwork-pages')) {
      return { bg: 'bg-orange-500/10 dark:bg-orange-500/5', border: 'border-orange-500/30', label: 'Pages', color: 'text-orange-500' };
    }
    // PDF
    if (ext === 'pdf' || fileType.includes('pdf')) {
      return { bg: 'bg-red-500/10 dark:bg-red-500/5', border: 'border-red-500/30', label: 'PDF Document', color: 'text-red-500' };
    }
    // Image
    if (fileType.startsWith('image/')) {
      return { bg: 'bg-zinc-100 dark:bg-zinc-900', border: 'border-zinc-200 dark:border-zinc-800', label: 'Image', color: 'text-zinc-500' };
    }
    
    return { bg: 'bg-zinc-100 dark:bg-zinc-900', border: 'border-zinc-200 dark:border-zinc-800', label: 'File', color: 'text-zinc-500' };
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-zinc-50 dark:bg-zinc-900/40 relative">
      
      {/* Editor Top Bar Toolbar */}
      <div className="h-14 border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur px-6 flex items-center justify-between">
        
        {/* Navigation & Folder Move Option */}
        <div className="flex items-center gap-3">
          {onBackToList && (
            <button 
              onClick={onBackToList}
              className="lg:hidden p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900 text-zinc-600 dark:text-zinc-400"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
          )}

          {/* Folder Move Selector */}
          <select
            value={note.folder_id || ''}
            onChange={(e) => handleMoveFolder(e.target.value || null)}
            className="text-xs font-semibold tracking-wide border border-zinc-200 dark:border-zinc-800 bg-zinc-100 dark:bg-zinc-900 text-zinc-700 dark:text-zinc-300 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-amber-500"
          >
            <option value="">Move to iCloud Notes</option>
            {folders.map(f => (
              <option key={f.id} value={f.id}>{f.name}</option>
            ))}
          </select>
        </div>

        {/* Action icons shelf */}
        <div className="flex items-center gap-2">
          
          {/* Sketch Draw trigger */}
          <button
            onClick={() => setActiveCanvas(true)}
            className="p-2 rounded-xl text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900 transition-colors"
            title="Sketch Draw"
          >
            <Palette className="h-5 w-5" />
          </button>

          {/* Camera Scanner trigger */}
          <button
            onClick={() => setActiveScanner(true)}
            className="p-2 rounded-xl text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900 transition-colors"
            title="Scan Document"
          >
            <Camera className="h-5 w-5" />
          </button>

          {/* Attach file trigger */}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="p-2 rounded-xl text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900 transition-colors"
            title="Attach file"
          >
            <Paperclip className="h-5 w-5" />
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            multiple
            className="hidden"
          />

          <div className="h-6 w-px bg-zinc-200 dark:bg-zinc-800 mx-1" />

          {/* Pin trigger */}
          <button
            onClick={handleTogglePin}
            className={`p-2 rounded-xl transition-colors ${note.is_pinned === 1 ? 'text-amber-500 bg-amber-500/10' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900'}`}
            title="Pin Note"
          >
            <Pin className="h-5 w-5" />
          </button>

          {/* Lock trigger */}
          <button
            onClick={handleToggleLock}
            className={`p-2 rounded-xl transition-colors ${note.is_locked === 1 ? 'text-amber-500 bg-amber-500/10' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900'}`}
            title="Lock Folder"
          >
            {note.is_locked === 1 ? <Lock className="h-5 w-5" /> : <Unlock className="h-5 w-5" />}
          </button>

          {/* Delete trigger */}
          <button
            onClick={handleDelete}
            className="p-2 rounded-xl text-red-500 hover:bg-red-500/10 transition-colors"
            title={note.is_deleted === 1 ? 'Permanently Delete' : 'Move to Trash'}
          >
            <Trash2 className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Editor Content Area */}
      <div className="flex-1 overflow-y-auto px-10 py-8 space-y-6">
        
        {/* Title Input */}
        <input
          type="text"
          value={note.title}
          onChange={handleTitleChange}
          placeholder="New Note Title..."
          className="w-full text-3xl font-extrabold tracking-tight bg-transparent text-zinc-950 dark:text-white focus:outline-none placeholder-zinc-350"
        />

        {/* Tag chips row */}
        <div className="flex flex-wrap items-center gap-1.5 min-h-[30px] border-b border-zinc-100 dark:border-zinc-800/50 pb-4">
          <Tag className="h-3.5 w-3.5 text-zinc-400" />
          
          {(note.tags || []).map(tag => (
            <span 
              key={tag} 
              className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold text-amber-600 dark:text-amber-500 bg-amber-500/5 border border-amber-500/10"
            >
              #{tag}
              <button 
                onClick={() => handleRemoveTag(tag)}
                className="hover:text-red-500 font-bold ml-0.5 text-[10px]"
              >
                ✕
              </button>
            </span>
          ))}

          {showTagInput ? (
            <form onSubmit={handleAddTag} className="inline-block">
              <input
                autoFocus
                type="text"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                placeholder="tag..."
                className="w-16 text-xs bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-750 rounded-full px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-amber-500 dark:text-zinc-100"
              />
            </form>
          ) : (
            <button
              onClick={() => setShowTagInput(true)}
              className="flex items-center gap-0.5 text-xs text-zinc-500 hover:text-amber-500 font-medium px-2 py-0.5 rounded-full border border-dashed border-zinc-350"
            >
              <Plus className="h-3 w-3" /> Add Tag
            </button>
          )}
        </div>

        {/* Drawings overlay if exists */}
        {note.canvas_data && (
          <div className="group relative max-w-lg border border-zinc-200 dark:border-zinc-800 rounded-2xl overflow-hidden bg-zinc-950 shadow-md">
            <img src={note.canvas_data} alt="Note Sketch" className="w-full max-h-60 object-contain" />
            <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1.5">
              <button 
                onClick={() => setActiveCanvas(true)}
                className="px-2.5 py-1 text-xs bg-zinc-900/90 hover:bg-zinc-800 text-white rounded-md font-semibold border border-zinc-700 shadow"
              >
                Edit Sketch
              </button>
              <button 
                onClick={async () => {
                  await db.notes.update(noteId, { canvas_data: null, version: note.version + 1, updated_at: Date.now() });
                }}
                className="p-1 text-red-400 bg-zinc-900/90 hover:bg-zinc-800 rounded-md border border-zinc-700 shadow"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Custom TipTap Toolbar for inline formatting */}
        {editor && (
          <div className="flex flex-wrap items-center gap-1.5 bg-zinc-100 dark:bg-zinc-900/60 p-2 rounded-2xl border border-zinc-200 dark:border-zinc-800/80 mb-4">
            <button
              onClick={() => editor.chain().focus().toggleBold().run()}
              className={`p-1.5 rounded-lg ${editor.isActive('bold') ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <Bold className="h-4 w-4" />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleItalic().run()}
              className={`p-1.5 rounded-lg ${editor.isActive('italic') ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <Italic className="h-4 w-4" />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleUnderline().run()}
              className={`p-1.5 rounded-lg ${editor.isActive('underline') ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <UnderlineIcon className="h-4 w-4" />
            </button>

            <div className="h-5 w-px bg-zinc-200 dark:bg-zinc-800 mx-1" />

            <button
              onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
              className={`p-1.5 rounded-lg ${editor.isActive('heading', { level: 1 }) ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <Heading1 className="h-4 w-4" />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
              className={`p-1.5 rounded-lg ${editor.isActive('heading', { level: 2 }) ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <Heading2 className="h-4 w-4" />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
              className={`p-1.5 rounded-lg ${editor.isActive('heading', { level: 3 }) ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <Heading3 className="h-4 w-4" />
            </button>

            <div className="h-5 w-px bg-zinc-200 dark:bg-zinc-800 mx-1" />

            <button
              onClick={() => editor.chain().focus().toggleBulletList().run()}
              className={`p-1.5 rounded-lg ${editor.isActive('bulletList') ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <List className="h-4 w-4" />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleOrderedList().run()}
              className={`p-1.5 rounded-lg ${editor.isActive('orderedList') ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <ListOrdered className="h-4 w-4" />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleTaskList().run()}
              className={`p-1.5 rounded-lg ${editor.isActive('taskList') ? 'bg-amber-500 text-zinc-950 font-bold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800'}`}
            >
              <CheckSquare className="h-4 w-4" />
            </button>

            <div className="h-5 w-px bg-zinc-200 dark:bg-zinc-800 mx-1" />

            <button
              onClick={() => editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()}
              className="p-1.5 rounded-lg text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-800"
              title="Insert Table"
            >
              <TableIcon className="h-4 w-4" />
            </button>
          </div>
        )}

        {/* TipTap Editor instance */}
        <div className="min-h-[350px]">
          <EditorContent editor={editor} />
        </div>

        {/* File Attachments List (Apple Format cards included) */}
        {attachments.length > 0 && (
          <div className="space-y-3 pt-6 border-t border-zinc-200 dark:border-zinc-800">
            <h3 className="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Attachments ({attachments.length})</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {attachments.map(att => {
                const styles = getAttachmentStyles(att.filename, att.file_type);
                const isImg = att.file_type.startsWith('image/');
                const isPdf = att.file_type.includes('pdf');
                
                return (
                  <div 
                    key={att.id}
                    className={`flex flex-col rounded-xl border ${styles.border} ${styles.bg} overflow-hidden shadow-sm hover:shadow-md transition-shadow`}
                  >
                    {isImg ? (
                      <div className="h-32 bg-zinc-900 flex justify-center items-center overflow-hidden border-b border-zinc-200 dark:border-zinc-800">
                        <img src={att.file_path} alt={att.filename} className="w-full h-full object-cover" />
                      </div>
                    ) : (
                      <div className="p-4 flex items-center gap-3">
                        <FileText className={`h-8 w-8 ${styles.color}`} />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 truncate">{att.filename}</p>
                          <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">{styles.label}</span>
                        </div>
                      </div>
                    )}

                    {/* Actions panel */}
                    <div className="px-4 py-2.5 bg-zinc-100/50 dark:bg-zinc-950/50 border-t border-zinc-200/50 dark:border-zinc-800/50 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        {isPdf && (
                          <button
                            onClick={() => setActivePdfAnnotator(att)}
                            className="text-xs font-semibold text-amber-600 dark:text-amber-500 hover:underline flex items-center gap-1"
                          >
                            <Palette className="h-3.5 w-3.5" /> Markup
                          </button>
                        )}
                        <a 
                          href={att.file_path} 
                          download={att.filename}
                          className="text-xs font-semibold text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 flex items-center gap-1"
                        >
                          <Download className="h-3.5 w-3.5" /> Download
                        </a>
                      </div>
                      
                      <button 
                        onClick={async () => {
                          await db.attachments.delete(att.id);
                        }}
                        className="text-red-500 hover:text-red-600 p-1 rounded hover:bg-red-500/10"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>

                    {/* Show annotations preview inside cards if exist */}
                    {att.annotations && (
                      <div className="p-2 bg-zinc-950 flex justify-center border-t border-zinc-800">
                        <img src={att.annotations} alt="Annotated markup overlay" className="max-h-20 object-contain opacity-80" />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

      </div>

      {/* Floating Canvas Sketch Overlay */}
      {activeCanvas && (
        <DrawingCanvas
          initialData={note.canvas_data}
          onSave={handleSaveCanvas}
          onClose={() => setActiveCanvas(false)}
        />
      )}

      {/* Floating PDF Annotator Overlay */}
      {activePdfAnnotator && (
        <PDFAnnotator
          fileUrl={activePdfAnnotator.file_path}
          filename={activePdfAnnotator.filename}
          initialAnnotations={activePdfAnnotator.annotations}
          onSave={handleSavePDFAnnotations}
          onClose={() => setActivePdfAnnotator(null)}
        />
      )}

      {/* Floating Camera Document Scanner Overlay */}
      {activeScanner && (
        <DocumentScanner
          onScan={handleSaveScanner}
          onClose={() => setActiveScanner(false)}
        />
      )}

    </div>
  );
}
