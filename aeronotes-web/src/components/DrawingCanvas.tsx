'use client';

import React, { useRef, useState, useEffect } from 'react';
import { Undo2, Redo2, Eraser, Edit3, Trash2, X, Check } from 'lucide-react';

interface DrawingCanvasProps {
  initialData: string | null;
  onSave: (dataUrl: string) => void;
  onClose: () => void;
}

export default function DrawingCanvas({ initialData, onSave, onClose }: DrawingCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState('#d97706'); // Warm gold/amber accent by default
  const [brushSize, setBrushSize] = useState(4);
  const [tool, setTool] = useState<'pen' | 'eraser'>('pen');
  
  // History stacks for Undo / Redo
  const [history, setHistory] = useState<string[]>([]);
  const [historyStep, setHistoryStep] = useState(-1);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Make canvas crisp on high-res displays
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

    // Set background to transparent or off-white paper texture
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Load initial canvas drawing if provided
    if (initialData) {
      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0, rect.width, rect.height);
        // Save initial state
        const initialUrl = canvas.toDataURL();
        setHistory([initialUrl]);
        setHistoryStep(0);
      };
      img.src = initialData;
    } else {
      const initialUrl = canvas.toDataURL();
      setHistory([initialUrl]);
      setHistoryStep(0);
    }

    // Handle resize
    const handleResize = () => {
      const tempImage = canvas.toDataURL();
      const currentRect = canvas.getBoundingClientRect();
      canvas.width = currentRect.width * window.devicePixelRatio;
      canvas.height = currentRect.height * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0, currentRect.width, currentRect.height);
      };
      img.src = tempImage;
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getCoordinates = (e: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };

    const rect = canvas.getBoundingClientRect();
    
    // Support Touch & Mouse coordinates
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
      ctx.strokeStyle = 'rgba(0,0,0,1)'; // destination-out ignores color
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

    // Push new state to history
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
          <Edit3 className="h-5 w-5 text-amber-500" />
          <h2 className="font-semibold tracking-wide">Sketchpad Markup</h2>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={handleUndo} 
            disabled={historyStep <= 0}
            className="rounded p-1.5 hover:bg-zinc-800 disabled:opacity-40"
          >
            <Undo2 className="h-5 w-5" />
          </button>
          <button 
            onClick={handleRedo} 
            disabled={historyStep >= history.length - 1}
            className="rounded p-1.5 hover:bg-zinc-800 disabled:opacity-40"
          >
            <Redo2 className="h-5 w-5" />
          </button>
          <button 
            onClick={handleClear}
            className="rounded p-1.5 text-red-400 hover:bg-red-500/10"
            title="Clear canvas"
          >
            <Trash2 className="h-5 w-5" />
          </button>
          <div className="h-6 w-px bg-zinc-800" />
          <button 
            onClick={onClose}
            className="flex h-9 items-center gap-1 rounded bg-zinc-800 px-3 hover:bg-zinc-700 text-sm font-medium"
          >
            <X className="h-4 w-4" /> Cancel
          </button>
          <button 
            onClick={handleSave}
            className="flex h-9 items-center gap-1 rounded bg-amber-500 px-4 hover:bg-amber-600 text-zinc-950 font-semibold text-sm transition-all"
          >
            <Check className="h-4 w-4" /> Save Markup
          </button>
        </div>
      </div>

      {/* Drawing Space */}
      <div className="flex-1 overflow-hidden p-6 flex justify-center items-center bg-zinc-900 relative">
        {/* Subtle grid pattern background for sketchbook feel */}
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]" />
        
        <canvas
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
          className="w-full h-full max-w-4xl max-h-[75vh] bg-zinc-950 border border-zinc-800 shadow-2xl touch-none cursor-crosshair rounded-xl"
        />
      </div>

      {/* Floating Apple-style toolbar at bottom */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex items-center gap-6 rounded-2xl border border-zinc-800 bg-zinc-900/90 shadow-2xl px-6 py-3 backdrop-blur">
        {/* Tool selector */}
        <div className="flex items-center gap-2 border-r border-zinc-800 pr-4">
          <button 
            onClick={() => setTool('pen')}
            className={`rounded-lg p-2.5 transition-colors ${tool === 'pen' ? 'bg-amber-500/10 text-amber-500' : 'text-zinc-400 hover:text-zinc-200'}`}
            title="Pen"
          >
            <Edit3 className="h-5 w-5" />
          </button>
          <button 
            onClick={() => setTool('eraser')}
            className={`rounded-lg p-2.5 transition-colors ${tool === 'eraser' ? 'bg-amber-500/10 text-amber-500' : 'text-zinc-400 hover:text-zinc-200'}`}
            title="Eraser"
          >
            <Eraser className="h-5 w-5" />
          </button>
        </div>

        {/* Brush Size selector */}
        <div className="flex items-center gap-2 border-r border-zinc-800 pr-4">
          {[2, 4, 8, 16].map((size) => (
            <button
              key={size}
              onClick={() => setBrushSize(size)}
              className={`flex items-center justify-center rounded-full hover:bg-zinc-800 ${brushSize === size ? 'ring-2 ring-amber-500' : ''}`}
              style={{ width: 28, height: 28 }}
            >
              <div 
                className="bg-zinc-300 rounded-full" 
                style={{ width: Math.max(size/2, 2), height: Math.max(size/2, 2) }} 
              />
            </button>
          ))}
        </div>

        {/* Color Palette */}
        <div className="flex items-center gap-2">
          {['#ffffff', '#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6', '#1e293b'].map((hex) => (
            <button
              key={hex}
              onClick={() => {
                setColor(hex);
                setTool('pen');
              }}
              className={`w-6 h-6 rounded-full border border-zinc-700 transition-transform hover:scale-110 ${color === hex && tool === 'pen' ? 'ring-2 ring-amber-500 ring-offset-2 ring-offset-zinc-900' : ''}`}
              style={{ backgroundColor: hex }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
