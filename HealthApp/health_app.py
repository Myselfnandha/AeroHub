"""
Health App / Eye Break Reminder — Coordinates healthy work breaks.
Full-screen overlay lock, 8D breathing audio, weather-based display warmth,
and fully configurable break schedule via settings GUI.
"""

import os
import sys
import json
import time
import math
import struct
import wave
import threading
import logging
import logging.handlers
import datetime
import ctypes
import ctypes.wintypes
import tkinter as tk
from tkinter import ttk, colorchooser
import queue
import asyncio

try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    )
    WINSDK_AVAILABLE = True
except ImportError:
    WINSDK_AVAILABLE = False

import psutil
import requests

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow psutil requests")
    sys.exit(1)

try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(SCRIPT_DIR, "settings.json")
BREATHING_WAV = os.path.join(SCRIPT_DIR, "breathing_8d.wav")
LOGS_DIR = r"c:\Users\NANDHA A\Desktop\UTILITIES\Logs"
LOG_PATH = os.path.join(LOGS_DIR, "health_app.log")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCRIPT_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.HealthApp")
except Exception:
    pass

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("HealthApp")

# ── Theme ──
TH = {
    "bg": "#070b14",          # Deep space black
    "bg2": "#101625",         # Slightly lighter for panels
    "bg3": "#1a233a",         # Highlight panels
    "accent": "#00f0ff",      # Cyberpunk Neon Cyan
    "accent_hover": "#33f3ff",
    "fg": "#e2e8f0",          # Bright tech gray
    "fg_dim": "#64748b",      # Muted tech gray
    "success": "#00ff41",     # Matrix green
    "warning": "#ffb000",     # Warning orange
    "danger": "#ff2a2a",      # Neon Red
    "border": "#1e293b",      # Dark border
    "border_glow": "#0088aa"  # Accent border
}

# ── Media Key Constants ──
VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002


# ══════════════════════════════════════════════════════════
#  Media Control — Persistent Async Loop on Dedicated Thread
# ══════════════════════════════════════════════════════════
class MediaController:
    """Manages media pause/resume on a single dedicated COM+async thread.

    Fixes:
    - No more asyncio.run() per call (which creates/destroys event loops)
    - COM is initialized once on the dedicated thread
    - Stale session objects are never reused across calls
    - Each pause/resume fetches fresh sessions from the SessionManager
    - Deduplicates sessions by app_id to prevent flicker
    - Robust error handling per-session so one bad session doesn't crash all
    """

    def __init__(self):
        self._loop = None
        self._thread = None
        self._ready = threading.Event()
        self._paused_app_ids = []
        self._lock = threading.Lock()
        self._start_thread()

    def _start_thread(self):
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)

    def _run_loop(self):
        # Initialize COM as MTA once for the lifetime of this thread
        hr = ctypes.windll.ole32.CoInitializeEx(None, 2)
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._ready.set()
            self._loop.run_forever()
        finally:
            if hr in (0, 1):
                ctypes.windll.ole32.CoUninitialize()

    def _run_async(self, coro):
        """Schedule a coroutine on the dedicated loop and wait for result."""
        if not self._loop or not self._loop.is_running():
            return None
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout=10)
        except Exception as e:
            logger.error(f"MediaController async error: {e}")
            return None

    def pause_active_media(self):
        """Pause all currently PLAYING media sessions. Records app_ids to resume later."""
        with self._lock:
            self._paused_app_ids.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        paused_ids = self._run_async(self._do_pause())
        if paused_ids is None:
            # Async failed — fall back to global media key
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        with self._lock:
            self._paused_app_ids = paused_ids

        logger.info(f"Paused {len(paused_ids)} active media sessions via winsdk.")

    def resume_paused_media(self):
        """Resume only the media sessions that were paused before the break."""
        with self._lock:
            ids_to_resume = list(self._paused_app_ids)
            self._paused_app_ids.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        if not ids_to_resume:
            return

        count = self._run_async(self._do_resume(ids_to_resume))
        if count is None:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        logger.info(f"Resumed {count} media sessions via winsdk.")

    async def _do_pause(self):
        """Fetch fresh sessions and pause all that are Playing (status==4).

        Returns list of app_ids that were successfully paused.
        Deduplicates by app_id so Chrome with 2 tabs only gets paused once.
        """
        paused_ids = []
        seen_app_ids = set()

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""

                    # Deduplicate: only process first session per app
                    if app_id in seen_app_ids:
                        continue
                    seen_app_ids.add(app_id)

                    info = session.get_playback_info()
                    if not info:
                        continue

                    status = info.playback_status
                    if status != 4:  # Not Playing
                        continue

                    result = await session.try_pause_async()
                    if result:
                        paused_ids.append(app_id)
                    else:
                        # try_pause_async returned False — session may not support it
                        paused_ids.append(app_id)

                except Exception as e:
                    logger.debug(f"Error pausing session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager pause error: {e}")

        return paused_ids

    async def _do_resume(self, app_ids_to_resume):
        """Fetch fresh sessions and resume those whose app_id is in the list.

        Uses fresh session objects (never stale references).
        """
        resumed = 0
        target_ids = set(app_ids_to_resume)

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    if app_id not in target_ids:
                        continue

                    # Remove so we only resume once per app
                    target_ids.discard(app_id)

                    await session.try_play_async()
                    resumed += 1

                except Exception as e:
                    logger.debug(f"Error resuming session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager resume error: {e}")

        return resumed


def _send_media_key(vk_code: int):
    """Send a media key press/release via keybd_event (global fallback)."""
    try:
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(
            vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0
        )
        time.sleep(0.15)
    except Exception as e:
        logger.error(f"Media key send error: {e}")


# ── Singleton media controller ──
_media_controller = None


def get_media_controller():
    global _media_controller
    if _media_controller is None:
        _media_controller = MediaController()
    return _media_controller


def is_workstation_locked() -> bool:
    """Check if the Windows workstation is currently locked."""
    try:
        user32 = ctypes.windll.user32
        hDesktop = user32.OpenInputDesktop(0, False, 0x0100)
        if not hDesktop:
            return True
        user32.CloseDesktop(hDesktop)
        return False
    except Exception:
        return False


