import ctypes
from PIL import Image, ImageDraw
from core.logger import logger

# Theme (Luxury Minimal Dark)
TH = {
    "bg": "#0d0d0f",  # Pure minimalist dark
    "bg2": "#161619",  # Subtle card background
    "bg3": "#212124",  # Active element background
    "accent": "#00df77",  # Mint Green Accent
    "accent_hover": "#32e896",
    "fg": "#f5f5f7",  # Crisp, readable white
    "fg_dim": "#86868b",  # Elegant muted text
    "success": "#34c759",  # Refined green
    "warning": "#ff9f0a",  # Refined orange
    "danger": "#ff453a",  # Refined red
    "border": "#2c2c2e",  # Subtle borders
    "border_glow": "#48484a",  # Soft glow
}


def _add_hover(widget, bg_normal, bg_hover, fg_normal=None, fg_hover=None):
    def on_enter(e):
        widget.config(bg=bg_hover)
        if fg_hover is not None:
            widget.config(fg=fg_hover)

    def on_leave(e):
        widget.config(bg=bg_normal)
        if fg_normal is not None:
            widget.config(fg=fg_normal)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def apply_dwm_rounding(window):
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if hwnd == 0:
            hwnd = window.winfo_id()
        pref = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 33, ctypes.byref(pref), ctypes.sizeof(pref)
        )
    except Exception as e:
        logger.error(f"DWM rounding error: {e}")


def create_health_icon(paused: bool = False) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Luxury outer ring
    ring_color = (150, 150, 150, 255) if paused else (0, 223, 119, 255)
    draw.ellipse([2, 2, 62, 62], outline=ring_color, width=2)

    # Premium dark glassmorphism inner background
    bg_color = (40, 40, 42, 240) if paused else (22, 22, 25, 240)
    draw.ellipse([4, 4, 60, 60], fill=bg_color)

    # Glowing pulse/heartbeat line in the center
    pulse_color = (150, 150, 150, 255) if paused else (0, 223, 119, 255)
    
    # Heartbeat path coordinates (a sleek pulse wave)
    points = [
        (10, 32),
        (20, 32),
        (25, 20),
        (29, 44),
        (34, 12),
        (39, 52),
        (44, 32),
        (54, 32)
    ]
    
    # Draw glow effect (semi-transparent wider lines behind)
    glow_color = (150, 150, 150, 60) if paused else (0, 223, 119, 60)
    draw.line(points, fill=glow_color, width=6, joint="round")
    draw.line(points, fill=pulse_color, width=3, joint="round")

    # Add a glowing core dot at the peak
    if not paused:
        draw.ellipse([32, 10, 36, 14], fill=(255, 255, 255, 255))
    else:
        # Subtle cross for pause state
        draw.line([26, 26, 38, 38], fill=(255, 69, 58, 255), width=3)
        draw.line([38, 26, 26, 38], fill=(255, 69, 58, 255), width=3)

    return img
