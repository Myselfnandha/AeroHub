'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Undo2, Redo2, Edit3, Eraser, Check, X, FileText } from 'lucide-react';

interface PDFAnnotatorProps {
  fileUrl: string;
  filename: string;
  initialAnnotations: string | null; // Base64 drawing overlay
  onSave: (annotationsDataUrl: string) => void;
  onClose: () => void;
}

export default function PDFAnnotator({ fileUrl, filename, initialAnnotations, onSave, onClose }: PDFAnnotatorProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState('#eab308'); // Apple Gold/Amber markup
  const brushSize = 3;
  const [tool, setTool] = useState<'pen' | 'eraser'>('pen');
  
  const [history, setHistory] = useState<string[]>([]);
  const [historyStep, setHistoryStep] = useState(-1);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Load initial annotations overlay if exists
    if (initialAnnotations) {
      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0, rect.width, rect.height);
        const url = canvas.toDataURL();
        setHistory([url]);
        setHistoryStep(0);
      };
      img.src = initialAnnotations;
    } else {
      const url = canvas.toDataURL();
      setHistory([url]);
      setHistoryStep(0);
    }
  }, [initialAnnotations]);

  const getCoordinates = (e: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    if ('touches' in e) {
      if (e.touches.length === 0) return { x: 0, y: 0 };
      return {
        x: e.touches[0].clientX - rect.left,
        y: e.touches[0].clientY - rect.top
      };
    } else {
      return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
    }
  };

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const { x, y } = getCoordinates(e);
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.beginPath();
    ctx.moveTo(x, y);
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    e.preventDefault();
    const { x, y } = getCoordinates(e);
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.lineWidth = brushSize;
    if (tool === 'eraser') {
      ctx.globalCompositeOperation = 'destination-out';
      ctx.strokeStyle = 'rgba(0,0,0,1)';
    } else {
      ctx.globalCompositeOperation = 'source-over';
      ctx.strokeStyle = color;
    }
    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    const canvas = canvasRef.current;
    if (!canvas) return;

    const dataUrl = canvas.toDataURL();
    const newHistory = history.slice(0, historyStep + 1);
    newHistory.push(dataUrl);
    setHistory(newHistory);
    setHistoryStep(newHistory.length - 1);
  };

  const handleUndo = () => {
    if (historyStep <= 0) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const rect = canvas.getBoundingClientRect();
    const nextStep = historyStep - 1;
    setHistoryStep(nextStep);

    ctx.clearRect(0, 0, rect.width, rect.height);
    const img = new Image();
    img.onload = () => {
      ctx.globalCompositeOperation = 'source-over';
      ctx.drawImage(img, 0, 0, rect.width, rect.height);
    };
    img.src = history[nextStep];
  };

  const handleRedo = () => {
    if (historyStep >= history.length - 1) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const rect = canvas.getBoundingClientRect();
    const nextStep = historyStep + 1;
    setHistoryStep(nextStep);

    ctx.clearRect(0, 0, rect.width, rect.height);
    const img = new Image();
    img.onload = () => {
      ctx.globalCompositeOperation = 'source-over';
      ctx.drawImage(img, 0, 0, rect.width, rect.height);
    };
    img.src = history[nextStep];
  };

  const handleClear = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const rect = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);

    const dataUrl = canvas.toDataURL();
    const newHistory = history.slice(0, historyStep + 1);
    newHistory.push(dataUrl);
    setHistory(newHistory);
    setHistoryStep(newHistory.length - 1);
  };

  const handleSave = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    onSave(canvas.toDataURL());
  };

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-zinc-950/80 backdrop-blur-md animate-fade-in">
      {/* Header bar */}
      <div className="flex h-14 items-center justify-between border-b border-zinc-800 bg-zinc-900/90 px-6 text-zinc-50">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-amber-500" />
          <span className="font-semibold truncate max-w-xs sm:max-w-md">Annotate: {filename}</span>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={handleUndo} disabled={historyStep <= 0} className="rounded p-1.5 hover:bg-zinc-800 disabled:opacity-40">
            <Undo2 className="h-5 w-5" />
          </button>
          <button onClick={handleRedo} disabled={historyStep >= history.length - 1} className="rounded p-1.5 hover:bg-zinc-800 disabled:opacity-40">
            <Redo2 className="h-5 w-5" />
          </button>
          <button onClick={handleClear} className="rounded p-1.5 text-red-400 hover:bg-red-500/10" title="Clear all annotations">
            <Eraser className="h-5 w-5" />
          </button>
          <div className="h-6 w-px bg-zinc-800" />
          <button onClick={onClose} className="flex h-9 items-center gap-1 rounded bg-zinc-800 px-3 hover:bg-zinc-700 text-sm font-medium">
            <X className="h-4 w-4" /> Cancel
          </button>
          <button onClick={handleSave} className="flex h-9 items-center gap-1 rounded bg-amber-500 px-4 hover:bg-amber-600 text-zinc-950 font-semibold text-sm transition-all">
            <Check className="h-4 w-4" /> Save Markup
          </button>
        </div>
      </div>

      {/* Main split: PDF viewer on left, markup canvas on top */}
      <div className="flex-1 flex overflow-hidden justify-center bg-zinc-900 relative">
        <div className="w-full h-full max-w-4xl p-6 relative flex justify-center items-center">
          
          {/* Native PDF view as base layer */}
          <iframe 
            src={`${fileUrl}#toolbar=0`} 
            className="w-full h-full border border-zinc-800 bg-white rounded-xl shadow-2xl pointer-events-none"
            title="PDF Document"
          />

          {/* Transparent Overlay drawing canvas */}
          <canvas
            ref={canvasRef}
            onMouseDown={startDrawing}
            onMouseMove={draw}
            onMouseUp={stopDrawing}
            onMouseLeave={stopDrawing}
            onTouchStart={startDrawing}
            onTouchMove={draw}
            onTouchEnd={stopDrawing}
            className="absolute top-6 left-6 w-[calc(100%-48px)] h-[calc(100%-48px)] bg-transparent touch-none cursor-crosshair rounded-xl z-10"
          />
        </div>
      </div>

      {/* Apple-style Tool Shelf */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex items-center gap-6 rounded-2xl border border-zinc-800 bg-zinc-900/90 shadow-2xl px-6 py-3 backdrop-blur z-20">
        <div className="flex items-center gap-2 border-r border-zinc-800 pr-4">
          <button 
            onClick={() => setTool('pen')}
            className={`rounded-lg p-2 transition-colors ${tool === 'pen' ? 'bg-amber-500/10 text-amber-500' : 'text-zinc-400 hover:text-zinc-200'}`}
          >
            <Edit3 className="h-5 w-5" />
          </button>
          <button 
            onClick={() => setTool('eraser')}
            className={`rounded-lg p-2 transition-colors ${tool === 'eraser' ? 'bg-amber-500/10 text-amber-500' : 'text-zinc-400 hover:text-zinc-200'}`}
          >
            <Eraser className="h-5 w-5" />
          </button>
        </div>
        
        {/* Colors */}
        <div className="flex items-center gap-2">
          {['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6', '#000000'].map((hex) => (
            <button
              key={hex}
              onClick={() => {
                setColor(hex);
                setTool('pen');
              }}
              className={`w-5 h-5 rounded-full border border-zinc-700 transition-transform hover:scale-110 ${color === hex && tool === 'pen' ? 'ring-2 ring-amber-500 ring-offset-2 ring-offset-zinc-900' : ''}`}
              style={{ backgroundColor: hex }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
