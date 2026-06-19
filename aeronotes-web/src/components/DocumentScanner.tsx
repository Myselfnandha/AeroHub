'use client';

import React, { useRef, useState, useEffect } from 'react';
import { Camera, X, Check, RefreshCw } from 'lucide-react';

interface DocumentScannerProps {
  onScan: (scannedDataUrl: string, filename: string) => void;
  onClose: () => void;
}

export default function DocumentScanner({ onScan, onClose }: DocumentScannerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [filter, setFilter] = useState<'none' | 'mono' | 'scan'>('scan'); // 'scan' is high-contrast b&w
  const [error, setError] = useState<string | null>(null);

  // Initialize camera stream
  useEffect(() => {
    async function startCamera() {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } },
          audio: false
        });
        setStream(mediaStream);
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch (err: unknown) {
        console.error('Camera access error:', err);
        setError('Could not access the camera. Make sure permissions are granted.');
      }
    }

    startCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleCapture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas dimensions to match video stream resolution
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current frame
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Apply the chosen pixel filters
    applyFilters(ctx, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/png');
    setCapturedImage(dataUrl);

    // Turn off camera stream to save power
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const applyFilters = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    if (filter === 'none') return;

    const imgData = ctx.getImageData(0, 0, width, height);
    const data = imgData.data;

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];

      // Grayscale calculation
      const gray = 0.299 * r + 0.587 * g + 0.114 * b;

      if (filter === 'mono') {
        data[i] = gray;
        data[i + 1] = gray;
        data[i + 2] = gray;
      } else if (filter === 'scan') {
        // High-contrast document thresholding
        const threshold = 128;
        const val = gray > threshold ? 255 : 0;
        data[i] = val;
        data[i + 1] = val;
        data[i + 2] = val;
      }
    }

    ctx.putImageData(imgData, 0, 0);
  };

  const handleRetake = async () => {
    setCapturedImage(null);
    setError(null);
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } },
        audio: false
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch {
      setError('Could not restart the camera.');
    }
  };

  const handleConfirm = () => {
    if (!capturedImage) return;
    const filename = `Scan_${new Date().toISOString().slice(0,10)}_${Math.floor(Math.random()*1000)}.png`;
    onScan(capturedImage, filename);
  };

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-black text-white animate-fade-in">
      {/* Header */}
      <div className="flex h-14 items-center justify-between bg-zinc-900/90 px-6 border-b border-zinc-800">
        <div className="flex items-center gap-2">
          <Camera className="h-5 w-5 text-amber-500" />
          <span className="font-semibold tracking-wide">iScan Document Camera</span>
        </div>
        <button onClick={onClose} className="p-2 hover:bg-zinc-800 rounded-full transition-colors">
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Main Viewfinder / Result */}
      <div className="flex-1 flex flex-col justify-center items-center relative overflow-hidden bg-black p-4">
        {error ? (
          <div className="text-center p-6 bg-zinc-900 rounded-xl border border-zinc-800 max-w-sm">
            <p className="text-red-400 mb-4">{error}</p>
            <button onClick={onClose} className="px-4 py-2 bg-zinc-800 rounded hover:bg-zinc-700">Go Back</button>
          </div>
        ) : capturedImage ? (
          <img 
            src={capturedImage} 
            alt="Scanned Document" 
            className="max-h-[70vh] max-w-full rounded-lg border border-zinc-800 shadow-2xl object-contain animate-scale-up"
          />
        ) : (
          <div className="relative w-full h-full max-w-lg max-h-[70vh] rounded-2xl overflow-hidden border border-zinc-800 bg-zinc-950">
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline 
              muted 
              className="w-full h-full object-cover"
            />
            {/* Overlay document guide box */}
            <div className="absolute inset-8 border-2 border-dashed border-amber-500/50 rounded-xl pointer-events-none flex items-center justify-center">
              <span className="text-xs text-amber-500/70 bg-black/50 px-2 py-1 rounded">Align document edges</span>
            </div>
          </div>
        )}
      </div>

      {/* Hidden processing canvas */}
      <canvas ref={canvasRef} className="hidden" />

      {/* Controls */}
      <div className="bg-zinc-950 border-t border-zinc-900 px-6 py-8 flex flex-col gap-6 items-center">
        {/* Filter Toolbar (only active when not yet captured) */}
        {!capturedImage && (
          <div className="flex items-center gap-3 bg-zinc-900 p-1.5 rounded-full border border-zinc-850">
            {(['none', 'mono', 'scan'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wider transition-all ${filter === f ? 'bg-amber-500 text-zinc-950 shadow-md' : 'text-zinc-400 hover:text-zinc-200'}`}
              >
                {f === 'none' ? 'Color' : f === 'mono' ? 'B&W Photo' : 'Scan Mode'}
              </button>
            ))}
          </div>
        )}

        {/* Action button */}
        <div className="flex justify-between items-center w-full max-w-xs">
          {capturedImage ? (
            <>
              <button 
                onClick={handleRetake}
                className="flex flex-col items-center gap-1.5 text-zinc-400 hover:text-white"
              >
                <div className="p-3 bg-zinc-900 hover:bg-zinc-850 rounded-full border border-zinc-800">
                  <RefreshCw className="h-5 w-5" />
                </div>
                <span className="text-xs">Retake</span>
              </button>

              <button 
                onClick={handleConfirm}
                className="flex flex-col items-center gap-1.5 text-amber-500 hover:text-amber-400"
              >
                <div className="p-4 bg-amber-500 hover:bg-amber-600 rounded-full text-zinc-950 font-bold shadow-lg shadow-amber-500/20">
                  <Check className="h-6 w-6" />
                </div>
                <span className="text-xs font-semibold">Save Attachment</span>
              </button>
            </>
          ) : (
            <div className="flex justify-center w-full">
              <button 
                onClick={handleCapture}
                disabled={!stream}
                className="p-5 bg-white hover:bg-zinc-200 text-black rounded-full shadow-2xl disabled:opacity-40 transition-all hover:scale-105 active:scale-95"
              >
                <Camera className="h-8 w-8" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
