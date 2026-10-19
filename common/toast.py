"""
AeroHub Toast Notifications — Compact Dynamic Island Pill & Cross-Platform Engine.

Features:
- Compact Dynamic Island Pill: Sleek top-center capsule notification (~275px width).
- Single Firework Emoji: '🔥' with subtle left-to-right shake in-animation.
- Red Temperature Badge: Bold, color-coded temperature pill level.
- Clean and non-distracting: Fast pop-in, auto-dismiss, click to close.
- Fallback to Tkinter toast for environments without PySide6.
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import threading
import time

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import tkinter as tk

try:
    from common.dwm import apply_rounded_corners
    from common.tray import get_theme
except ImportError:
    apply_rounded_corners = lambda *_: None
    get_theme = lambda: {"dark": True, "accent_hex": "#ef4444"}

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toast_config.json")

_active_toasts: list[tk.Tk] = []
_lock = threading.Lock()

_DEFAULT_TOAST_CONFIG = {
    "position": "top-center",
    "animation": "slide",
    "duration_sec": 4,
    "width": 380,
    "height": 80,
    "border_radius": 12,
    "font_family": "Segoe UI",
    "font_size_title": 13,
    "font_size_body": 11,
    "padding": 16,
    "margin": 10,
    "sound_enabled": False,
    "bg_color": None,
    "text_color": None,
    "accent_color": None,
    "border_color": None,
    "style": "dynamic_island",
}


def _load_toast_config(module_name: str) -> dict:
    config = dict(_DEFAULT_TOAST_CONFIG)
    try:
        if os.path.exists(_CONFIG_PATH):
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                all_config = json.load(f)
            if module_name in all_config:
                config.update(all_config[module_name])
    except (json.JSONDecodeError, OSError):
        pass
    return config


def _resolve_colors(config: dict) -> dict:
    theme = get_theme()
    if theme["dark"]:
        defaults = {
            "bg_color": "#1a1a2e",
            "text_color": "#e8e8e8",
            "accent_color": theme["accent_hex"],
            "border_color": "#2a2a3e",
        }
    else:
        defaults = {
            "bg_color": "#ffffff",
            "text_color": "#1a1a1a",
            "accent_color": theme["accent_hex"],
            "border_color": "#d0d0d0",
        }

    resolved = dict(config)
    for key in ("bg_color", "text_color", "accent_color", "border_color"):
        if resolved.get(key) is None:
            resolved[key] = defaults[key]
    return resolved


def _calculate_position(
    config: dict, screen_w: int, screen_h: int, stack_index: int
) -> tuple[int, int]:
    w = config["width"]
    h = config["height"]
    margin = config["margin"]
    stack_offset = stack_index * (h + margin)

    pos = config["position"]
    if pos == "top-center":
        x = (screen_w - w) // 2
        y = margin + stack_offset
    elif pos == "top-right":
        x = screen_w - w - margin
        y = margin + stack_offset
    elif pos == "top-left":
        x = margin
        y = margin + stack_offset
    elif pos == "bottom-right":
        x = screen_w - w - margin
        y = screen_h - h - margin - stack_offset
    elif pos == "bottom-left":
        x = margin
        y = screen_h - h - margin - stack_offset
    elif pos == "bottom-center":
        x = (screen_w - w) // 2
        y = screen_h - h - margin - stack_offset
    else:
        x = (screen_w - w) // 2
        y = margin + stack_offset

    return x, y


def _slide_in(root: tk.Tk, target_y: int, current_y: int, step: int = 4):
    if not root.winfo_exists():
        return
    pos = root.winfo_y()
    if step > 0 and pos < target_y:
        new_y = min(pos + step, target_y)
    elif step < 0 and pos > target_y:
        new_y = max(pos + step, target_y)
    else:
        return
    root.geometry(f"+{root.winfo_x()}+{new_y}")
    root.after(10, _slide_in, root, target_y, current_y, step)


def _fade_out(root: tk.Tk, alpha: float = 1.0):
    if not root.winfo_exists():
        return
    alpha -= 0.05
    if alpha <= 0:
        _remove_toast(root)
        return
    root.attributes("-alpha", alpha)
    root.after(30, _fade_out, root, alpha)


def _remove_toast(root: tk.Tk):
    with _lock:
        if root in _active_toasts:
            _active_toasts.remove(root)
    try:
        root.destroy()
    except tk.TclError:
        pass


def _fade_in(root: tk.Tk, alpha: float = 0.0):
    if not root.winfo_exists():
        return
    alpha += 0.05
    if alpha >= 0.95:
        root.attributes("-alpha", 0.95)
        return
    root.attributes("-alpha", alpha)
    root.after(20, _fade_in, root, alpha)


def _extract_temp_str(text: str) -> str:
    m = re.search(r'(\d+[\.,]?\d*)\s*°?[Cc]', text)
    if m:
        return f"{m.group(1)}°C"
    return ""


# ─────────────────────────────────────────────────────────────
# Compact Dynamic Island Pill Notification (PySide6)
# ─────────────────────────────────────────────────────────────


def _play_alert_chime() -> None:
    """Play a subtle desktop warning chime on Linux/Windows for critical alerts."""
    try:
        import shutil
        if shutil.which("canberra-gtk-play"):
            subprocess.Popen(
                ["canberra-gtk-play", "-i", "dialog-warning"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        if shutil.which("paplay"):
            for sound_path in [
                "/usr/share/sounds/freedesktop/stereo/dialog-warning.oga",
                "/usr/share/sounds/Oxygen-Sys-Warning.ogg",
                "/usr/share/sounds/gnome/default/alerts/glass.ogg",
            ]:
                if os.path.exists(sound_path):
                    subprocess.Popen(
                        ["paplay", sound_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return
    except Exception:
        pass


def _run_dynamic_island_process(
    title: str,
    body: str,
    temp_level: str,
    icon_text: str,
    duration_sec: float,
    accent_color: str,
    sound: bool = False,
):
    if sound:
        _play_alert_chime()
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
    from PySide6.QtGui import (
        QPainter, QColor, QFont, QPen, QBrush, QPainterPath,
        QLinearGradient, QCursor
    )

    class CompactDynamicIslandToast(QWidget):
        def __init__(self):
            super().__init__()
            self.title = title
            self.body = body
            self.temp_level = temp_level or _extract_temp_str(body) or _extract_temp_str(title) or "HOT"
            self.duration_ms = int(duration_sec * 1000)

            # Notification overlay flags (never steal focus, never appear on taskbar or alt-tab)
            self.setWindowFlags(
                Qt.FramelessWindowHint
                | Qt.WindowStaysOnTopHint
                | Qt.WindowDoesNotAcceptFocus
                | Qt.BypassWindowManagerHint
                | Qt.ToolTip
            )
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.setAttribute(Qt.WA_ShowWithoutActivating, True)
            self.setFocusPolicy(Qt.NoFocus)
            self.setCursor(QCursor(Qt.PointingHandCursor))

            # Compact size: 275px width, 44px height
            self.full_w = 275
            self.full_h = 44
            self.initial_w = 90
            self.initial_h = 24

            screen = QApplication.primaryScreen().geometry()
            self.center_x = (screen.width() - self.full_w) // 2
            # Position cleanly below top panel (26px panel -> y=34 gives 8px margin)
            self.top_y = 34

            start_x = (screen.width() - self.initial_w) // 2
            self.setGeometry(start_x, self.top_y, self.initial_w, self.initial_h)

            # In-animation: emoji shakes left-to-right for 500ms
            self.shake_time = 0.0
            self.shake_duration = 0.5
            self.shake_offset = 0.0
            self.shake_active = True

            self.anim_timer = QTimer(self)
            self.anim_timer.timeout.connect(self._on_tick)
            self.anim_timer.start(25)

            # Smooth compact pop-in
            self.expand_anim = QPropertyAnimation(self, b"geometry")
            self.expand_anim.setDuration(320)
            self.expand_anim.setStartValue(QRect(start_x, self.top_y, self.initial_w, self.initial_h))
            self.expand_anim.setEndValue(QRect(self.center_x, self.top_y, self.full_w, self.full_h))
            self.expand_anim.setEasingCurve(QEasingCurve.OutBack)
            self.expand_anim.start()

            # Auto-dismiss timer (warnings auto-dismiss, critical duration_ms <= 0 stays until clicked)
            if self.duration_ms > 0:
                self.dismiss_timer = QTimer(self)
                self.dismiss_timer.setSingleShot(True)
                self.dismiss_timer.timeout.connect(self._close_animated)
                self.dismiss_timer.start(self.duration_ms)

            self.closing = False

        def _on_tick(self):
            if self.shake_active:
                self.shake_time += 0.025
                if self.shake_time <= self.shake_duration:
                    progress = self.shake_time / self.shake_duration
                    decay = 1.0 - progress
                    freq = 8.0  # oscillation cycles
                    self.shake_offset = math.sin(self.shake_time * 2 * math.pi * freq) * 5.0 * decay
                else:
                    self.shake_offset = 0.0
                    self.shake_active = False

            self.update()

        def _close_animated(self):
            if self.closing:
                return
            self.closing = True
            self.anim_timer.stop()

            screen = QApplication.primaryScreen().geometry()
            start_x = (screen.width() - self.initial_w) // 2

            self.shrink_anim = QPropertyAnimation(self, b"geometry")
            self.shrink_anim.setDuration(240)
            self.shrink_anim.setStartValue(self.geometry())
            self.shrink_anim.setEndValue(QRect(start_x, self.top_y, self.initial_w, self.initial_h))
            self.shrink_anim.setEasingCurve(QEasingCurve.InBack)
            self.shrink_anim.finished.connect(self._quit_app)
            self.shrink_anim.start()

        def _quit_app(self):
            self.close()
            QApplication.instance().quit()

        def mousePressEvent(self, event):
            self._close_animated()

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.TextAntialiasing)

            w = self.width()
            h = self.height()
            r = h / 2.0

            # ── 1. Compact Pill Container ──
            pill_path = QPainterPath()
            pill_path.addRoundedRect(1, 1, w - 2, h - 2, r, r)

            # Deep Obsidian Black Fill
            painter.fillPath(pill_path, QColor(8, 8, 10, 250))

            # Subtle Glowing Red Border
            border_pen = QPen(QColor(239, 68, 68, 150), 1.2)
            painter.setPen(border_pen)
            painter.drawPath(pill_path)

            if w < 160:
                return

            # ── 2. Single Firework Emoji with Left-to-Right Shake ──
            emoji_x = 10.0 + self.shake_offset
            font_emoji = QFont("Noto Color Emoji, Segoe UI Emoji, Apple Color Emoji", 16)
            painter.setFont(font_emoji)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(QRect(int(emoji_x), 0, 32, h), Qt.AlignCenter, "🔥")

            # ── 3. Red Temperature Pill Badge (Right) ──
            badge_w = 64
            badge_h = 26
            badge_x = w - badge_w - 9
            badge_y = (h - badge_h) // 2
            badge_r = badge_h / 2.0

            badge_path = QPainterPath()
            badge_path.addRoundedRect(badge_x, badge_y, badge_w, badge_h, badge_r, badge_r)

            badge_grad = QLinearGradient(badge_x, badge_y, badge_x, badge_y + badge_h)
            badge_grad.setColorAt(0.0, QColor(248, 113, 113))
            badge_grad.setColorAt(1.0, QColor(220, 38, 38))
            painter.fillPath(badge_path, badge_grad)

            font_temp = QFont("DejaVu Sans, Inter, Segoe UI", 10, QFont.Bold)
            painter.setFont(font_temp)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(QRect(badge_x, badge_y, badge_w, badge_h), Qt.AlignCenter, self.temp_level)

            # ── 4. Compact Title & Sensor Label (Center) ──
            text_x = 45
            text_w = badge_x - text_x - 6

            font_title = QFont("DejaVu Sans, Inter, Segoe UI", 9, QFont.Bold)
            painter.setFont(font_title)
            painter.setPen(QColor(250, 250, 250))
            title_text = "High Temp" if "warning" in self.title.lower() or "high" in self.title.lower() else self.title
            painter.drawText(QRect(text_x, 6, text_w, 16), Qt.AlignLeft | Qt.AlignVCenter, title_text)

            font_body = QFont("DejaVu Sans, Inter, Segoe UI", 8)
            painter.setFont(font_body)
            painter.setPen(QColor(156, 163, 175))
            clean_body = self.body.split(":")[0].strip() if ":" in self.body else self.body
            painter.drawText(QRect(text_x, 22, text_w, 16), Qt.AlignLeft | Qt.AlignVCenter, clean_body)

    app = QApplication.instance() or QApplication(sys.argv)
    toast_win = CompactDynamicIslandToast()
    toast_win.show()
    sys.exit(app.exec())


def _try_launch_dynamic_island(
    module_name: str,
    title: str,
    body: str,
    temp_level: str | None,
    icon_text: str,
    duration_sec: float,
    accent_color: str,
    sound: bool = False,
) -> bool:
    try:
        import PySide6
        cmd = [
            sys.executable,
            os.path.abspath(__file__),
            "--dynamic-island",
            "--title", title,
            "--body", body,
            "--temp", temp_level or "",
            "--icon", "🔥",
            "--duration", str(duration_sec),
            "--accent", accent_color or "#ef4444",
        ]
        if sound:
            cmd.append("--sound")
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def show_toast(
    module_name: str,
    title: str,
    body: str = "",
    *,
    icon_text: str = "",
    position: str | None = None,
    bg_color: str | None = None,
    text_color: str | None = None,
    accent_color: str | None = None,
    duration_sec: int | None = None,
    animation: str | None = None,
    temp_level: str | None = None,
    style: str | None = None,
    sound: bool = False,
) -> None:
    config = _load_toast_config(module_name)
    resolved_duration = duration_sec if duration_sec is not None else config.get("duration_sec", 4)
    resolved_accent = accent_color or config.get("accent_color", "#ef4444")

    should_use_island = (
        style == "dynamic_island"
        or config.get("style") == "dynamic_island"
        or module_name == "TempMonitor"
        or temp_level is not None
        or bool(_extract_temp_str(body))
    )

    if should_use_island:
        extracted_temp = temp_level or _extract_temp_str(body) or _extract_temp_str(title)
        if _try_launch_dynamic_island(
            module_name,
            title,
            body,
            extracted_temp,
            "🔥",
            resolved_duration,
            resolved_accent,
            sound=sound,
        ):
            return

    # Fallback to standard Tkinter toast
    def _run():
        tk_config = _resolve_colors(config)
        if position:
            tk_config["position"] = position
        if bg_color:
            tk_config["bg_color"] = bg_color
        if text_color:
            tk_config["text_color"] = text_color
        if accent_color:
            tk_config["accent_color"] = accent_color
        if duration_sec is not None:
            tk_config["duration_sec"] = duration_sec
        if animation:
            tk_config["animation"] = animation

        root = tk.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.0)
        root.configure(bg=tk_config["bg_color"])

        w = tk_config["width"]
        h = tk_config["height"]

        with _lock:
            stack_index = len(_active_toasts)
            _active_toasts.append(root)

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        target_x, target_y = _calculate_position(tk_config, screen_w, screen_h, stack_index)

        canvas = tk.Canvas(
            root, width=w, height=h,
            bg=tk_config["bg_color"], highlightthickness=0,
        )
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(
            0, 0, w, h, fill=tk_config["bg_color"], outline=tk_config["border_color"], width=1
        )

        icon_w = 48
        canvas.create_rectangle(
            0, 0, icon_w, h, fill=tk_config["accent_color"], outline=""
        )
        canvas.create_text(
            icon_w // 2, h // 2,
            text="🔥", fill="#ffffff",
            font=(tk_config["font_family"], 16, "bold"),
        )
        text_x = icon_w + tk_config["padding"]

        canvas.create_text(
            text_x, tk_config["padding"],
            text=title, fill=tk_config["text_color"],
            font=(tk_config["font_family"], tk_config["font_size_title"], "bold"),
            anchor="nw",
        )

        if body:
            canvas.create_text(
                text_x, tk_config["padding"] + tk_config["font_size_title"] + 8,
                text=body, fill=tk_config["text_color"],
                font=(tk_config["font_family"], tk_config["font_size_body"]),
                anchor="nw", width=w - text_x - tk_config["padding"],
            )

        canvas.bind("<Button-1>", lambda e: _fade_out(root))

        anim = tk_config["animation"]
        if anim == "slide":
            is_top = tk_config["position"].startswith("top")
            start_y = -h if is_top else screen_h
            root.geometry(f"{w}x{h}+{target_x}+{start_y}")
            root.deiconify()
            root.attributes("-alpha", 0.95)
            step = 4 if is_top else -4
            root.after(10, _slide_in, root, target_y, start_y, step)
        else:
            root.geometry(f"{w}x{h}+{target_x}+{target_y}")
            root.deiconify()
            root.attributes("-alpha", 0.0)
            _fade_in(root)

        root.update_idletasks()
        try:
            hwnd = (
                int(root.frame(), 16)
                if isinstance(root.frame(), str) and root.frame().startswith("0x")
                else int(root.frame())
            )
            apply_rounded_corners(hwnd)
        except (ValueError, TypeError, OSError):
            pass

        root.after(tk_config["duration_sec"] * 1000, lambda: _fade_out(root))
        root.mainloop()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AeroHub Toast Engine")
    parser.add_argument("--dynamic-island", action="store_true", help="Launch dynamic island toast")
    parser.add_argument("--title", type=str, default="Notice")
    parser.add_argument("--body", type=str, default="")
    parser.add_argument("--temp", type=str, default="")
    parser.add_argument("--icon", type=str, default="🔥")
    parser.add_argument("--duration", type=float, default=3.5)
    parser.add_argument("--accent", type=str, default="#ef4444")
    parser.add_argument("--sound", action="store_true", help="Play alert chime")

    args = parser.parse_args()

    if args.dynamic_island:
        _run_dynamic_island_process(
            args.title, args.body, args.temp, args.icon, args.duration, args.accent, args.sound
        )
    else:
        show_toast("TempMonitor", args.title, args.body, temp_level=args.temp, duration_sec=int(args.duration))
        time.sleep(args.duration + 1)