# ── Default Settings ──
DEFAULT_SETTINGS = {
    "short_break_interval_min": 20,
    "short_break_duration_sec": 15,
    "long_break_interval_min": 60,
    "long_break_duration_sec": 60,
    "pre_warning_sec": 30,
    "enable_sound": True,
    "enable_dimming": True,
    "enable_weather_warmth": True,
    "latitude": 13.08,
    "longitude": 80.27,
    "paused": False,
    "night_light_start_hour": 18,
    "night_light_end_hour": 6,
    "run_during_game": True,
    "toast_pos": "Center",
    "toast_width": 260,
    "toast_height": 60,
    "toast_bg_color": "#252525",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#7c3aed",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_emoji": "👁️",
    "toast_radius": 16,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#7c3aed",
}


# ══════════════════════════════════════════════════════════
#  Settings I/O
# ══════════════════════════════════════════════════════════
def load_settings() -> dict:
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**DEFAULT_SETTINGS, **saved}
    except Exception as e:
        logger.error(f"Settings load error: {e}")
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        logger.info("Settings saved.")
    except Exception as e:
        logger.error(f"Settings save error: {e}")


# ══════════════════════════════════════════════════════════
#  8D Breathing Sound Generation
# ══════════════════════════════════════════════════════════
def generate_breathing_sound(duration_sec: int = 65):
    """Generate a stereo WAV with breathing-like tones and 8D panning effect."""
    if os.path.exists(BREATHING_WAV):
        return

    logger.info("Generating 8D breathing sound...")
    sample_rate = 44100
    n_samples = sample_rate * duration_sec
    samples = []
    breath_cycle = 4.0
    freq_base = 220
    pan_speed = 0.15

    for i in range(n_samples):
        t = i / sample_rate
        breath_phase = (t % breath_cycle) / breath_cycle

        if breath_phase < 0.5:
            envelope = math.sin(breath_phase * math.pi)
        else:
            envelope = math.sin(breath_phase * math.pi) * 0.6

        envelope = max(0, envelope) * 0.35

        tone = (
            math.sin(2 * math.pi * freq_base * t) * 0.4
            + math.sin(2 * math.pi * freq_base * 1.5 * t) * 0.2
            + math.sin(2 * math.pi * freq_base * 2 * t) * 0.15
            + math.sin(2 * math.pi * freq_base * 0.5 * t) * 0.25
        )

        pan = math.sin(2 * math.pi * pan_speed * t)
        left_vol = math.sqrt(0.5 * (1 + pan))
        right_vol = math.sqrt(0.5 * (1 - pan))

        sample_val = tone * envelope
        left_sample = max(-32767, min(32767, int(sample_val * left_vol * 32767)))
        right_sample = max(-32767, min(32767, int(sample_val * right_vol * 32767)))

        samples.append(left_sample)
        samples.append(right_sample)

    with wave.open(BREATHING_WAV, "w") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(struct.pack(f"<{len(samples)}h", *samples))

    logger.info(f"8D breathing sound saved: {BREATHING_WAV}")


