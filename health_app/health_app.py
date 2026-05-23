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
from tkinter import ttk

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
LOG_PATH = os.path.join(SCRIPT_DIR, "health_app.log")
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
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("HealthApp")

# ── Theme ──
TH = {
    "bg": "#0a0a1a",
    "bg2": "#121228",
    "accent": "#7c3aed",
    "accent_hover": "#9b59f5",
    "fg": "#f0f0f0",
    "fg_dim": "#8892b0",
    "success": "#00ff88",
    "warning": "#ffdd00",
    "border": "#2d2d5e",
}

# ── Media Control via SendInput ──
VK_MEDIA_PLAY_PAUSE = 0xB3

def send_media_key(vk_code: int):
    """Send a media key press/release via keybd_event (highly reliable globally)."""
    try:
        KEYEVENTF_EXTENDEDKEY = 0x0001
        KEYEVENTF_KEYUP = 0x0002
        
        # Press
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        # Release
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)  # Give OS time to process
    except Exception as e:
        logger.error(f"Media key send error: {e}")

def is_workstation_locked() -> bool:
    """Check if the Windows workstation is currently locked."""
    try:
        user32 = ctypes.windll.user32
        # 0x0100 is DESKTOP_SWITCHDESKTOP
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
}


# ══════════════════════════════════════════════════════════
#  Settings
# ══════════════════════════════════════════════════════════
def load_settings() -> dict:
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r") as f:
                saved = json.load(f)
                # Merge with defaults for any missing keys
                merged = {**DEFAULT_SETTINGS, **saved}
                return merged
    except Exception as e:
        logger.error(f"Settings load error: {e}")
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    try:
        with open(SETTINGS_PATH, "w") as f:
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

    breath_cycle = 4.0  # seconds per breath cycle (inhale + exhale)

    for i in range(n_samples):
        t = i / sample_rate

        # Breathing envelope: sine wave for inhale/exhale rhythm
        breath_phase = (t % breath_cycle) / breath_cycle
        # Smooth inhale (0 to 0.5) then exhale (0.5 to 1.0)
        if breath_phase < 0.5:
            envelope = math.sin(breath_phase * math.pi)  # 0 -> 1 -> 0
        else:
            envelope = math.sin(breath_phase * math.pi) * 0.6  # softer exhale

        envelope = max(0, envelope) * 0.35

        # Base tone: soft pad-like sound with harmonics
        freq_base = 220  # A3
        tone = (
            math.sin(2 * math.pi * freq_base * t) * 0.4
            + math.sin(2 * math.pi * freq_base * 1.5 * t) * 0.2  # fifth
            + math.sin(2 * math.pi * freq_base * 2 * t) * 0.15   # octave
            + math.sin(2 * math.pi * freq_base * 0.5 * t) * 0.25 # sub
        )

        # 8D effect: pan left-right with slow rotation
        pan_speed = 0.15  # rotations per second
        pan = math.sin(2 * math.pi * pan_speed * t)

        left_vol = math.sqrt(0.5 * (1 + pan))
        right_vol = math.sqrt(0.5 * (1 - pan))

        sample_val = tone * envelope

        left_sample = int(sample_val * left_vol * 32767)
        right_sample = int(sample_val * right_vol * 32767)

        left_sample = max(-32767, min(32767, left_sample))
        right_sample = max(-32767, min(32767, right_sample))

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
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=sunrise,sunset&timezone=auto"
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
        return {"temperature": 25, "is_day": 1, "sunrise": "", "sunset": ""}


def kelvin_to_rgb(kelvin: int) -> tuple:
    """Convert color temperature (Kelvin) to RGB."""
    temp = kelvin / 100.0

    if temp <= 66:
        red = 255
    else:
        red = 329.698727446 * ((temp - 60) ** -0.1332047592)
        red = max(0, min(255, red))

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
        blue = 138.5177312231 * math.log(temp - 10) - 305.0447927307
        blue = max(0, min(255, blue))

    return (int(red), int(green), int(blue))


