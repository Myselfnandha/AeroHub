import sys
import os
import json
import tkinter as tk
import ctypes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "touch_settings.json")

def load_settings(is_preview=False):
    path = os.path.join(SCRIPT_DIR, "temp_preview.json") if is_preview else SETTINGS_FILE
    if os.path.exists(path):
        try:
            with open(path, "r") as f: return json.load(f)
        except Exception: pass
    
    return {
        "toast_pos": "Center", "toast_anim_style": "Slide",
        "toast_width": 260, "toast_height": 60,
        "toast_bg_color": "#18181B", "toast_fg_color": "#FFFFFF",
        "toast_font_size": 11, "toast_font_weight": "bold",
        "toast_emoji": "🖐️", "toast_radius": 15,
        "toast_padding_x": 12, "toast_padding_y": 10,
        "toast_opacity": 0.95, "toast_border_width": 1,
        "toast_border_color": "#27272A", "toast_enable_sound": False
    }

def main():
    if len(sys.argv) < 2: return
    text = sys.argv[1]
    
    state = "on"
    if len(sys.argv) > 2:
        state = sys.argv[2].lower()
    else:
        if "off" in text.lower() or "disabled" in text.lower():
            state = "off"
            
    is_preview = len(sys.argv) > 3 and sys.argv[3] == "1"
    settings = load_settings(is_preview)
    
    if is_preview:
        try: os.remove(os.path.join(SCRIPT_DIR, "temp_preview.json"))
        except Exception: pass

    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    
    trans_color = "#010203"
    root.config(bg=trans_color)
    root.attributes("-transparentcolor", trans_color)
    root.attributes("-alpha", 0.0)

    tw = int(settings.get("toast_width", 260))
    th = int(settings.get("toast_height", 60))
    pos = settings.get("toast_pos", "Center").lower()
    bg_col = settings.get("toast_bg_color", "#18181B")
    fg_col = settings.get("toast_fg_color", "#ffffff")
    font_size = int(settings.get("toast_font_size", 11))
    font_weight = settings.get("toast_font_weight", "bold")
    emoji = settings.get("toast_emoji", "🖐️")
    radius = int(settings.get("toast_radius", 15))
    padx = int(settings.get("toast_padding_x", 12))
    pady = int(settings.get("toast_padding_y", 10))
    anim_style = settings.get("toast_anim_style", "slide").lower()
    opacity = float(settings.get("toast_opacity", 0.95))
    border_width = int(settings.get("toast_border_width", 1))
    border_color = settings.get("toast_border_color", "#27272A")

    sw = root.winfo_screenwidth()
    final_y = 60

    if pos == "left":
        final_x = 20
        start_x, start_y = -tw - 10, final_y
    elif pos == "right":
        final_x = sw - tw - 20
        start_x, start_y = sw + 10, final_y
    else:
        final_x = (sw - tw) // 2
        start_x, start_y = final_x, -th - 10

    if anim_style == "fade":
        root.geometry(f"{tw}x{th}+{final_x}+{final_y}")
    else:
        root.geometry(f"{tw}x{th}+{start_x}+{start_y}")

    canvas = tk.Canvas(root, width=tw, height=th, bg=trans_color, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Draw rounded rect
    points = [
        radius, 0, tw - radius, 0,
        tw, 0, tw, radius,
        tw, th - radius, tw, th,
        tw - radius, th, radius, th,
        0, th, 0, th - radius,
        0, radius, 0, 0,
    ]
    if border_width > 0:
        canvas.create_polygon(points, smooth=True, fill=bg_col, outline=border_color, width=border_width)
    else:
        canvas.create_polygon(points, smooth=True, fill=bg_col)

    # Text
    msg_font = ("Segoe UI", font_size, font_weight)
    
    # State specific text
    if state == "off":
        status_text = "Touch screen disabled"
        state_col = "#EF4444"
    else:
        status_text = "Touch screen enabled"
        state_col = "#10B981"
        
    if is_preview:
        status_text = "Preview Mode Active"
        state_col = "#ff8800"

    canvas.create_text(
        padx + 10, pady, anchor=tk.NW,
        text=f"{emoji}  {text}",
        font=msg_font, fill=fg_col,
    )
    
    sub_font = ("Segoe UI", max(8, font_size - 2))
    canvas.create_text(
        padx + 10, pady + font_size + 8, anchor=tk.NW,
        text=status_text,
        font=sub_font, fill=state_col,
    )

    root.update_idletasks()
    
    closing = False
    
    def slide_in(step=0):
        if closing: return
        if step <= 20:
            p = step / 20
            ease = 1 - (1 - p) ** 3
            if anim_style == "fade":
                root.attributes("-alpha", min(opacity, ease * opacity))
            else:
                cx = int(start_x + (final_x - start_x) * ease)
                cy = int(start_y + (final_y - start_y) * ease)
                try:
                    root.geometry(f"{tw}x{th}+{cx}+{cy}")
                    root.attributes("-alpha", min(opacity, ease * opacity))
                except tk.TclError: pass
            root.after(16, lambda: slide_in(step + 1))
        else:
            root.after(2500, slide_out)

    def slide_out(step=0):
        nonlocal closing
        closing = True
        if step <= 15:
            p = step / 15
            ease = p * p
            if anim_style == "fade":
                root.attributes("-alpha", max(0, opacity * (1 - ease)))
            else:
                cx = int(final_x)
                cy = int(final_y - ease * 20)
                try:
                    root.geometry(f"{tw}x{th}+{cx}+{cy}")
                    root.attributes("-alpha", max(0, opacity * (1 - ease)))
                except tk.TclError: pass
            root.after(16, lambda: slide_out(step + 1))
        else:
            root.destroy()
            
    # Audio
    if settings.get("toast_enable_sound", False) and not is_preview:
        try:
            import winsound
            sound_path = os.path.join(SCRIPT_DIR, "resources", "on_pre_break.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception: pass

    root.deiconify()
    slide_in(0)
    root.mainloop()

if __name__ == "__main__":
    main()
