import sys
import tkinter as tk
import ctypes

def main():
    if len(sys.argv) < 2:
        return
    text = sys.argv[1]

    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(bg="#000001", borderwidth=0, highlightthickness=0, relief="flat")
    # Make the #000001 background completely transparent
    root.attributes("-transparentcolor", "#000001")

    # Hardcoded dimensions to guarantee perfect positioning instantly
    w, h = 220, 35
    sw = root.winfo_screenwidth()
    
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
    
    rect = RECT()
    SPI_GETWORKAREA = 48
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    
    x = (sw - w) // 2
    y = rect.bottom - h - 15 
    
    root.geometry(f"{w}x{h}+{x}+{y}")
    
    canvas = tk.Canvas(root, width=w, height=h, bg="#000001", highlightthickness=0, borderwidth=0)
    canvas.pack(fill="both", expand=True)

    # Function to draw a smooth rounded rectangle on the canvas
    def create_round_rect(x1, y1, x2, y2, radius=15, **kwargs):
        points = [
            x1+radius, y1,   x1+radius, y1,   x2-radius, y1,   x2-radius, y1,
            x2, y1,          x2, y1+radius,   x2, y1+radius,   x2, y2-radius,
            x2, y2-radius,   x2, y2,          x2-radius, y2,   x2-radius, y2,
            x1+radius, y2,   x1+radius, y2,   x1, y2,          x1, y2-radius,
            x1, y2-radius,   x1, y1+radius,   x1, y1+radius,   x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    # Draw the pill background
    create_round_rect(0, 0, w, h, radius=18, fill="#222222", outline="")
    
    # Add the text in the center
    canvas.create_text(w/2, h/2, text=text, fill="white", font=("Segoe UI", 9, "bold"))
        
    root.attributes("-alpha", 0.9) # Make it visible!
    root.deiconify()
    # Increased time to 2.5 seconds
    root.after(2500, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()