def apply_gamma_ramp(kelvin: int):
    """Apply color temperature via Windows gamma ramp."""
    try:
        r, g, b = kelvin_to_rgb(kelvin)
        # Normalize to 0-1
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0

        # Build gamma ramp (256 WORD entries per channel)
        GammaArray = (ctypes.wintypes.WORD * 256 * 3)()

        for i in range(256):
            GammaArray[0][i] = int(min(65535, i * 256 * rf))
            GammaArray[1][i] = int(min(65535, i * 256 * gf))
            GammaArray[2][i] = int(min(65535, i * 256 * bf))

        hdc = ctypes.windll.user32.GetDC(None)
        ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(GammaArray))
        ctypes.windll.user32.ReleaseDC(None, hdc)
        logger.info(f"Applied color temperature: {kelvin}K")
    except Exception as e:
        logger.error(f"Gamma ramp error: {e}")


def reset_gamma_ramp():
    """Reset gamma ramp to default (6500K)."""
    apply_gamma_ramp(6500)


def apply_dwm_rounding(window):
    try:
        import ctypes
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
#  Pre-break Warning Toast
# ══════════════════════════════════════════════════════════
class WarningToast:
    def __init__(self, message: str, duration_sec: int, enable_sound: bool = True):
        self.message = message
        self.duration = duration_sec
        self.enable_sound = enable_sound

    def show(self):
        threading.Thread(target=self._create, daemon=True).start()

    def _create(self):
        try:
            root = tk.Tk()
            root.withdraw()

            toast = tk.Toplevel(root)
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.attributes("-alpha", 0.0)
            toast.configure(bg=TH["bg2"])

            tw, th = 350, 70
            sw = toast.winfo_screenwidth()
            final_x = sw - tw - 20
            start_x = sw + 10

            toast.geometry(f"{tw}x{th}+{start_x}+{60}")

            tk.Frame(toast, bg=TH["accent"], width=4).pack(side=tk.LEFT, fill=tk.Y)
            content = tk.Frame(toast, bg=TH["bg2"], padx=12, pady=10)
            content.pack(fill=tk.BOTH, expand=True)

            tk.Label(
                content, text="👁️  " + self.message,
                font=("Segoe UI", 11, "bold"), bg=TH["bg2"], fg=TH["fg"]
            ).pack(anchor=tk.W)

            tk.Label(
                content, text=f"Break in {self.duration} seconds",
                font=("Segoe UI", 9), bg=TH["bg2"], fg=TH["fg_dim"]
            ).pack(anchor=tk.W)

            toast.update_idletasks()
            apply_dwm_rounding(toast)

            def slide_in(step=0):
                if step <= 20:
                    p = step / 20
                    ease = 1 - (1 - p) ** 3
                    cx = int(start_x + (final_x - start_x) * ease)
                    try:
                        toast.geometry(f"{tw}x{th}+{cx}+{60}")
                        toast.attributes("-alpha", min(0.92, ease * 0.92))
                        toast.after(16, lambda: slide_in(step + 1))
                    except tk.TclError:
                        pass
                else:
                    toast.after(self.duration * 1000, lambda: close_toast())

            def close_toast():
                try:
                    toast.destroy()
                    root.destroy()
                except Exception:
                    pass

            toast.deiconify()
            slide_in(0)

            # Play pre-break sound asynchronously
            if self.enable_sound:
                try:
                    import winsound
                    sound_path = os.path.join(SCRIPT_DIR, "resources", "on_pre_break.wav")
                    if os.path.exists(sound_path):
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                except Exception as e:
                    logger.error(f"Warning toast sound play error: {e}")

            root.mainloop()
        except Exception as e:
            logger.error(f"Warning toast error: {e}")


