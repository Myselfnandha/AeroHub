import sys
import tkinter as tk
import ctypes

def main():
    if len(sys.argv) < 2:
        return
    text = sys.argv[1]
    
    # Parse state: check if passed in argv[2] or deduce from text
    state = "on"
    if len(sys.argv) > 2:
        state = sys.argv[2].lower()
    else:
        if "off" in text.lower() or "disabled" in text.lower():
            state = "off"

    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(bg="#000001", borderwidth=0, highlightthickness=0, relief="flat")
    # Make the #000001 background completely transparent
    root.attributes("-transparentcolor", "#000001")

    # Dimensions for two-line layout with icon
    w, h = 260, 60
    sw = root.winfo_screenwidth()
    
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
    
    rect = RECT()
    SPI_GETWORKAREA = 48
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    
    x = (sw - w) // 2
    y_target = rect.bottom - h - 15
    y_start = rect.bottom - h + 15 # Slide up by 30px
    
    root.geometry(f"{w}x{h}+{x}+{y_start}")
    
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

    # Draw the premium pill background with border
    create_round_rect(1, 1, w-1, h-1, radius=15, fill="#18181B", outline="#27272A", width=1)
    
    # Draw the status-based icon
    # Circular icon backdrop container on the left
    canvas.create_oval(12, 12, 48, 48, fill="#27272A", outline="")
    
    if state == "on":
        color = "#10B981" # Emerald Green
        # Draw tap rings
        canvas.create_oval(25, 17, 35, 27, outline=color, width=1.5)
        canvas.create_oval(21, 13, 39, 31, outline=color, width=1)
        
        # Pointing finger hand
        # Index finger
        canvas.create_line(30, 22, 30, 34, fill="white", width=4, capstyle="round")
        # Fist/Palm
        canvas.create_polygon([24, 32, 36, 32, 38, 42, 34, 45, 26, 45, 22, 42], fill="white", outline="")
        # Thumb
        canvas.create_line(24, 35, 20, 33, fill="white", width=3, capstyle="round")
    else:
        color = "#EF4444" # Crimson Red
        
        # Pointing finger hand (grayed out)
        canvas.create_line(30, 22, 30, 34, fill="#A1A1AA", width=4, capstyle="round")
        canvas.create_polygon([24, 32, 36, 32, 38, 42, 34, 45, 26, 45, 22, 42], fill="#A1A1AA", outline="")
        canvas.create_line(24, 35, 20, 33, fill="#A1A1AA", width=3, capstyle="round")
        
        # Red strike-through line
        canvas.create_line(15, 15, 45, 45, fill="#18181B", width=5, capstyle="round")
        canvas.create_line(16, 16, 44, 44, fill=color, width=3, capstyle="round")

    # Add the text fields
    # Title
    canvas.create_text(60, 20, text="Touch Screen", fill="#FFFFFF", font=("Segoe UI", 10, "bold"), anchor="w")
    # Status
    status_text = "Enabled" if state == "on" else "Disabled"
    canvas.create_text(60, 38, text=status_text, fill=color, font=("Segoe UI", 9, "bold"), anchor="w")
        
    root.attributes("-alpha", 0.0) # Start invisible for fade-in animation
    root.deiconify()

    # Animation variables
    steps = 15
    delay = 15 # ms
    current_step = 0

    def animate_entrance():
        nonlocal current_step
        if current_step < steps:
            current_step += 1
            # Easing: ease-out quadratic
            t = current_step / steps
            ease_t = t * (2 - t) # 0 to 1
            
            curr_alpha = ease_t * 0.95
            curr_y = int(y_start - ease_t * (y_start - y_target))
            
            root.attributes("-alpha", curr_alpha)
            root.geometry(f"{w}x{h}+{x}+{curr_y}")
            root.after(delay, animate_entrance)

    def start_exit():
        steps_exit = 10
        delay_exit = 15
        current_step_exit = 0
        
        def animate_exit():
            nonlocal current_step_exit
            if current_step_exit < steps_exit:
                current_step_exit += 1
                t = current_step_exit / steps_exit
                # Easing: ease-in quadratic
                ease_t = t * t
                curr_alpha = 0.95 * (1 - ease_t)
                curr_y = int(y_target + ease_t * 15)
                
                root.attributes("-alpha", curr_alpha)
                root.geometry(f"{w}x{h}+{x}+{curr_y}")
                root.after(delay_exit, animate_exit)
            else:
                root.destroy()
        animate_exit()

    # Start the entrance animation
    animate_entrance()
    
    # Schedule exit after 2.5 seconds
    root.after(2500, start_exit)
    root.mainloop()

if __name__ == "__main__":
    main()