# ══════════════════════════════════════════════════════════
#  Weather & Color Temperature
# ══════════════════════════════════════════════════════════
def get_weather_info(lat: float, lon: float) -> dict:
    """Fetch current weather from Open-Meteo API."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true&daily=sunrise,sunset&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return {
            "temperature": data.get("current_weather", {}).get("temperature", 25),
            "is_day": data.get("current_weather", {}).get("is_day", 1),
            "sunrise": data.get("daily", {}).get("sunrise", [""])[0],
            "sunset": data.get("daily", {}).get("sunset", [""])[0],
        }
    except Exception as e:
        logger.error(f"Weather fetch error: {e}")
        settings = load_settings()
        start_hour = settings.get("night_light_start_hour", 18)
        end_hour = settings.get("night_light_end_hour", 6)
        is_day_local = 1 if not _is_night_hour(
            datetime.datetime.now().hour, start_hour, end_hour
        ) else 0
        return {"temperature": 25, "is_day": is_day_local, "sunrise": "", "sunset": ""}


def _is_night_hour(current_hour: int, start_hour: int, end_hour: int) -> bool:
    if start_hour > end_hour:
        return current_hour >= start_hour or current_hour < end_hour
    return start_hour <= current_hour < end_hour


def kelvin_to_rgb(kelvin: int) -> tuple:
    """Convert color temperature (Kelvin) to RGB."""
    temp = kelvin / 100.0

    if temp <= 66:
        red = 255
    else:
        red = max(0, min(255, 329.698727446 * ((temp - 60) ** -0.1332047592)))

    if temp <= 66:
        green = 99.4708025861 * math.log(temp) - 161.1195681661
    else:
        green = 288.1221695283 * ((temp - 60) ** -0.0755148492)
    green = max(0, min(255, green))

    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = max(0, min(255, 138.5177312231 * math.log(temp - 10) - 305.0447927307))

    return (int(red), int(green), int(blue))


def apply_gamma_ramp(kelvin: int, log_action: bool = True):
    """Apply color temperature via Windows gamma ramp."""
    try:
        r, g, b = kelvin_to_rgb(kelvin)
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0

        GammaArray = (ctypes.wintypes.WORD * 256 * 3)()
        for i in range(256):
            GammaArray[0][i] = int(min(65535, i * 256 * rf))
            GammaArray[1][i] = int(min(65535, i * 256 * gf))
            GammaArray[2][i] = int(min(65535, i * 256 * bf))

        hdc = ctypes.windll.user32.GetDC(None)

        CurrentGammaArray = (ctypes.wintypes.WORD * 256 * 3)()
        if ctypes.windll.gdi32.GetDeviceGammaRamp(hdc, ctypes.byref(CurrentGammaArray)):
            is_different = False
            for i in range(256):
                if (
                    abs(CurrentGammaArray[0][i] - GammaArray[0][i]) > 10
                    or abs(CurrentGammaArray[1][i] - GammaArray[1][i]) > 10
                    or abs(CurrentGammaArray[2][i] - GammaArray[2][i]) > 10
                ):
                    is_different = True
                    break

            if not is_different:
                ctypes.windll.user32.ReleaseDC(None, hdc)
                return

        ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(GammaArray))
        ctypes.windll.user32.ReleaseDC(None, hdc)
        if log_action:
            logger.info(f"Applied color temperature: {kelvin}K")
    except Exception as e:
        if log_action:
            logger.error(f"Gamma ramp error: {e}")


def reset_gamma_ramp():
    """Reset gamma ramp to default (6500K)."""
    apply_gamma_ramp(6500)


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


# ══════════════════════════════════════════════════════════
#  Break Audio Selection
# ══════════════════════════════════════════════════════════
def select_break_audio(settings: dict) -> str:
    """Select the break audio file based on settings."""
    audio_source = settings.get("break_audio_source", "default")
    ambient_dir = os.path.join(SCRIPT_DIR, "resources", "ambient")

    if audio_source == "default":
        return BREATHING_WAV

    if audio_source == "random":
        import random
        if os.path.exists(ambient_dir):
            files = [f for f in os.listdir(ambient_dir) if f.endswith((".mp3", ".wav"))]
            if files:
                return os.path.join(ambient_dir, random.choice(files))
        return BREATHING_WAV

    # Specific track name
    if os.path.exists(ambient_dir):
        for ext in [".mp3", ".wav"]:
            test_path = os.path.join(ambient_dir, f"{audio_source}{ext}")
            if os.path.exists(test_path):
                return test_path

    return BREATHING_WAV


# ══════════════════════════════════════════════════════════
#  Pre-break Warning Toast
# ══════════════════════════════════════════════════════════
class WarningToast:
    def __init__(self, parent, message: str, duration_sec: int, settings: dict):
        self.parent = parent
        self.message = message
        self.duration = duration_sec
        self.settings = settings
        self.closing = False

    def show(self):
        try:
            self._create_toast()
        except Exception:
            pass

    def _create_toast(self):
        toast = tk.Toplevel(self.parent)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        trans_color = "#010203"
        toast.configure(bg=trans_color)
        toast.attributes("-transparentcolor", trans_color)
        toast.attributes("-alpha", 0.0)

        tw = int(self.settings.get("toast_width", 260))
        th = int(self.settings.get("toast_height", 60))
        pos = self.settings.get("toast_pos", "Center").lower()
        bg_col = self.settings.get("toast_bg_color", "#252525")
        fg_col = self.settings.get("toast_fg_color", "#ffffff")
        font_size = int(self.settings.get("toast_font_size", 11))
        font_weight = self.settings.get("toast_font_weight", "bold")
        emoji = self.settings.get("toast_emoji", "👁️")
        radius = int(self.settings.get("toast_radius", 16))
        padx = int(self.settings.get("toast_padding_x", 12))
        pady = int(self.settings.get("toast_padding_y", 10))
        anim_style = self.settings.get("toast_anim_style", "Slide").lower()
        opacity = float(self.settings.get("toast_opacity", 0.92))
        border_width = int(self.settings.get("toast_border_width", 0))
        border_color = self.settings.get("toast_border_color", "#7c3aed")

        sw = toast.winfo_screenwidth()
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
            toast.geometry(f"{tw}x{th}+{final_x}+{final_y}")
        else:
            toast.geometry(f"{tw}x{th}+{start_x}+{start_y}")

        canvas = tk.Canvas(toast, width=tw, height=th, bg=trans_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        self._draw_toast_bg(canvas, tw, th, radius, bg_col, border_width, border_color)
        self._draw_toast_text(canvas, padx, pady, font_size, font_weight, emoji, fg_col)

        toast.update_idletasks()

        def close_toast(event=None):
            self.closing = True
            try:
                toast.destroy()
            except Exception:
                pass
                
        self.force_close = close_toast

        toast.bind("<Button-1>", close_toast)
        canvas.bind("<Button-1>", close_toast)

        self._animate_in(toast, tw, th, start_x, start_y, final_x, final_y, anim_style, opacity, close_toast)
        if self.duration > 0:
            self._play_pre_break_sound()

    def _draw_toast_bg(self, canvas, tw, th, radius, bg_col, border_width, border_color):
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

    def _draw_toast_text(self, canvas, padx, pady, font_size, font_weight, emoji, fg_col):
        msg_font = ("Segoe UI", font_size, font_weight)
        sub_font = ("Segoe UI", max(8, font_size - 2))

        canvas.create_text(
            padx + 10, pady, anchor=tk.NW,
            text=f"{emoji}  {self.message}",
            font=msg_font, fill=fg_col,
        )
        canvas.create_text(
            padx + 10, pady + font_size + 8, anchor=tk.NW,
            text=f"Break in {self.duration} seconds",
            font=sub_font, fill="#8892b0",
        )

    def _animate_in(self, toast, tw, th, sx, sy, fx, fy, anim_style, opacity, close_cb):
        def slide_in(step=0):
            if self.closing:
                return
            if step <= 20:
                p = step / 20
                ease = 1 - (1 - p) ** 3

                if anim_style == "fade":
                    toast.attributes("-alpha", min(opacity, ease * opacity))
                else:
                    cx = int(sx + (fx - sx) * ease)
                    cy = int(sy + (fy - sy) * ease)
                    try:
                        toast.geometry(f"{tw}x{th}+{cx}+{cy}")
                        toast.attributes("-alpha", min(opacity, ease * opacity))
                    except tk.TclError:
                        pass
                toast.after(16, lambda: slide_in(step + 1))
            else:
                if self.duration > 0:
                    toast.after(self.duration * 1000, close_cb)

        slide_in(0)

    def _play_pre_break_sound(self):
        if not self.settings.get("toast_enable_sound", True):
            return
        try:
            import winsound
            sound_path = os.path.join(SCRIPT_DIR, "resources", "on_pre_break.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════
#  Full-Screen Break Overlay
# ══════════════════════════════════════════════════════════
class BreakOverlay:
    """Full-screen black overlay on all monitors with countdown and breathing text."""

    def __init__(self, parent, duration_sec: int, break_type: str, settings: dict, on_complete):
        self.parent = parent
        self.duration = duration_sec
        self.break_type = break_type
        self.settings = settings
        self._remaining = duration_sec
        self._original_brightness = None
        self.status = "completed"
        self.on_complete = on_complete
        self._focus_fail_count = 0
        self._using_windowed_fallback = False

    def show(self):
        """Show the overlay (non-blocking call)."""
        try:
            self._dim_screen()
            self._pause_media()
            self._play_break_audio()
            self._create_overlay_window()
            self._start_countdown()
            self._start_focus_keeper()
        except Exception as e:
            logger.error(f"Break overlay error: {e}")
            self._restore()
            if self.on_complete:
                self.on_complete(self.status)

    def _dim_screen(self):
        if SBC_AVAILABLE and self.settings.get("enable_dimming"):
            try:
                self._original_brightness = sbc.get_brightness()
                logger.info("Physical brightness dimming bypassed.")
            except Exception as e:
                logger.error(f"Brightness query error: {e}")

    def _pause_media(self):
        get_media_controller().pause_active_media()
        logger.info("Executed pause for active media sessions.")

    def _play_break_audio(self):
        if not PYGAME_AVAILABLE or not self.settings.get("enable_sound"):
            return
        try:
            sound_file = select_break_audio(self.settings)
            logger.info(f"Loading break sound: {sound_file}")
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play(-1)
        except Exception as e:
            logger.error(f"Audio play error: {e}")

    def _create_overlay_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="black")
        self.window.overrideredirect(True)

        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.bind("<Escape>", lambda e: None)
        self.window.bind("<Alt-F4>", lambda e: None)

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        self.window.geometry(f"{sw}x{sh}+0+0")
        self.window.grab_set()

        self._build_overlay_ui()

    def _build_overlay_ui(self):
        main_frame = tk.Frame(self.window, bg="black")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        type_text = "☕ Short Break" if self.break_type == "short" else "🧘 Long Break"
        tk.Label(
            main_frame, text=type_text,
            font=("Segoe UI", 20), fg=TH["accent"], bg="black",
        ).pack(pady=(0, 20))

        self._countdown_var = tk.StringVar(value=str(self.duration))
        tk.Label(
            main_frame, textvariable=self._countdown_var,
            font=("Segoe UI Light", 96, "bold"), fg="white", bg="black",
        ).pack(pady=(0, 20))

        self._breathing_var = tk.StringVar(value="Breathe In...")
        self._breathing_label = tk.Label(
            main_frame, textvariable=self._breathing_var,
            font=("Segoe UI", 24), fg=TH["fg_dim"], bg="black",
        )
        self._breathing_label.pack(pady=(0, 10))

        btn_frame = tk.Frame(main_frame, bg="black")
        btn_frame.pack(pady=10)

        btn_skip = tk.Button(
            btn_frame, text="Skip ⏭", font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e", fg=TH["fg_dim"], relief=tk.FLAT, cursor="hand2",
            activebackground=TH["bg2"], activeforeground="white",
            padx=20, pady=8, command=self._skip_break,
        )
        btn_skip.pack(side=tk.LEFT, padx=10)

        btn_postpone = tk.Button(
            btn_frame, text="Postpone (2m) ⏰", font=("Segoe UI", 12, "bold"),
            bg=TH["accent"], fg="white", relief=tk.FLAT, cursor="hand2",
            activebackground=TH["accent_hover"], activeforeground="white",
            padx=20, pady=8, command=self._postpone_break,
        )
        btn_postpone.pack(side=tk.LEFT, padx=10)

        _add_hover(btn_skip, "#1a1a2e", TH["bg2"], TH["fg_dim"], "white")
        _add_hover(btn_postpone, TH["accent"], TH["accent_hover"])

        tk.Label(
            main_frame,
            text="Look away from the screen • Focus on something 20ft away",
            font=("Segoe UI", 12), fg="#444", bg="black",
        ).pack(pady=(20, 0))

    def _skip_break(self):
        self.status = "skipped"
        logger.info("Break skipped by user action.")
        self._cleanup()

    def _postpone_break(self):
        self.status = "postponed"
        logger.info("Break postponed by user action.")
        self._cleanup()

    def _start_countdown(self):
        self._remaining = self.duration
        self._tick_countdown()

    def _tick_countdown(self):
        if self._remaining > 0:
            try:
                self._countdown_var.set(str(self._remaining))

                cycle = (self.duration - self._remaining) % 8
                if cycle < 4:
                    self._breathing_var.set("Breathe In... 🌬️")
                    self._breathing_label.config(fg=TH["success"])
                else:
                    self._breathing_var.set("Breathe Out... 💨")
                    self._breathing_label.config(fg=TH["accent"])

                self._remaining -= 1
                self.window.after(1000, self._tick_countdown)
            except tk.TclError:
                pass
        else:
            self._cleanup()

    def _start_focus_keeper(self):
        self._keep_on_top()

    def _keep_on_top(self):
        if not hasattr(self, "window") or not self.window.winfo_exists():
            return
        try:
            if self.window.state() == "iconic":
                self.window.deiconify()

            self.window.lift()
            self.window.attributes("-topmost", True)

            if self.window.focus_displayof() is None:
                self._focus_fail_count += 1
                if self._focus_fail_count >= 5 and not self._using_windowed_fallback:
                    logger.warning("Focus repeatedly lost. Applying windowed borderless fallback...")
                    try:
                        self.window.attributes("-fullscreen", False)
                        self.window.overrideredirect(True)
                        sw = self.window.winfo_screenwidth()
                        sh = self.window.winfo_screenheight()
                        self.window.geometry(f"{sw}x{sh}+0+0")
                        self._using_windowed_fallback = True
                    except Exception as ex:
                        logger.error(f"Failed to apply borderless fallback: {ex}")

                self.window.focus_force()
                try:
                    self.window.grab_set()
                except Exception:
                    pass
            else:
                self._focus_fail_count = 0
        except Exception as e:
            logger.error(f"Keep on top error: {e}")

        self.window.after(500, self._keep_on_top)

    def _cleanup(self):
        """Clean up and restore system state."""
        try:
            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
            self.window.grab_release()
            self.window.destroy()

            if self.settings.get("enable_sound"):
                try:
                    import winsound
                    sound_path = os.path.join(SCRIPT_DIR, "resources", "on_stop_break.wav")
                    if os.path.exists(sound_path):
                        winsound.PlaySound(
                            sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
                        )
                except Exception as e:
                    logger.error(f"Stop break sound play error: {e}")
        except Exception as e:
            logger.error(f"Error in overlay cleanup: {e}")

        self._restore()

        # Resume media on a short delay so the stop-break sound plays first
        time.sleep(0.3)
        get_media_controller().resume_paused_media()
        logger.info("Executed resume for paused media sessions.")

        if self.on_complete:
            self.on_complete(self.status)

    def _restore(self):
        """Restore brightness (bypassed per request)."""
        if SBC_AVAILABLE and self._original_brightness:
            try:
                logger.info("Physical brightness restore bypassed.")
            except Exception as e:
                logger.error(f"Brightness restore error: {e}")


# ══════════════════════════════════════════════════════════
#  Hover Helper
# ══════════════════════════════════════════════════════════
def _add_hover(btn, normal_bg, hover_bg, normal_fg=None, hover_fg=None):
    def on_enter(e):
        btn.config(bg=hover_bg)
        if hover_fg:
            btn.config(fg=hover_fg)

    def on_leave(e):
        btn.config(bg=normal_bg)
        if normal_fg:
            btn.config(fg=normal_fg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


# ══════════════════════════════════════════════════════════
#  Settings GUI
# ══════════════════════════════════════════════════════════
class SettingsWindow:
    def __init__(self, parent, settings: dict, on_save):
        self.parent = parent
        self.settings = settings
        self.on_save = on_save
        self.entries = {}

    def show(self):
        self._create()

    def _create(self):
        root = tk.Toplevel(self.parent)
        root.title("SYSTEM OVERRIDE // HEALTH CONFIG")
        root.configure(bg=TH["bg"])
        root.resizable(False, False)
        root.grab_set()

        try:
            apply_dwm_rounding(root)
        except Exception:
            pass

        def on_closing():
            if hasattr(self, 'preview_instance') and self.preview_instance and hasattr(self.preview_instance, 'force_close'):
                self.preview_instance.force_close()
            root.grab_release()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Main Layout: Sidebar (Left) and Content (Right)
        main_container = tk.Frame(root, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Title in Sidebar
        tk.Label(self.sidebar, text="HEALTH.SYS", font=("Consolas", 18, "bold"), bg=TH["bg2"], fg=TH["accent"]).pack(pady=(30, 40))

        # Content Area
        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frames = {}
        
        # Build Frames
        f_sched = tk.Frame(self.content_area, bg=TH["bg"])
        f_toast = tk.Frame(self.content_area, bg=TH["bg"])
        
        self.frames["Schedule"] = f_sched
        self.frames["Toast FX"] = f_toast

        self._build_schedule_tab(f_sched)
        self._build_toast_tab(f_toast)
        
        self.current_frame = None
        self.nav_buttons = {}

        def switch_tab(name):
            if self.current_frame:
                self.current_frame.pack_forget()
                self.nav_buttons[self.current_frame_name].config(bg=TH["bg2"], fg=TH["fg_dim"])
            
            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
            self.nav_buttons[name].config(bg=TH["bg3"], fg=TH["accent"])

        # Navigation Buttons
        for name in ["Schedule", "Toast FX"]:
            btn = tk.Button(
                self.sidebar, text=f"■ {name.upper()}", font=("Consolas", 11, "bold"),
                bg=TH["bg2"], fg=TH["fg_dim"], activebackground=TH["bg3"], activeforeground=TH["accent"],
                relief=tk.FLAT, cursor="hand2", anchor="w", padx=24, pady=12,
                command=lambda n=name: switch_tab(n)
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

        # Save Button in Sidebar (Bottom)
        tk.Button(
            self.sidebar, text="[ SAVE_CFG ]", font=("Consolas", 12, "bold"),
            bg=TH["accent"], fg=TH["bg"], activebackground=TH["accent_hover"], activeforeground=TH["bg"],
            relief=tk.FLAT, cursor="hand2", pady=12,
            command=lambda: self._save_and_close(root)
        ).pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=24)

        # Init First Tab
        switch_tab("Schedule")

        root.update_idletasks()
        root.geometry("900x650")

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame, text=label.upper(), font=("Consolas", 9),
            bg=TH["bg"], fg=TH["fg_dim"], anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)

        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(
            parent_frame, textvariable=var, font=("Consolas", 10),
            bg=TH["bg"], fg=TH["fg"], insertbackground=TH["accent"],
            relief=tk.FLAT, highlightthickness=1,
            highlightcolor=TH["accent"], highlightbackground=TH["border"],
            width=14,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))

        self.entries[key] = (var, is_str)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame, text=label.upper(), font=("Consolas", 9),
            bg=TH["bg"], fg=TH["fg_dim"], anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)

        var = tk.StringVar(value=self.settings.get(key, values[0]))
        ttk.Combobox(
            parent_frame, textvariable=var, values=values,
            font=("Consolas", 10), state="readonly", width=12,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))

        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame, text=label.upper(), font=("Consolas", 9),
            bg=TH["bg"], fg=TH["fg_dim"], anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)

        var = tk.StringVar(value=str(self.settings.get(key, "")))
        
        def choose_color(v=var):
            color_code = colorchooser.askcolor(title="Choose color", initialcolor=v.get())[1]
            if color_code:
                v.set(color_code)
                btn.config(bg=color_code)
                
        btn = tk.Button(
            parent_frame, bg=var.get(), width=10, relief=tk.FLAT,
            cursor="hand2", command=choose_color
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))

        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_chk(self, parent, label, key):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent, text=label.upper(), variable=var,
            font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"],
            selectcolor=TH["bg2"], activebackground=TH["bg"], activeforeground=TH["accent"],
        ).pack(anchor=tk.W, pady=2)
        self.entries[key] = (var, "bool")
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_grid_chk(self, parent_frame, label, key, row):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent_frame, text=label.upper(), variable=var,
            font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"],
            selectcolor=TH["bg2"], activebackground=TH["bg"], activeforeground=TH["accent"],
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)
        self.entries[key] = (var, "bool")
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _build_schedule_tab(self, tab):
        tk.Label(tab, text="SYSTEM PARAMETERS", font=("Consolas", 14, "bold"), bg=TH["bg"], fg=TH["fg"]).pack(anchor=tk.W, pady=(0, 20))
        
        # We will split it into two columns or just standard grid
        f1 = tk.Frame(tab, bg=TH["bg"])
        f1.pack(fill=tk.X)

        self._add_field(f1, "Short break interval (min):", "short_break_interval_min", 0)
        self._add_field(f1, "Short break duration (sec):", "short_break_duration_sec", 1)
        self._add_field(f1, "Long break interval (min):", "long_break_interval_min", 2)
        self._add_field(f1, "Long break duration (sec):", "long_break_duration_sec", 3)
        self._add_field(f1, "Pre-warning (sec):", "pre_warning_sec", 4)
        self._add_field(f1, "Latitude:", "latitude", 5)
        self._add_field(f1, "Longitude:", "longitude", 6)

        audio_sources = ["default", "random", "campfire", "forest", "night", "ocean", "rain", "waterfall"]
        self._add_combo(f1, "Break Audio Source:", "break_audio_source", 7, audio_sources)
        self._add_field(f1, "Night light start hr (0-23):", "night_light_start_hour", 8)
        self._add_field(f1, "Night light end hr (0-23):", "night_light_end_hour", 9)

        tk.Label(tab, text="MODULES", font=("Consolas", 14, "bold"), bg=TH["bg"], fg=TH["fg"]).pack(anchor=tk.W, pady=(30, 10))

        chk_frame = tk.Frame(tab, bg=TH["bg"])
        chk_frame.pack(fill=tk.X)

        self._add_chk(chk_frame, "Enable breathing sound", "enable_sound")
        self._add_chk(chk_frame, "Dim screen during breaks", "enable_dimming")
        self._add_chk(chk_frame, "Weather-based color temp", "enable_weather_warmth")
        self._add_chk(chk_frame, "Run breaks during games", "run_during_game")

    def _build_toast_tab(self, tab):
        tk.Label(tab, text="UI / UX CONFIG", font=("Consolas", 14, "bold"), bg=TH["bg"], fg=TH["fg"]).pack(anchor=tk.W, pady=(0, 10))
        
        # Grid frame and Preview frame
        f_top = tk.Frame(tab, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        
        # Need two columns of inputs for toast to save vertical space
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        f2_right = tk.Frame(f_top, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        self._add_combo(f2_left, "Position:", "toast_pos", 0, ["Left", "Center", "Right"])
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, ["Slide", "Fade"])
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_color_field(f2_left, "Background Color:", "toast_bg_color", 4)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 5)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 6)
        self._add_combo(f2_left, "Font Weight:", "toast_font_weight", 7, ["normal", "bold"])
        
        self._add_field(f2_right, "Emoji Icon:", "toast_emoji", 0, is_str=True)
        self._add_field(f2_right, "Border Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X (px):", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y (px):", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity (0.1 - 1.0):", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width (px):", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_grid_chk(f2_right, "Play Warning Sound", "toast_enable_sound", 7)

        btn_frame = tk.Frame(tab, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(
            btn_frame, text="[ PREVIEW_UI ]", font=("Consolas", 10, "bold"),
            bg=TH["bg2"], fg=TH["accent"], activebackground=TH["bg3"], activeforeground=TH["accent"],
            relief=tk.FLAT, cursor="hand2",
            command=self._preview_toast, padx=20, pady=8,
        ).pack(side=tk.RIGHT)

    def _schedule_preview(self):
        if hasattr(self, '_preview_timer') and self._preview_timer:
            try:
                self.parent.after_cancel(self._preview_timer)
            except Exception:
                pass
        self._preview_timer = self.parent.after(400, self._preview_toast)

    def _preview_toast(self):
        if hasattr(self, 'preview_instance') and self.preview_instance and hasattr(self.preview_instance, 'force_close'):
            self.preview_instance.force_close()
            
        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = (val == "1" or val == "True" or val is True)
                elif key in ("latitude", "longitude", "toast_opacity"):
                    temp_settings[key] = float(val)
                elif var_type is False: # int
                    temp_settings[key] = int(val)
                else: # string (when var_type is True)
                    temp_settings[key] = val
            except ValueError:
                pass
                
        # Use duration=0 for infinite preview
        self.preview_instance = WarningToast(self.parent, "SIMULATED OVERLOAD", 0, temp_settings)
        self.preview_instance.show()

    def _save_and_close(self, root):
        if hasattr(self, 'preview_instance') and self.preview_instance and hasattr(self.preview_instance, 'force_close'):
            self.preview_instance.force_close()
            
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type is True or var_type == "bool":
                    self.settings[key] = val
                elif key in ("latitude", "longitude", "toast_opacity"):
                    self.settings[key] = float(val)
                else:
                    self.settings[key] = int(val)
            except ValueError:
                pass

        save_settings(self.settings)
        self.on_save(self.settings)
        root.grab_release()
        root.destroy()

# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
def create_health_icon(paused: bool = False) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg_color = (100, 100, 100, 200) if paused else (124, 58, 237, 230)
    draw.ellipse([4, 4, 60, 60], fill=bg_color)

    draw.ellipse([16, 22, 48, 42], outline=(255, 255, 255, 220), width=2)
    draw.ellipse([26, 26, 38, 38], fill=(255, 255, 255, 220))

    if paused:
        draw.line([12, 12, 52, 52], fill=(255, 100, 100, 200), width=3)

    return img


# ══════════════════════════════════════════════════════════
#  Main Health App
# ══════════════════════════════════════════════════════════
class HealthApp:
    POSTPONE_SECONDS = 120
    GRACE_PERIOD_SECONDS = 15 * 60

    def __init__(self):
        self.settings = load_settings()
        self.tray_icon = None
        self._running = True
        self._paused = self.settings.get("paused", False)
        self._skip_next = False
        self._last_short_break = time.time()
        self._last_long_break = time.time()
        self._game_mode = False
        self._current_kelvin = 6500
        self._last_gamma_apply = 0
        self._short_warn_shown = False
        self._long_warn_shown = False
        self.gui_queue = queue.Queue()

    def _set_self_priority(self, level: str):
        try:
            p = psutil.Process()
            if level == "idle":
                p.nice(psutil.IDLE_PRIORITY_CLASS)
            elif level == "normal":
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            logger.info(f"[PRIORITY] Set self priority to {level.upper()}")
        except Exception as e:
            logger.warning(f"Failed to set self priority to {level}: {e}")

    def _take_break(self, break_type: str = "short"):
        if self._game_mode:
            self._set_self_priority("normal")

        duration = self.settings[
            "short_break_duration_sec" if break_type == "short" else "long_break_duration_sec"
        ]
        logger.info(f"Starting {break_type} break ({duration}s)")

        completion_event = threading.Event()
        result = {}
        self.gui_queue.put(("break", (break_type, duration, completion_event, result)))
        completion_event.wait()

        status = result.get("status", "completed")
        self._handle_break_result(break_type, status)

        if self._game_mode:
            self._set_self_priority("idle")

    def _handle_break_result(self, break_type: str, status: str):
        now = time.time()

        if status == "postponed":
            logger.info(f"{break_type.title()} break postponed by 2 minutes.")
            self._postpone_timers(break_type, now)
        else:
            logger.info(f"{break_type.title()} break {status}.")
            self._reset_timers_after_break(break_type, now)

    def _postpone_timers(self, break_type: str, now: float):
        short_interval = self.settings["short_break_interval_min"] * 60
        self._last_short_break = now - (short_interval - self.POSTPONE_SECONDS)
        self._short_warn_shown = False

        if break_type == "long":
            long_interval = self.settings["long_break_interval_min"] * 60
            self._last_long_break = now - (long_interval - self.POSTPONE_SECONDS)
            self._long_warn_shown = False

    def _reset_timers_after_break(self, break_type: str, now: float):
        if break_type == "short":
            self._last_short_break = now
            self._short_warn_shown = False
        else:
            self._last_long_break = now
            self._last_short_break = now
            self._long_warn_shown = False
            self._short_warn_shown = False

    def _scheduler_loop(self):
        """Background thread: schedule breaks based on configured intervals."""
        logger.info("Break scheduler started.")
        last_weather_check = 0

        while self._running:
            try:
                now = time.time()

                self._maybe_update_weather(now, last_weather_check)
                if not self._game_mode and self.settings.get("enable_weather_warmth") and now - last_weather_check > 1800:
                    last_weather_check = now

                self._maybe_reapply_gamma(now)

                if self._paused:
                    time.sleep(1)
                    self._last_short_break += 1
                    self._last_long_break += 1
                    continue

                if self._game_mode and not self.settings.get("run_during_game", True):
                    self._handle_game_mode_postpone(now)
                    time.sleep(5)
                    continue

                if self._handle_lock_screen(now):
                    continue

                self._check_and_trigger_breaks(now)

            except Exception as e:
                logger.error(f"Scheduler error: {e}")

            time.sleep(1)

    def _maybe_update_weather(self, now: float, last_check: float):
        if (
            not self._game_mode
            and self.settings.get("enable_weather_warmth")
            and now - last_check > 1800
        ):
            threading.Thread(target=self._update_color_temp, daemon=True).start()

    def _maybe_reapply_gamma(self, now: float):
        if (
            not self._game_mode
            and self.settings.get("enable_weather_warmth")
            and now - self._last_gamma_apply > 5
        ):
            self._last_gamma_apply = now
            apply_gamma_ramp(self._current_kelvin, log_action=False)

    def _handle_game_mode_postpone(self, now: float):
        short_interval = self.settings["short_break_interval_min"] * 60
        long_interval = self.settings["long_break_interval_min"] * 60
        elapsed_long = now - self._last_long_break
        elapsed_short = now - self._last_short_break

        if elapsed_long >= long_interval:
            self._last_long_break = now - long_interval + self.POSTPONE_SECONDS
            logger.info("[GAME MODE] Auto-postponing long break by 2 minutes (AeroEco).")
        elif elapsed_short >= short_interval:
            self._last_short_break = now - short_interval + self.POSTPONE_SECONDS
            logger.info("[GAME MODE] Auto-postponing short break by 2 minutes (AeroEco).")

    def _handle_lock_screen(self, now: float) -> bool:
        was_locked = False
        while self._running and is_workstation_locked():
            was_locked = True
            time.sleep(1)

        if not was_locked:
            return False

        now = time.time()
        short_interval = self.settings["short_break_interval_min"] * 60
        long_interval = self.settings["long_break_interval_min"] * 60

        self._last_short_break = max(
            self._last_short_break, now - short_interval + self.GRACE_PERIOD_SECONDS
        )
        self._last_long_break = max(
            self._last_long_break, now - long_interval + self.GRACE_PERIOD_SECONDS
        )

        next_short_min = max(0.0, (self._last_short_break + short_interval - now) / 60)
        next_long_min = max(0.0, (self._last_long_break + long_interval - now) / 60)
        logger.info(
            f"Screen unlocked. Next short break in {next_short_min:.1f} mins, "
            f"next long break in {next_long_min:.1f} mins."
        )
        return True

    def _check_and_trigger_breaks(self, now: float):
        short_interval = self.settings["short_break_interval_min"] * 60
        long_interval = self.settings["long_break_interval_min"] * 60
        pre_warn = self.settings["pre_warning_sec"]

        elapsed_short = now - self._last_short_break
        elapsed_long = now - self._last_long_break

        # Long break has priority
        if elapsed_long >= long_interval:
            if self._skip_next:
                self._skip_next = False
                self._last_long_break = now
                self._last_short_break = now
                logger.info("Skipped long break.")
            else:
                self._take_break("long")
            self._long_warn_shown = False
            self._short_warn_shown = False
            return

        if elapsed_long >= long_interval - pre_warn:
            if not self._long_warn_shown:
                if self._game_mode:
                    self._set_self_priority("normal")
                self.gui_queue.put(("warning", (f"Long break in {pre_warn} seconds", pre_warn)))
                self._long_warn_shown = True
            return

        # Short break (only if long break pre-warning is NOT active)
        if elapsed_short >= short_interval:
            if self._skip_next:
                self._skip_next = False
                self._last_short_break = now
                logger.info("Skipped short break.")
            else:
                self._take_break("short")
            self._short_warn_shown = False
            return

        if elapsed_short >= short_interval - pre_warn:
            if not self._short_warn_shown:
                if self._game_mode:
                    self._set_self_priority("normal")
                self.gui_queue.put(("warning", (f"Short break in {pre_warn} seconds", pre_warn)))
                self._short_warn_shown = True

    def _update_color_temp(self):
        current_hour = datetime.datetime.now().hour
        start_hour = self.settings.get("night_light_start_hour", 18)
        end_hour = self.settings.get("night_light_end_hour", 6)

        is_night = _is_night_hour(current_hour, start_hour, end_hour)
        is_day = not is_night
        kelvin = 6500 if is_day else 3500

        try:
            lat = self.settings.get("latitude", 13.08)
            lon = self.settings.get("longitude", 80.27)
            weather = get_weather_info(lat, lon)

            if abs(lat - 13.08) > 0.01 or abs(lon - 80.27) > 0.01:
                is_day = bool(weather.get("is_day", is_day))
                kelvin = 6500 if is_day else 3500

            outdoor_temp = weather.get("temperature", 25)
            if outdoor_temp < 10:
                kelvin = min(kelvin, 3200)
            elif outdoor_temp > 35:
                kelvin = max(kelvin, 5500)

        except Exception as e:
            logger.error(f"Color temp update error: {e}")

        self._current_kelvin = kelvin
        apply_gamma_ramp(kelvin, log_action=True)

    def _on_settings_saved(self, new_settings):
        self.settings = new_settings
        logger.info("Settings updated from GUI.")
        threading.Thread(target=self._update_color_temp, daemon=True).start()

    def _on_take_break(self, icon, item):
        threading.Thread(target=lambda: self._take_break("short"), daemon=True).start()

    def _on_skip(self, icon, item):
        self._skip_next = True
        logger.info("Next break will be skipped.")

    def _on_settings(self, icon, item):
        self.gui_queue.put(("settings", None))

    def _on_pause_resume(self, icon, item):
        self._paused = not self._paused
        logger.info(f"{'Paused' if self._paused else 'Resumed'}")
        if self.tray_icon:
            self.tray_icon.icon = create_health_icon(self._paused)

    def _on_quit(self, icon, item):
        logger.info("Health App shutting down.")
        self._running = False
        reset_gamma_ramp()
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.quit()
            except Exception:
                pass
        icon.stop()
        os._exit(0)

    def _start_udp_listener(self):
        import socket

        def _listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", 5098))
            except Exception as e:
                logger.error(f"Failed to bind HealthApp UDP socket: {e}")
                return

            logger.info("HealthApp UDP Listener bound to 127.0.0.1:5098")
            while self._running:
                try:
                    data, addr = sock.recvfrom(1024)
                    msg = data.decode("utf-8").strip()
                    if msg == "game_mode:on" and not self._game_mode:
                        logger.info("[UDP] Game Mode activated. Shifting to low-resource mode...")
                        self._game_mode = True
                        self._set_self_priority("idle")
                    elif msg == "game_mode:off" and self._game_mode:
                        logger.info("[UDP] Game Mode deactivated. Restoring normal mode...")
                        self._game_mode = False
                        self._set_self_priority("normal")
                except Exception as e:
                    logger.error(f"Error in UDP listener: {e}")

            try:
                sock.close()
            except Exception:
                pass

        threading.Thread(target=_listen, daemon=True).start()

    def _process_gui_queue(self):
        while not self.gui_queue.empty():
            try:
                action, data = self.gui_queue.get_nowait()
                if action == "settings":
                    SettingsWindow(self.root, dict(self.settings), self._on_settings_saved).show()
                elif action == "warning":
                    msg, duration = data
                    WarningToast(self.root, msg, duration, self.settings).show()
                elif action == "break":
                    break_type, duration, completion_event, result = data

                    def on_overlay_complete(status):
                        result["status"] = status
                        completion_event.set()

                    BreakOverlay(
                        self.root, duration, break_type, self.settings, on_overlay_complete
                    ).show()
            except Exception as e:
                logger.error(f"Error processing GUI queue: {e}")

        if self._running:
            self.root.after(100, self._process_gui_queue)

    def run(self):
        logger.info("=" * 50)
        logger.info("Health App starting...")
        self._start_udp_listener()
        logger.info(f"Settings: {json.dumps(self.settings, indent=2)}")

        generate_breathing_sound()

        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot
        logger.info(f"System uptime: {uptime}")

        # Initialize the media controller early
        get_media_controller()

        icon_image = create_health_icon(self._paused)
        self.tray_icon = pystray.Icon(
            name="HealthApp",
            icon=icon_image,
            title="Health App — Eye Break Reminder",
            menu=pystray.Menu(
                pystray.MenuItem("👁️ Take Break Now", self._on_take_break),
                pystray.MenuItem("⏭ Skip Next Break", self._on_skip),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("⚙️ Settings", self._on_settings),
                pystray.MenuItem(
                    lambda item: "▶ Resume" if self._paused else "⏸ Pause",
                    self._on_pause_resume,
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )

        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        scheduler_thread.start()

        logger.info("Tray icon running detached.")
        self.tray_icon.run_detached()

        self.root = tk.Tk()
        self.root.withdraw()

        self._process_gui_queue()
        self.root.mainloop()


if __name__ == "__main__":
    is_debug_break = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "/debug:break screen":
            is_debug_break = True
        elif len(sys.argv) > 2 and sys.argv[1] == "/debug:break" and sys.argv[2] == "screen":
            is_debug_break = True

    if is_debug_break:
        generate_breathing_sound()

        root = tk.Tk()
        root.withdraw()
        settings = load_settings()

        def on_complete(status):
            print(f"Break completed with status: {status}")
            root.destroy()
            sys.exit(0)

        # Initialize media controller for debug mode too
        get_media_controller()

        overlay = BreakOverlay(
            root, settings["short_break_duration_sec"], "short", settings, on_complete
        )
        overlay.show()
        root.mainloop()
    else:
        app = HealthApp()
        app.run()