# ══════════════════════════════════════════════════════════
#  Full-Screen Break Overlay
# ══════════════════════════════════════════════════════════
class BreakOverlay:
    """Full-screen black overlay on all monitors with countdown and breathing text."""

    def __init__(self, duration_sec: int, break_type: str, settings: dict):
        self.duration = duration_sec
        self.break_type = break_type
        self.settings = settings
        self._remaining = duration_sec
        self._original_brightness = None
        self.status = "completed"

    def show(self):
        """Show the overlay (blocking call on the calling thread)."""
        try:
            # Dim screen (bypassed per request)
            if SBC_AVAILABLE and self.settings.get("enable_dimming"):
                try:
                    self._original_brightness = sbc.get_brightness()
                    logger.info("Physical brightness dimming bypassed.")
                except Exception as e:
                    logger.error(f"Brightness query error: {e}")

            # Pause any currently playing system media
            send_media_key(VK_MEDIA_PLAY_PAUSE)
            logger.info("Sent media pause key for break screen.")

            # Play break sound
            if PYGAME_AVAILABLE and self.settings.get("enable_sound"):
                try:
                    audio_source = self.settings.get("break_audio_source", "default")
                    sound_file = None
                    ambient_dir = os.path.join(SCRIPT_DIR, "resources", "ambient")
                    
                    if audio_source == "default":
                        sound_file = BREATHING_WAV
                    elif audio_source == "random":
                        import random
                        if os.path.exists(ambient_dir):
                            files = [f for f in os.listdir(ambient_dir) if f.endswith((".mp3", ".wav"))]
                            if files:
                                sound_file = os.path.join(ambient_dir, random.choice(files))
                    else:
                        # Specific track
                        if os.path.exists(ambient_dir):
                            for ext in [".mp3", ".wav"]:
                                test_path = os.path.join(ambient_dir, f"{audio_source}{ext}")
                                if os.path.exists(test_path):
                                    sound_file = test_path
                                    break
                    
                    if not sound_file or not os.path.exists(sound_file):
                        sound_file = BREATHING_WAV
                        
                    logger.info(f"Loading break sound: {sound_file}")
                    pygame.mixer.music.load(sound_file)
                    pygame.mixer.music.play(-1)  # Loop
                except Exception as e:
                    logger.error(f"Audio play error: {e}")

            root = tk.Tk()
            root.attributes("-fullscreen", True)
            root.attributes("-topmost", True)
            root.configure(bg="black")
            root.overrideredirect(True)

            # Prevent Alt+F4
            root.protocol("WM_DELETE_WINDOW", lambda: None)
            root.bind("<Escape>", lambda e: None)
            root.bind("<Alt-F4>", lambda e: None)

            # Cover all monitors
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

            # ── UI ──
            main_frame = tk.Frame(root, bg="black")
            main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            # Break type label
            type_text = "☕ Short Break" if self.break_type == "short" else "🧘 Long Break"
            tk.Label(
                main_frame, text=type_text,
                font=("Segoe UI", 20), fg=TH["accent"], bg="black"
            ).pack(pady=(0, 20))

            # Countdown
            countdown_var = tk.StringVar(value=str(self.duration))
            countdown_label = tk.Label(
                main_frame, textvariable=countdown_var,
                font=("Segoe UI Light", 96, "bold"), fg="white", bg="black"
            )
            countdown_label.pack(pady=(0, 20))

            # Breathing text
            breathing_var = tk.StringVar(value="Breathe In...")
            breathing_label = tk.Label(
                main_frame, textvariable=breathing_var,
                font=("Segoe UI", 24), fg=TH["fg_dim"], bg="black"
            )
            breathing_label.pack(pady=(0, 10))

            # Skip and Postpone button callbacks
            def skip_break():
                self.status = "skipped"
                logger.info("Break skipped by user action.")
                self._cleanup(root)

            def postpone_break():
                self.status = "postponed"
                logger.info("Break postponed by user action.")
                self._cleanup(root)

            # Button container frame
            btn_frame = tk.Frame(main_frame, bg="black")
            btn_frame.pack(pady=10)

            # Modern button controls with hover styles
            btn_skip = tk.Button(
                btn_frame, text="Skip ⏭", font=("Segoe UI", 12, "bold"),
                bg="#1a1a2e", fg=TH["fg_dim"], relief=tk.FLAT, cursor="hand2",
                activebackground=TH["bg2"], activeforeground="white",
                padx=20, pady=8, command=skip_break
            )
            btn_skip.pack(side=tk.LEFT, padx=10)

            btn_postpone = tk.Button(
                btn_frame, text="Postpone (2m) ⏰", font=("Segoe UI", 12, "bold"),
                bg=TH["accent"], fg="white", relief=tk.FLAT, cursor="hand2",
                activebackground=TH["accent_hover"], activeforeground="white",
                padx=20, pady=8, command=postpone_break
            )
            btn_postpone.pack(side=tk.LEFT, padx=10)

            def on_enter_skip(e):
                btn_skip.config(bg=TH["bg2"], fg="white")
            def on_leave_skip(e):
                btn_skip.config(bg="#1a1a2e", fg=TH["fg_dim"])
            btn_skip.bind("<Enter>", on_enter_skip)
            btn_skip.bind("<Leave>", on_leave_skip)

            def on_enter_post(e):
                btn_postpone.config(bg=TH["accent_hover"])
            def on_leave_post(e):
                btn_postpone.config(bg=TH["accent"])
            btn_postpone.bind("<Enter>", on_enter_post)
            btn_postpone.bind("<Leave>", on_leave_post)

            # Tip
            tk.Label(
                main_frame, text="Look away from the screen • Focus on something 20ft away",
                font=("Segoe UI", 12), fg="#444", bg="black"
            ).pack(pady=(20, 0))

            self._remaining = self.duration

            def update_countdown():
                if self._remaining > 0:
                    countdown_var.set(str(self._remaining))

                    # Breathing cycle (4s inhale, 4s exhale)
                    cycle = (self.duration - self._remaining) % 8
                    if cycle < 4:
                        breathing_var.set("Breathe In... 🌬️")
                        breathing_label.config(fg=TH["success"])
                    else:
                        breathing_var.set("Breathe Out... 💨")
                        breathing_label.config(fg=TH["accent"])

                    self._remaining -= 1
                    root.after(1000, update_countdown)
                else:
                    # Break over
                    self._cleanup(root)

            update_countdown()
            root.mainloop()

        except Exception as e:
            logger.error(f"Break overlay error: {e}")
            self._restore()

    def _cleanup(self, root):
        """Clean up and restore system state."""
        try:
            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
            root.destroy()

            # Play post-break sound asynchronously
            if self.settings.get("enable_sound"):
                try:
                    import winsound
                    sound_path = os.path.join(SCRIPT_DIR, "resources", "on_stop_break.wav")
                    if os.path.exists(sound_path):
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                except Exception as e:
                    logger.error(f"Stop break sound play error: {e}")
        except Exception:
            pass
        self._restore()
        # Resume system media after break
        time.sleep(0.3)
        send_media_key(VK_MEDIA_PLAY_PAUSE)
        logger.info("Sent media resume key after break screen.")

    def _restore(self):
        """Restore brightness (bypassed per request)."""
        if SBC_AVAILABLE and self._original_brightness:
            try:
                logger.info("Physical brightness restore bypassed.")
            except Exception as e:
                logger.error(f"Brightness restore error: {e}")


# ══════════════════════════════════════════════════════════
#  Settings GUI
# ══════════════════════════════════════════════════════════
class SettingsWindow:
    def __init__(self, settings: dict, on_save):
        self.settings = settings
        self.on_save = on_save

    def show(self):
        threading.Thread(target=self._create, daemon=True).start()

    def _create(self):
        root = tk.Tk()
        root.title("Health App — Settings")
        root.geometry("450x560")
        root.configure(bg=TH["bg"])
        root.resizable(False, False)

        apply_dwm_rounding(root)

        # Title
        tk.Label(
            root, text="⚙️ Break Schedule Settings",
            font=("Segoe UI", 16, "bold"), bg=TH["bg"], fg=TH["accent"]
        ).pack(pady=(20, 15))

        frame = tk.Frame(root, bg=TH["bg"], padx=30)
        frame.pack(fill=tk.BOTH, expand=True)

        entries = {}

        def add_field(parent, label, key, row):
            tk.Label(
                parent, text=label, font=("Segoe UI", 11),
                bg=TH["bg"], fg=TH["fg"], anchor=tk.W
            ).grid(row=row, column=0, sticky=tk.W, pady=6)

            var = tk.StringVar(value=str(self.settings.get(key, "")))
            entry = tk.Entry(
                parent, textvariable=var, font=("Segoe UI", 11),
                bg=TH["bg2"], fg=TH["fg"], insertbackground=TH["accent"],
                relief=tk.FLAT, highlightthickness=1,
                highlightcolor=TH["accent"], highlightbackground=TH["border"],
                width=10
            )
            entry.grid(row=row, column=1, sticky=tk.E, pady=6, padx=(10, 0))
            entries[key] = var

        add_field(frame, "Short break interval (min):", "short_break_interval_min", 0)
        add_field(frame, "Short break duration (sec):", "short_break_duration_sec", 1)
        add_field(frame, "Long break interval (min):", "long_break_interval_min", 2)
        add_field(frame, "Long break duration (sec):", "long_break_duration_sec", 3)
        add_field(frame, "Pre-warning (sec before break):", "pre_warning_sec", 4)
        add_field(frame, "Latitude:", "latitude", 5)
        add_field(frame, "Longitude:", "longitude", 6)

        # Break Audio Source Dropdown
        tk.Label(
            frame, text="Break Audio Source:", font=("Segoe UI", 11),
            bg=TH["bg"], fg=TH["fg"], anchor=tk.W
        ).grid(row=7, column=0, sticky=tk.W, pady=6)

        audio_sources = ["default", "random", "campfire", "forest", "night", "ocean", "rain", "waterfall"]
        audio_var = tk.StringVar(value=self.settings.get("break_audio_source", "default"))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox",
            fieldbackground=TH["bg2"],
            background=TH["accent"],
            foreground=TH["fg"],
            arrowcolor=TH["fg"],
            bordercolor=TH["border"],
            darkcolor=TH["bg2"],
            lightcolor=TH["bg2"]
        )
        audio_combo = ttk.Combobox(
            frame, textvariable=audio_var, values=audio_sources, font=("Segoe UI", 10),
            state="readonly", width=12
        )
        audio_combo.grid(row=7, column=1, sticky=tk.E, pady=6, padx=(10, 0))

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        # Checkboxes
        chk_frame = tk.Frame(root, bg=TH["bg"], padx=30)
        chk_frame.pack(fill=tk.X, pady=(5, 10))

        sound_var = tk.BooleanVar(value=self.settings.get("enable_sound", True))
        tk.Checkbutton(
            chk_frame, text="Enable breathing sound", variable=sound_var,
            font=("Segoe UI", 10), bg=TH["bg"], fg=TH["fg"],
            selectcolor=TH["bg2"], activebackground=TH["bg"]
        ).pack(anchor=tk.W)

        dim_var = tk.BooleanVar(value=self.settings.get("enable_dimming", True))
        tk.Checkbutton(
            chk_frame, text="Dim screen during breaks", variable=dim_var,
            font=("Segoe UI", 10), bg=TH["bg"], fg=TH["fg"],
            selectcolor=TH["bg2"], activebackground=TH["bg"]
        ).pack(anchor=tk.W)

        warmth_var = tk.BooleanVar(value=self.settings.get("enable_weather_warmth", True))
        tk.Checkbutton(
            chk_frame, text="Weather-based color temperature", variable=warmth_var,
            font=("Segoe UI", 10), bg=TH["bg"], fg=TH["fg"],
            selectcolor=TH["bg2"], activebackground=TH["bg"]
        ).pack(anchor=tk.W)

        # Save button
        def on_save():
            for key, var in entries.items():
                val = var.get()
                if key in ("latitude", "longitude"):
                    self.settings[key] = float(val)
                else:
                    self.settings[key] = int(val)

            self.settings["enable_sound"] = sound_var.get()
            self.settings["enable_dimming"] = dim_var.get()
            self.settings["enable_weather_warmth"] = warmth_var.get()
            self.settings["break_audio_source"] = audio_var.get()

            save_settings(self.settings)
            self.on_save(self.settings)
            root.destroy()

        tk.Button(
            root, text="💾 Save Settings", font=("Segoe UI", 12, "bold"),
            bg=TH["accent"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=on_save, padx=20, pady=8
        ).pack(pady=(5, 20))

        root.mainloop()


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
def create_health_icon(paused: bool = False) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg_color = (100, 100, 100, 200) if paused else (124, 58, 237, 230)
    draw.ellipse([4, 4, 60, 60], fill=bg_color)

    # Eye icon
    draw.ellipse([16, 22, 48, 42], outline=(255, 255, 255, 220), width=2)
    draw.ellipse([26, 26, 38, 38], fill=(255, 255, 255, 220))

    if paused:
        # Pause bars
        draw.line([12, 12, 52, 52], fill=(255, 100, 100, 200), width=3)

    return img


# ══════════════════════════════════════════════════════════
#  Main Health App
# ══════════════════════════════════════════════════════════
class HealthApp:
    def __init__(self):
        self.settings = load_settings()
        self.tray_icon = None
        self._running = True
        self._paused = self.settings.get("paused", False)
        self._skip_next = False
        self._last_short_break = time.time()
        self._last_long_break = time.time()

    def _take_break(self, break_type: str = "short"):
        """Execute a break."""
        if break_type == "short":
            duration = self.settings["short_break_duration_sec"]
        else:
            duration = self.settings["long_break_duration_sec"]

        logger.info(f"Starting {break_type} break ({duration}s)")

        overlay = BreakOverlay(duration, break_type, self.settings)
        overlay.show()

        if overlay.status == "postponed":
            logger.info(f"{break_type.title()} break postponed by 2 minutes.")
            if break_type == "short":
                short_interval = self.settings["short_break_interval_min"] * 60
                self._last_short_break = time.time() - (short_interval - 120)
            else:
                long_interval = self.settings["long_break_interval_min"] * 60
                self._last_long_break = time.time() - (long_interval - 120)
                # Also reset short break to prevent it from firing immediately
                short_interval = self.settings["short_break_interval_min"] * 60
                self._last_short_break = time.time() - (short_interval - 120)
        else:
            logger.info(f"{break_type.title()} break {overlay.status}.")
            if break_type == "short":
                self._last_short_break = time.time()
            else:
                self._last_long_break = time.time()
                self._last_short_break = time.time()  # Reset short too

    def _scheduler_loop(self):
        """Background thread: schedule breaks based on configured intervals."""
        logger.info("Break scheduler started.")

        # Weather-based color temp (run once at start, then every 30 min)
        last_weather_check = 0

        while self._running:
            try:
                now = time.time()

                # Weather check every 30 minutes
                if self.settings.get("enable_weather_warmth") and now - last_weather_check > 1800:
                    last_weather_check = now
                    threading.Thread(target=self._update_color_temp, daemon=True).start()

                if self._paused:
                    time.sleep(5)
                    continue

                # Lock screen handling with 15-minute grace period upon unlock
                was_locked = False
                while self._running and is_workstation_locked():
                    was_locked = True
                    time.sleep(1)

                if was_locked:
                    now = time.time()
                    short_interval = self.settings["short_break_interval_min"] * 60
                    long_interval = self.settings["long_break_interval_min"] * 60
                    grace_period = min(15 * 60, short_interval)
                    
                    self._last_short_break = now - short_interval + grace_period
                    self._last_long_break = max(self._last_long_break, now - long_interval + grace_period)
                    logger.info(f"Screen unlocked. Next break pushed to {grace_period // 60} mins from now.")
                    continue

                short_interval = self.settings["short_break_interval_min"] * 60
                long_interval = self.settings["long_break_interval_min"] * 60
                pre_warn = self.settings["pre_warning_sec"]

                elapsed_short = now - self._last_short_break
                elapsed_long = now - self._last_long_break

                # Check for long break first
                if elapsed_long >= long_interval - pre_warn and elapsed_long < long_interval:
                    # Pre-warning for long break
                    remaining = int(long_interval - elapsed_long)
                    if remaining == pre_warn:
                        WarningToast(
                            f"Long break in {pre_warn} seconds",
                            pre_warn,
                            self.settings.get("enable_sound", True)
                        ).show()

                elif elapsed_long >= long_interval:
                    if self._skip_next:
                        self._skip_next = False
                        self._last_long_break = now
                        self._last_short_break = now
                        logger.info("Skipped long break.")
                    else:
                        self._take_break("long")
                    continue

                # Check for short break
                elif elapsed_short >= short_interval - pre_warn and elapsed_short < short_interval:
                    remaining = int(short_interval - elapsed_short)
                    if remaining == pre_warn:
                        WarningToast(
                            f"Short break in {pre_warn} seconds",
                            pre_warn,
                            self.settings.get("enable_sound", True)
                        ).show()

                elif elapsed_short >= short_interval:
                    if self._skip_next:
                        self._skip_next = False
                        self._last_short_break = now
                        logger.info("Skipped short break.")
                    else:
                        self._take_break("short")
                    continue

            except Exception as e:
                logger.error(f"Scheduler error: {e}")

            time.sleep(1)

    def _update_color_temp(self):
        """Fetch weather and adjust display color temperature."""
        try:
            lat = self.settings.get("latitude", 13.08)
            lon = self.settings.get("longitude", 80.27)
            weather = get_weather_info(lat, lon)

            if weather["is_day"]:
                kelvin = 6500  # Neutral daylight
            else:
                kelvin = 3500  # Warm night

            # Adjust for outdoor temperature (colder outside = warmer screen)
            outdoor_temp = weather.get("temperature", 25)
            if outdoor_temp < 10:
                kelvin = min(kelvin, 3200)
            elif outdoor_temp > 35:
                kelvin = max(kelvin, 5500)

            apply_gamma_ramp(kelvin)

        except Exception as e:
            logger.error(f"Color temp update error: {e}")

    def _on_settings_saved(self, new_settings):
        self.settings = new_settings
        logger.info("Settings updated from GUI.")

    def _on_take_break(self, icon, item):
        threading.Thread(target=lambda: self._take_break("short"), daemon=True).start()

    def _on_skip(self, icon, item):
        self._skip_next = True
        logger.info("Next break will be skipped.")

    def _on_settings(self, icon, item):
        SettingsWindow(dict(self.settings), self._on_settings_saved).show()

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

    def run(self):
        logger.info("=" * 50)
        logger.info("Health App starting...")
        logger.info(f"Settings: {json.dumps(self.settings, indent=2)}")

        # Generate breathing sound
        generate_breathing_sound()

        # System uptime
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot
        logger.info(f"System uptime: {uptime}")

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
                    self._on_pause_resume
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )

        # Start scheduler
        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        scheduler_thread.start()

        logger.info("Tray icon running.")
        self.tray_icon.run()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "/debug:break screen":
        # Force generate breathing sound if it doesn't exist
        generate_breathing_sound()
        app = HealthApp()
        # Trigger break immediately and exit on complete/skip/postpone
        app._take_break("short")
        sys.exit(0)
    else:
        app = HealthApp()
        app.run()
