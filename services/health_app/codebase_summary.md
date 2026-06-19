# Codebase Summary: health_app

## Overview
- **Scan Date:** 2026-06-14 00:28:46
- **Source Folder:** `C:\Users\NANDHA A\Desktop\FOLDERS\UTILITIES\services\health_app`
- **Total Text Files:** 18
- **Estimated Token Count:** 50,875

## Directory Tree
```text
health_app/
├── core/
│   ├── __init__.py
│   ├── audio.py
│   ├── constants.py
│   ├── gamma.py
│   ├── logger.py
│   ├── media.py
│   ├── settings.py
│   └── utils.py
├── health_app.log
├── health_app.py
├── resources/
│   ├── ambient/
│   │   ├── campfire.mp3
│   │   ├── forest.mp3
│   │   ├── night.mp3
│   │   ├── ocean.mp3
│   │   ├── rain.mp3
│   │   └── waterfall.mp3
│   ├── breathing_8d.wav
│   ├── on_pre_break.wav
│   ├── on_stop_break.wav
│   └── sounds/
│       ├── bubble_pop.wav
│       ├── crystal_bell.wav
│       ├── cyber_alert.wav
│       ├── digital_chime.wav
│       ├── echo_ping.wav
│       ├── retro_beep.wav
│       ├── sci_fi_sweep.wav
│       ├── soft_click.wav
│       ├── tech_chirp.wav
│       └── zen_bowl.wav
├── settings.json
├── test_preview.py
├── tests/
│   └── test_health_app.py
└── ui/
    ├── __init__.py
    ├── overlay.py
    ├── settings_ui.py
    ├── theme.py
    └── toast.py
```

## File Contents

### File: `core/__init__.py`
- **Path:** `core/__init__.py`
- **Estimated Tokens:** 6
- **mtime:** 1781114451.516

```python
# HealthApp core package
```

---

### File: `core/audio.py`
- **Path:** `core/audio.py`
- **Estimated Tokens:** 3,051
- **mtime:** 1781116423.527

```python
import os
import math
import struct
import wave
import urllib.request
from core.logger import logger

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BREATHING_WAV = os.path.join(APP_ROOT, "resources", "breathing_8d.wav")

try:
    import pygame
    # Reinitialize if needed; pygame module level init is fine
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


def generate_breathing_sound(duration_sec: int = 65):
    """Generate a stereo WAV with breathing-like tones and 8D panning effect."""
    os.makedirs(os.path.dirname(BREATHING_WAV), exist_ok=True)
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


def ensure_sound_effects():
    """Download sound effects from the web, with local synthesis as a robust fallback."""
    sounds_dir = os.path.join(APP_ROOT, "resources", "sounds")
    os.makedirs(sounds_dir, exist_ok=True)

    sounds = {
        "cyber_alert.wav": "cyber_alert",
        "retro_beep.wav": "retro_beep",
        "zen_bowl.wav": "zen_bowl",
        "echo_ping.wav": "echo_ping",
        "digital_chime.wav": "digital_chime",
        "sci_fi_sweep.wav": "sci_fi_sweep",
        "soft_click.wav": "soft_click",
        "tech_chirp.wav": "tech_chirp",
        "bubble_pop.wav": "bubble_pop",
        "crystal_bell.wav": "crystal_bell",
    }

    # Public domain short WAV files
    sound_urls = {
        "cyber_alert.wav": (
            "https://raw.githubusercontent.com/iondrimba/images-and-sounds/"
            "master/sound-effects/success.wav"
        ),
        "retro_beep.wav": (
            "https://raw.githubusercontent.com/iondrimba/images-and-sounds/"
            "master/sound-effects/click.wav"
        ),
        "zen_bowl.wav": (
            "https://raw.githubusercontent.com/sfiera/wav-samples/master/"
            "input/pcm08m.wav"
        ),
        "echo_ping.wav": (
            "https://raw.githubusercontent.com/nandhaa/AeroHub/main/"
            "BatteryMonitor/sounds/mac_connect.wav"
        ),
    }

    for filename, sound_type in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        if os.path.exists(filepath):
            continue

        downloaded = False
        url = sound_urls.get(filename)
        if url:
            try:
                logger.info(f"Attempting to download {filename}...")
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    with open(filepath, "wb") as out_file:
                        out_file.write(response.read())
                logger.info(f"Successfully downloaded {filename}")
                downloaded = True
            except Exception as e:
                logger.warning(
                    f"Failed to download {filename}: {e}. Falling back to synthesis."
                )

        if not downloaded:
            try:
                logger.info(f"Synthesizing sound: {filename} ({sound_type})")
                _synthesize_wav(filepath, sound_type)
            except Exception as e:
                logger.error(f"Failed to synthesize {filename}: {e}")


def _synthesize_wav(filepath, sound_type):
    sample_rate = 44100
    channels = 1
    sampwidth = 2
    samples = []

    if sound_type == "cyber_alert":
        duration = 0.4
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            if t < 0.15:
                freq = 880
                val = math.sin(2 * math.pi * freq * t)
                decay = math.exp(-10.0 * t)
            elif 0.15 <= t < 0.20:
                val = 0.0
                decay = 0.0
            else:
                freq = 1760
                val = math.sin(2 * math.pi * freq * (t - 0.20))
                decay = math.exp(-12.0 * (t - 0.20))
            samples.append(int(val * decay * 16384))

    elif sound_type == "retro_beep":
        duration = 0.15
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * 600 * t)
            env = 1.0 if t < 0.12 else (0.15 - t) / 0.03
            samples.append(int(val * env * 12000))

    elif sound_type == "zen_bowl":
        duration = 2.0
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = (
                math.sin(2 * math.pi * 150 * t) * 0.5
                + math.sin(2 * math.pi * 300 * t) * 0.3
                + math.sin(2 * math.pi * 450 * t) * 0.2
            )
            decay = math.exp(-2.5 * t)
            samples.append(int(val * decay * 16384))

    elif sound_type == "echo_ping":
        duration = 1.2
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val1 = math.sin(2 * math.pi * 1000 * t) * math.exp(-8.0 * t)
            val2 = 0.0
            if t > 0.4:
                val2 = (
                    0.4
                    * math.sin(2 * math.pi * 1000 * (t - 0.4))
                    * math.exp(-6.0 * (t - 0.4))
                )
            val = val1 + val2
            samples.append(int(val * 16384))

    elif sound_type == "digital_chime":
        duration = 0.5
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            if t < 0.2:
                val = math.sin(2 * math.pi * 1200 * t) * math.exp(-10.0 * t)
            else:
                val = math.sin(2 * math.pi * 1500 * (t - 0.2)) * math.exp(
                    -10.0 * (t - 0.2)
                )
            samples.append(int(val * 16384))

    elif sound_type == "sci_fi_sweep":
        duration = 0.4
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 400 + (1200 * (t / duration))
            val = math.sin(2 * math.pi * freq * t)
            env = 1.0
            if t < 0.05:
                env = t / 0.05
            elif t > 0.35:
                env = (duration - t) / 0.05
            samples.append(int(val * env * 14000))

    elif sound_type == "soft_click":
        duration = 0.05
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * 2000 * t)
            decay = math.exp(-100.0 * t)
            samples.append(int(val * decay * 12000))

    elif sound_type == "tech_chirp":
        duration = 0.08
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 2500 - 1300 * (t / duration)
            val = math.sin(2 * math.pi * freq * t)
            decay = math.exp(-25.0 * t)
            samples.append(int(val * decay * 14000))

    elif sound_type == "bubble_pop":
        duration = 0.15
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 300 + 1500 * (t / duration)
            val = math.sin(2 * math.pi * freq * t)
            env = math.exp(-15.0 * t)
            samples.append(int(val * env * 16384))

    elif sound_type == "crystal_bell":
        duration = 1.0
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = (
                math.sin(2 * math.pi * 2000 * t) * 0.7
                + math.sin(2 * math.pi * 3000 * t) * 0.3
            )
            decay = math.exp(-6.0 * t)
            samples.append(int(val * decay * 16384))

    else:
        duration = 0.2
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * 440 * t)
            samples.append(int(val * 8192))

    with wave.open(filepath, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(sampwidth)
        w.setframerate(sample_rate)
        w.writeframes(struct.pack(f"<{len(samples)}h", *samples))


def select_break_audio(settings: dict) -> str:
    """Select the break audio file based on settings."""
    audio_source = settings.get("break_audio_source", "default")
    ambient_dir = os.path.join(APP_ROOT, "resources", "ambient")

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


def get_sapi_voices() -> list:
    """Dynamically list SAPI voices description or return default list."""
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        voices = speaker.GetVoices()
        names = []
        for i in range(voices.Count):
            names.append(voices.Item(i).GetDescription())
        return names if names else ["Default"]
    except Exception:
        return ["Default"]


def speak_sapi_async(text: str, voice_name: str = "Default", volume: int = 80, rate: int = 0):
    """Speak SAPI text in a background thread to prevent GUI lockup."""
    import threading

    def target():
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            if voice_name and voice_name != "Default":
                voices = speaker.GetVoices()
                for i in range(voices.Count):
                    if voices.Item(i).GetDescription() == voice_name:
                        speaker.Voice = voices.Item(i)
                        break
            speaker.Volume = max(0, min(100, int(volume)))
            speaker.Rate = max(-10, min(10, int(rate)))
            speaker.Speak(text)
        except Exception as e:
            logger.error(f"SAPI voice error: {e}")
        finally:
            pythoncom.CoUninitialize()

    threading.Thread(target=target, daemon=True).start()

```

---

### File: `core/constants.py`
- **Path:** `core/constants.py`
- **Estimated Tokens:** 2,374
- **mtime:** 1781257684.181

```python
# Constants and Configuration defaults for HealthApp

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

# Media Key Constants
VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

# Health Tips
HEALTH_TIPS = {
    "breathing": [
        "Take a slow, deep breath in for 4 seconds, hold for 4, and exhale for 4. 🫁",
        "Deep breathing increases oxygen flow and induces a state of calm. 🧘",
        "Inhale peace, exhale tension. Let your belly rise with each breath. 🌬️",
    ],
    "eye_care": [
        "Look away from the screen! Focus on an object 20 feet away for 20 seconds. 👁️",
        "Blink slowly and deliberately 10 times to rehydrate your eyes. 💧",
        "Gently roll your eyes in circles to relieve strain on the eye muscles. 🌀",
        "Adjust screen brightness so it matches the ambient lighting around you. 💡",
    ],
    "posture": [
        "Sit up straight! Align your ears with your shoulders. 📐",
        "Relax your shoulders away from your ears. Check your spine alignment. 🧘",
        "Make sure your feet are flat on the floor and your knees are at 90 degrees. 🦶",
        "Adjust your chair height so your screen is at eye level. 🖥️",
    ],
    "stretch": [
        "Clasp your hands and stretch them high above your head. 🤸",
        "Rotate your neck slowly to the left, then to the right to release tension. 🔄",
        "Do a gentle torso twist in your chair to stretch your lower back. 🪑",
        "Stand up and stretch your arms and legs. Hold for 15 seconds. 🚶",
    ],
    "hydration": [
        "Time for a sip of water! Stay hydrated to keep your mind sharp. 💧",
        "Drink a glass of water. Proper hydration keeps fatigue at bay. 🥛",
        "Keep a water bottle on your desk and take a sip every few minutes. 🐳",
    ],
    "mental": [
        "Take a 10-second mental pause. Let go of all work thoughts. 🧠",
        "Acknowledge one thing you're grateful for right now. 💖",
        "Smile! Even a forced smile can reduce stress hormones. 😊",
        "Take a deep breath and clear your mind of any clutter. 🧘",
    ],
    "hands_wrists": [
        "Shake out your hands and fingers to relieve typing strain. 🖐️",
        "Stretch your wrists: gently pull your fingers back with your other hand. 🫳",
        "Make gentle fists and rotate your wrists clockwise and counter-clockwise. ✊",
        "Massage the palms of your hands to release muscular tension. 💆",
    ],
}

# Default Settings
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
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 260,
    "toast_height": 60,
    "toast_bg_color": "#252525",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#00f0ff",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "👁️",
    "toast_radius": 16,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#00f0ff",
    "toast_gradient": False,
    "toast_gradient_end": "#101625",
    "toast_shadow": True,
    "toast_accent_stripe": False,
    "toast_text_align": "left",
    "toast_auto_dismiss": True,
    "toast_click_action": "dismiss",
    "toast_progress_bar": False,
    "toast_enable_sound": True,
    "toast_sound_effect": "mac_connect",
    "toast_volume": 80,
    "toast_border_style": "Solid",
    "toast_stripe_pos": "Left",
    "wellness_points": 0,
    "current_streak": 0,
    "ht_enabled": True,
    "ht_interval_min": 10,
    "ht_duration_sec": 5,
    "ht_night_enabled": True,
    "ht_night_interval_min": 30,
    "ht_night_duration_sec": 5,
    "ht_night_toast_pos": "Bottom-Right",
    "ht_cat_breathing": True,
    "ht_cat_eye_care": True,
    "ht_cat_posture": True,
    "ht_cat_stretch": True,
    "ht_cat_hydration": True,
    "ht_cat_mental": True,
    "ht_cat_hands_wrists": True,
    "ht_toast_pos": "Right",
    "ht_toast_custom_x": 100,
    "ht_toast_custom_y": 100,
    "ht_toast_width": 280,
    "ht_toast_height": 70,
    "ht_toast_bg_color": "#252525",
    "ht_toast_fg_color": "#ffffff",
    "ht_toast_accent_color": "#00f0ff",
    "ht_toast_font_size": 11,
    "ht_toast_font_weight": "bold",
    "ht_toast_font_family": "Segoe UI",
    "ht_toast_emoji": "💡",
    "ht_toast_radius": 16,
    "ht_toast_padding_x": 12,
    "ht_toast_padding_y": 10,
    "ht_toast_anim_style": "Slide",
    "ht_toast_opacity": 0.92,
    "ht_toast_border_width": 0,
    "ht_toast_border_color": "#00f0ff",
    "ht_toast_gradient": False,
    "ht_toast_gradient_end": "#101625",
    "ht_toast_shadow": True,
    "ht_toast_accent_stripe": False,
    "ht_toast_text_align": "left",
    "ht_toast_auto_dismiss": True,
    "ht_toast_click_action": "dismiss",
    "ht_toast_progress_bar": False,
    "ht_toast_enable_sound": False,
    "ht_toast_sound_effect": "mac_disconnect",
    "ht_toast_volume": 80,
    "ht_toast_border_style": "Solid",
    "ht_toast_stripe_pos": "Left",
    "bc_enabled": True,
    "bc_start_time": "23:00",
    "bc_end_time": "06:00",
    "bc_target_brightness": 2,
    "bc_duration_minutes": 60,
    "bc_aggressive_target_brightness": 5,
    "bc_aggressive_duration_minutes": 10,
    "bc_transition_time_sec": 5,
    "bc_aggressive_transition_time_sec": 30,
    "bc_safe_brightness": 30,
    "bc_safe_duration_seconds": 30,
    "bc_toast_enable_sound": True,
    "bc_toast_sound_effect": "mac_connect",
    "bc_toast_width": 320,
    "bc_toast_height": 145,
    "bc_toast_bg_color": "#101625",
    "bc_toast_fg_color": "#e2e8f0",
    "bc_toast_accent_color": "#ff2a2a",
    "bc_toast_border_width": 1,
    "bc_toast_border_color": "#7c3aed",
    "bc_toast_radius": 16,
    "bc_toast_gradient": False,
    "bc_toast_gradient_end": "#101625",
    "bc_toast_shadow": True,
    "bc_toast_accent_stripe": False,
    "bc_toast_text_align": "left",
    "bc_toast_progress_bar": False,
    "bc_toast_click_action": "dismiss",
    "bc_toast_border_style": "Solid",
    "bc_toast_stripe_pos": "Left",
    "bc_toast_volume": 80,
    "bc_toast_opacity": 0.95,
    "bc_toast_emoji": "⚠️",
    "bc_toast_padding_x": 12,
    "bc_toast_padding_y": 10,
    "nc_enabled": True,
    "nc_start_time": "23:59",
    "nc_end_time": "06:00",
    "nc_interval_minutes": 5,
    "nc_flick_enabled": True,
    "nc_flick_hold_sec": 1.0,
    "nc_flick_fade_sec": 3.0,
    "nc_slogans": (
        "It's late. Your body needs rest. 🌙|"
        "Go to sleep. Tomorrow is a new day. 💤|"
        "Screen time is over. Time for dream time. ✨|"
        "Rest your eyes and your mind. 🛌|"
        "Sleep is the best meditation. 🧘"
    ),
    "nc_toast_width": 300,
    "nc_toast_height": 80,
    "nc_toast_bg_color": "#0d1117",
    "nc_toast_fg_color": "#c9d1d9",
    "nc_toast_accent_color": "#58a6ff",
    "nc_toast_font_size": 12,
    "nc_toast_font_weight": "bold",
    "nc_toast_font_family": "Segoe UI",
    "nc_toast_emoji": "🌙",
    "nc_toast_radius": 12,
    "nc_toast_padding_x": 15,
    "nc_toast_padding_y": 15,
    "nc_toast_anim_style": "Slide",
    "nc_toast_opacity": 0.95,
    "nc_toast_border_width": 2,
    "nc_toast_border_color": "#30363d",
    "nc_toast_enable_sound": True,
    "nc_toast_sound_effect": "mac_connect",
    "nc_toast_gradient": False,
    "nc_toast_gradient_end": "#101625",
    "nc_toast_shadow": True,
    "nc_toast_accent_stripe": False,
    "nc_toast_text_align": "left",
    "nc_toast_progress_bar": False,
    "nc_toast_click_action": "dismiss",
    "nc_toast_border_style": "Solid",
    "nc_toast_stripe_pos": "Left",
    "nc_toast_volume": 80,
    "nl_enabled": True,
    "nl_day_temp": 6500,
    "nl_night_temp": 3500,
    "nl_transition_duration": 20,
    "break_audio_source": "default",
    "voice_prompts_enabled": False,
    "voice_inhale_sec": 4,
    "voice_hold_in_sec": 4,
    "voice_exhale_sec": 4,
    "voice_hold_out_sec": 4,
    "voice_volume": 80,
    "voice_rate": 0,
    "voice_inhale_text": "Breathe in",
    "voice_exhale_text": "Breathe out",
    "voice_hold_in_text": "Hold",
    "voice_hold_out_text": "Hold",
    "voice_break_type": "Both",
    "voice_min_duration_sec": 15,
    "voice_name": "Default",
    "location_check_interval_hours": 1,
}

SOUND_EFFECTS = [
    "cyber_alert",
    "retro_beep",
    "zen_bowl",
    "echo_ping",
    "digital_chime",
    "sci_fi_sweep",
    "soft_click",
    "tech_chirp",
    "bubble_pop",
    "crystal_bell",
    "SystemAsterisk",
    "SystemExclamation",
    "SystemHand",
    "SystemQuestion",
    "SystemDefault",
]
```

---

### File: `core/gamma.py`
- **Path:** `core/gamma.py`
- **Estimated Tokens:** 1,084
- **mtime:** 1781114497.088

```python
import ctypes
import ctypes.wintypes
import datetime
import math
import requests
from core.logger import logger
from core.settings import load_settings


def _is_time_between(start_str, end_str):
    try:
        now = datetime.datetime.now().time()
        start_parts = start_str.split(":")
        end_parts = end_str.split(":")
        start = datetime.time(int(start_parts[0]), int(start_parts[1]))
        end = datetime.time(int(end_parts[0]), int(end_parts[1]))
        if start <= end:
            return start <= now <= end
        else:
            return now >= start or now <= end
    except Exception:
        return False


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
        is_day_local = (
            1
            if not _is_night_hour(datetime.datetime.now().hour, start_hour, end_hour)
            else 0
        )
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
```

---

### File: `core/logger.py`
- **Path:** `core/logger.py`
- **Estimated Tokens:** 201
- **mtime:** 1781114467.79

```python
import os
import sys
import logging
import logging.handlers

# Resolve paths relative to app root
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(os.path.dirname(APP_ROOT), "Logs")
LOG_PATH = os.path.join(LOGS_DIR, "health_app.log")

os.makedirs(LOGS_DIR, exist_ok=True)

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

# Suppress noisy EDID parse warnings from screen_brightness_control
logging.getLogger("screen_brightness_control").setLevel(logging.ERROR)
```

---

### File: `core/media.py`
- **Path:** `core/media.py`
- **Estimated Tokens:** 1,829
- **mtime:** 1781270756.5

```python
import ctypes
import ctypes.wintypes
import threading
import asyncio
import time
from core.logger import logger
from core.constants import (
    VK_MEDIA_PLAY_PAUSE,
    KEYEVENTF_EXTENDEDKEY,
    KEYEVENTF_KEYUP,
)

try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    )
    WINSDK_AVAILABLE = True
except ImportError:
    WINSDK_AVAILABLE = False


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
        self._paused_sessions = []
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
        """Pause all currently PLAYING media sessions. Records (app_id, title) to resume later."""
        with self._lock:
            self._paused_sessions.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        paused = self._run_async(self._do_pause())
        if paused is None:
            # Async failed — fall back to global media key
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        with self._lock:
            self._paused_sessions = paused

        logger.info(f"Paused {len(paused)} active media sessions via winsdk.")

    def resume_paused_media(self):
        """Resume only the media sessions that were paused before the break."""
        with self._lock:
            sessions_to_resume = list(self._paused_sessions)
            self._paused_sessions.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        if not sessions_to_resume:
            return

        count = self._run_async(self._do_resume(sessions_to_resume))
        if count is None:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        logger.info(f"Resumed {count} media sessions via winsdk.")

    async def _do_pause(self):
        """Fetch fresh sessions and pause all that are Playing (status==4).

        Returns list of (app_id, title) tuples that were successfully paused.
        """
        paused = []
        seen_sessions = set()

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    
                    title = ""
                    try:
                        props = await session.try_get_media_properties_async()
                        title = props.title or ""
                    except Exception:
                        pass

                    # Unique session key
                    s_key = (app_id, title)
                    if s_key in seen_sessions:
                        continue
                    seen_sessions.add(s_key)

                    info = session.get_playback_info()
                    if not info:
                        continue

                    status = info.playback_status
                    if status != 4:  # Not Playing
                        continue

                    result = await session.try_pause_async()
                    # Keep track of it as paused
                    paused.append((app_id, title))

                except Exception as e:
                    logger.debug(f"Error pausing session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager pause error: {e}")

        return paused

    async def _do_resume(self, paused_sessions):
        """Fetch fresh sessions and resume those whose (app_id, title) matches the saved sessions.

        Uses fresh session objects.
        """
        resumed = 0
        targets = list(paused_sessions)

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    
                    title = ""
                    try:
                        props = await session.try_get_media_properties_async()
                        title = props.title or ""
                    except Exception:
                        pass

                    matched_target = None
                    for t in targets:
                        t_app_id, t_title = t
                        if t_app_id == app_id and (not t_title or t_title == title):
                            matched_target = t
                            break

                    if matched_target:
                        targets.remove(matched_target)
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
```

---

### File: `core/settings.py`
- **Path:** `core/settings.py`
- **Estimated Tokens:** 219
- **mtime:** 1781114472.45

```python
import os
import json
from core.logger import logger
from core.constants import DEFAULT_SETTINGS

# Resolve path relative to app root
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(APP_ROOT, "settings.json")

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
```

---

### File: `core/utils.py`
- **Path:** `core/utils.py`
- **Estimated Tokens:** 93
- **mtime:** 1781114476.414

```python
import ctypes

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
```

---

### File: `health_app.log`
- **Path:** `health_app.log`
- **Estimated Tokens:** 393
- **mtime:** 1780160861.375

```
2026-05-30 22:08:42,911 - INFO - ==================================================
2026-05-30 22:08:42,911 - INFO - Health App starting...
2026-05-30 22:08:42,911 - INFO - Settings: {
  "short_break_interval_min": 20,
  "short_break_duration_sec": 15,
  "long_break_interval_min": 60,
  "long_break_duration_sec": 40,
  "pre_warning_sec": 30,
  "enable_sound": true,
  "enable_dimming": false,
  "enable_weather_warmth": true,
  "latitude": 13.08,
  "longitude": 80.27,
  "paused": false,
  "night_light_start_hour": 18,
  "night_light_end_hour": 6,
  "run_during_game": true,
  "toast_pos": "Center",
  "toast_width": 195,
  "toast_height": 50,
  "toast_bg_color": "#252525",
  "toast_fg_color": "#ffffff",
  "toast_accent_color": "#ffffff",
  "toast_font_size": 8,
  "toast_font_weight": "bold",
  "toast_emoji": "\u25d5\u203f\u25d5\u273f",
  "toast_radius": 60,
  "toast_padding_x": 28,
  "toast_padding_y": 12,
  "toast_anim_style": "Slide",
  "toast_opacity": 2.0,
  "toast_border_width": 6,
  "toast_border_color": "#7c3aed",
  "break_audio_source": "random"
}
2026-05-30 22:08:42,911 - INFO - HealthApp UDP Listener bound to 127.0.0.1:5098
2026-05-30 22:08:42,912 - INFO - System uptime: 6 days, 22:13:56.168727
2026-05-30 22:08:42,915 - INFO - Break scheduler started.
2026-05-30 22:08:42,915 - INFO - Tray icon running detached.
2026-05-30 22:08:45,158 - INFO - Applied color temperature: 3500K
2026-05-30 22:28:43,642 - INFO - Starting short break (15s)
2026-05-30 22:37:41,374 - INFO - Settings saved.
2026-05-30 22:37:41,374 - INFO - Settings updated from GUI.
```

---

### File: `health_app.py`
- **Path:** `health_app.py`
- **Estimated Tokens:** 10,954
- **mtime:** 1781288700.894

```python
"""
Health App / Eye Break Reminder — Coordinates healthy work breaks.
Full-screen overlay lock, 8D breathing audio, weather-based display warmth,
and fully configurable break schedule via settings GUI.
"""
# ruff: noqa: E402

import os
import sys

# ── Dynamic Path Setup ──
# Ensure parent directory is in sys.path to import services.aerohub_core.system_utils as system_utils and toast_utils
# and ensure HealthApp directory is in sys.path for submodule imports.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import json
import time
import queue
import threading
import datetime
import tkinter as tk

# Suppress setuptools/pkg_resources deprecation warnings from libraries
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ── Import from Core Submodules ──
from core.logger import logger
from core.constants import DEFAULT_SETTINGS, HEALTH_TIPS
from core.settings import load_settings, save_settings
from core.utils import is_workstation_locked
from core.media import get_media_controller
from core.audio import (
    generate_breathing_sound,
    ensure_sound_effects,
    PYGAME_AVAILABLE,
    pygame,
)
from core.gamma import (
    _is_time_between,
    _is_night_hour,
    kelvin_to_rgb,
    apply_gamma_ramp,
    reset_gamma_ramp,
    get_weather_info,
)

# ── Import from UI Submodules ──
from ui.theme import create_health_icon
from ui.toast import WarningToast, BrightnessWarningToast
from ui.overlay import BreakOverlay, SBC_AVAILABLE, sbc
from ui.settings_ui import SettingsWindow
import services.aerohub_core.system_utils as system_utils
import pystray
import psutil
from services.aerohub_core.toast_utils import BaseToast

# ── Re-expose symbols for backward compatibility and testing ──
__all__ = [
    "HealthApp",
    "SettingsWindow",
    "WarningToast",
    "BrightnessWarningToast",
    "BreakOverlay",
    "kelvin_to_rgb",
    "_is_night_hour",
    "DEFAULT_SETTINGS",
    "load_settings",
    "save_settings",
    "generate_breathing_sound",
    "get_media_controller",
    "apply_gamma_ramp",
]


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
        self.udp_sock = None
        self._settings_window = None

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
            "short_break_duration_sec"
            if break_type == "short"
            else "long_break_duration_sec"
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

        if status == "completed":
            self.settings["wellness_points"] = (
                self.settings.get("wellness_points", 0) + 10
            )
            self.settings["current_streak"] = self.settings.get("current_streak", 0) + 1
            save_settings(self.settings)
        elif status == "skipped":
            self.settings["current_streak"] = 0
            save_settings(self.settings)

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
        last_loop_time = time.time()

        while self._running:
            try:
                now = time.time()
                elapsed = now - last_loop_time
                last_loop_time = now

                if elapsed > 10.0:
                    logger.info(
                        "[RESUME] System sleep/hibernate/suspend detected in scheduler loop "
                        f"(elapsed={elapsed:.1f}s). Resetting break timers."
                    )
                    self._last_short_break = now
                    self._last_long_break = now
                    self._short_warn_shown = False
                    self._long_warn_shown = False

                if not system_utils.is_system_awake_and_unlocked():
                    # While system is asleep or locked, keep pushing timers forward so we start fresh upon unlock/wake
                    self._last_short_break = now
                    self._last_long_break = now
                    self._short_warn_shown = False
                    self._long_warn_shown = False
                    time.sleep(2)
                    continue

                self._maybe_update_weather(now, last_weather_check)
                if (
                    not self._game_mode
                    and self.settings.get("enable_weather_warmth")
                    and now - last_weather_check > 1800
                ):
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
            logger.info(
                "[GAME MODE] Auto-postponing long break by 2 minutes (AeroEco)."
            )
        elif elapsed_short >= short_interval:
            self._last_short_break = now - short_interval + self.POSTPONE_SECONDS
            logger.info(
                "[GAME MODE] Auto-postponing short break by 2 minutes (AeroEco)."
            )

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

        self._last_short_break = now
        self._last_long_break = now

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
                try:
                    from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
                    status = read_shared_status()
                    status["break_warning_active"] = True
                    status["break_warning_pid"] = os.getpid()
                    status["break_warning_end_time"] = now + pre_warn
                    write_shared_status(status)
                except Exception:
                    pass
                self.gui_queue.put(
                    ("warning", ("Long Break", pre_warn))
                )
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
                try:
                    from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
                    status = read_shared_status()
                    status["break_warning_active"] = True
                    status["break_warning_pid"] = os.getpid()
                    status["break_warning_end_time"] = now + pre_warn
                    write_shared_status(status)
                except Exception:
                    pass
                self.gui_queue.put(
                    ("warning", ("Short Break", pre_warn))
                )
                self._short_warn_shown = True

    def _update_color_temp(self):
        if not self.settings.get("nl_enabled", True):
            self._current_kelvin = 6500
            self._target_kelvin_actual = 6500.0
            apply_gamma_ramp(6500, log_action=True)
            return

        current_hour = datetime.datetime.now().hour
        start_hour = self.settings.get("night_light_start_hour", 18)
        end_hour = self.settings.get("night_light_end_hour", 6)

        is_night = _is_night_hour(current_hour, start_hour, end_hour)
        is_day = not is_night

        day_temp = self.settings.get("nl_day_temp", 6500)
        night_temp = self.settings.get("nl_night_temp", 3500)
        kelvin = day_temp if is_day else night_temp

        try:
            if self.settings.get("enable_weather_warmth", True):
                lat = self.settings.get("latitude", 13.08)
                lon = self.settings.get("longitude", 80.27)
                weather = get_weather_info(lat, lon)

                if abs(lat - 13.08) > 0.01 or abs(lon - 80.27) > 0.01:
                    is_day = bool(weather.get("is_day", is_day))
                    kelvin = day_temp if is_day else night_temp

                outdoor_temp = weather.get("temperature", 25)
                if outdoor_temp < 10:
                    kelvin = min(kelvin, 3200)
                elif outdoor_temp > 35:
                    kelvin = max(kelvin, 5500)

        except Exception as e:
            logger.error(f"Color temp update error: {e}")

        self._current_kelvin = kelvin
        self._target_kelvin_actual = float(kelvin)
        apply_gamma_ramp(kelvin, log_action=True)

    def _is_time_in_range(self, start_str: str, end_str: str) -> bool:
        return _is_time_between(start_str, end_str)

    def _on_settings_saved(self, new_settings):
        self.settings = new_settings
        logger.info("Settings updated from GUI. Synchronizing break timers.")
        now = time.time()
        self._last_short_break = now
        self._last_long_break = now
        self._short_warn_shown = False
        self._long_warn_shown = False
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

    def _health_toast_loop(self):
        """Background thread: show health toast reminders periodically."""
        logger.info("Health toast scheduler started.")
        self._last_health_toast = time.time()
        last_loop_time = time.time()

        while self._running:
            try:
                now = time.time()
                elapsed = now - last_loop_time
                last_loop_time = now

                if elapsed > 10.0:
                    logger.info(
                        "[RESUME] System sleep/hibernate/suspend detected in health loop "
                        f"(elapsed={elapsed:.1f}s). Resetting health tip timer."
                    )
                    self._last_health_toast += elapsed

                if not system_utils.is_system_awake_and_unlocked():
                    self._last_health_toast += elapsed
                    time.sleep(2)
                    continue

                nc_start = self.settings.get("nc_start_time", "23:59")
                nc_end = self.settings.get("nc_end_time", "06:00")
                is_night = _is_time_between(nc_start, nc_end)

                if is_night:
                    if not self.settings.get("ht_night_enabled", True):
                        time.sleep(1)
                        continue
                    interval_sec = self.settings.get("ht_night_interval_min", 30) * 60
                else:
                    if not self.settings.get("ht_enabled", True):
                        time.sleep(1)
                        continue
                    interval_sec = self.settings.get("ht_interval_min", 10) * 60

                if self._paused:
                    time.sleep(1)
                    self._last_health_toast += 1
                    continue

                if now - self._last_health_toast >= interval_sec:
                    self._trigger_health_toast()
                    self._last_health_toast = now

            except Exception as e:
                logger.error(f"Health toast loop error: {e}")

            time.sleep(1)

    def _trigger_health_toast(self):
        # Collect enabled categories
        categories = []
        for cat_key, cat_name in [
            ("ht_cat_breathing", "breathing"),
            ("ht_cat_eye_care", "eye_care"),
            ("ht_cat_posture", "posture"),
            ("ht_cat_stretch", "stretch"),
            ("ht_cat_hydration", "hydration"),
            ("ht_cat_mental", "mental"),
            ("ht_cat_hands_wrists", "hands_wrists"),
        ]:
            if self.settings.get(cat_key, True):
                categories.append(cat_name)

        if not categories:
            categories = ["eye_care"]

        import random

        selected_category = random.choice(categories)
        selected_tip = random.choice(HEALTH_TIPS[selected_category])

        logger.info(
            f"Triggering health toast tip: {selected_tip} (Category: {selected_category})"
        )
        self.gui_queue.put(("health_toast", selected_tip))

    def _brightness_care_loop(self):
        """Background thread: Monitor screen brightness and alert if too high at night."""
        logger.info("Brightness Care monitor started.")
        high_start = None
        last_alert_time = 0

        while self._running:
            try:
                if not system_utils.is_system_awake_and_unlocked():
                    high_start = None
                    time.sleep(2)
                    continue

                if not self.settings.get("bc_enabled", True) or not SBC_AVAILABLE:
                    time.sleep(5)
                    continue

                # Check if we are in late hours
                start_time = self.settings.get("bc_start_time", "23:00")
                end_time = self.settings.get("bc_end_time", "06:00")
                if not _is_time_between(start_time, end_time):
                    high_start = None
                    time.sleep(5)
                    continue

                # Retrieve current brightness
                try:
                    b_list = sbc.get_brightness()
                    if isinstance(b_list, list) and b_list:
                        curr_b = b_list[0]
                    else:
                        curr_b = int(b_list)
                except Exception as e:
                    logger.warning(f"Brightness Care failed to read brightness: {e}")
                    time.sleep(10)
                    continue

                target_b = self.settings.get("bc_target_brightness", 2)
                agg_target_b = self.settings.get("bc_aggressive_target_brightness", 5)
                duration_min = self.settings.get("bc_duration_minutes", 60)
                agg_duration_min = self.settings.get(
                    "bc_aggressive_duration_minutes", 10
                )

                now = time.time()
                if curr_b > target_b:
                    if high_start is None:
                        high_start = now
                    else:
                        elapsed_min = (now - high_start) / 60.0

                        if curr_b >= agg_target_b:
                            threshold = agg_duration_min
                        else:
                            threshold = duration_min

                        if elapsed_min >= threshold:
                            if (
                                now - last_alert_time > 120
                            ):  # 2 minute cooldown between alerts
                                logger.info(
                                    f"Screen brightness ({curr_b}%) exceeds target ({target_b}%) "
                                    f"for {elapsed_min:.1f} mins. Triggering alert."
                                )
                                is_agg = curr_b >= agg_target_b
                                self.gui_queue.put(("brightness_care", {"is_aggressive": is_agg}))
                                last_alert_time = now
                else:
                    high_start = None

            except Exception as e:
                logger.error(f"Brightness Care loop error: {e}")

            time.sleep(5)

    def _decrease_brightness(self, is_aggressive=False):
        if SBC_AVAILABLE:
            try:
                target_b = self.settings.get("bc_target_brightness", 2)
                trans_sec = self.settings.get("bc_aggressive_transition_time_sec", 30) if is_aggressive else self.settings.get("bc_transition_time_sec", 5)
                
                b_list = sbc.get_brightness()
                start_b = int(b_list[0]) if isinstance(b_list, list) and b_list else int(b_list)
                
                def fade():
                    steps = int(trans_sec * 10)
                    if steps <= 0:
                        sbc.set_brightness(target_b)
                        return
                    step_delay = trans_sec / steps
                    for i in range(1, steps + 1):
                        val = start_b + (target_b - start_b) * (i / steps)
                        sbc.set_brightness(int(val))
                        time.sleep(step_delay)
                    logger.info(f"Brightness gradually decreased to target: {target_b}% over {trans_sec}s")
                
                threading.Thread(target=fade, daemon=True).start()
            except Exception as e:
                logger.error(f"Failed to decrease brightness: {e}")

    def _skip_brightness_warning(self):
        logger.info("Brightness warning skipped by user.")

    def _play_screen_flick(self, hold_sec, fade_sec):
        flick_win = tk.Toplevel(self.root)
        flick_win.attributes("-topmost", True)
        flick_win.attributes("-alpha", 1.0)
        flick_win.configure(bg="black")
        flick_win.overrideredirect(True)
        # Cover entire virtual screen
        v_width = self.root.winfo_vrootwidth()
        v_height = self.root.winfo_vrootheight()
        v_x = self.root.winfo_vrootx()
        v_y = self.root.winfo_vrooty()
        # Fallback to screen width/height if vroot is zero
        if v_width <= 0:
            v_width = self.root.winfo_screenwidth()
            v_height = self.root.winfo_screenheight()
            v_x = 0
            v_y = 0
        flick_win.geometry(f"{v_width}x{v_height}+{v_x}+{v_y}")

        def start_fade():
            steps = int(fade_sec * 20)  # 20 steps per second
            if steps <= 0:
                flick_win.destroy()
                return

            def step(i):
                if i > steps:
                    flick_win.destroy()
                    return
                alpha = 1.0 - (i / steps)
                flick_win.attributes("-alpha", alpha)
                flick_win.after(int((fade_sec / steps) * 1000), lambda: step(i + 1))

            step(1)

        flick_win.after(int(hold_sec * 1000), start_fade)

    def _night_care_loop(self):
        """Background thread: remind user to sleep periodically during night hours."""
        logger.info("Night Care monitor started.")
        self._last_night_care = time.time()
        last_loop_time = time.time()

        while self._running:
            try:
                now = time.time()
                elapsed = now - last_loop_time
                last_loop_time = now

                if elapsed > 10.0:
                    logger.info(
                        "[RESUME] System sleep/hibernate/suspend detected in night care loop "
                        f"(elapsed={elapsed:.1f}s). Resetting night care timer."
                    )
                    self._last_night_care = now

                if not system_utils.is_system_awake_and_unlocked():
                    self._last_night_care = now
                    time.sleep(2)
                    continue

                if not self.settings.get("nc_enabled", True):
                    time.sleep(5)
                    continue

                if self._paused:
                    time.sleep(1)
                    self._last_night_care += 1
                    continue

                # Check night hours
                start_time = self.settings.get("nc_start_time", "23:59")
                end_time = self.settings.get("nc_end_time", "06:00")
                if not _is_time_between(start_time, end_time):
                    time.sleep(5)
                    continue

                interval_sec = self.settings.get("nc_interval_minutes", 5) * 60
                if now - self._last_night_care >= interval_sec:
                    slogans_str = self.settings.get("nc_slogans", "")
                    if slogans_str:
                        slogans = slogans_str.split("|")
                    else:
                        slogans = ["It's late. Your body needs rest. 🌙"]

                    import random

                    selected_slogan = random.choice(slogans)
                    logger.info(f"Triggering night care toast: {selected_slogan}")
                    
                    if self.settings.get("nc_flick_enabled", True):
                        hold_sec = self.settings.get("nc_flick_hold_sec", 1.0)
                        fade_sec = self.settings.get("nc_flick_fade_sec", 3.0)
                        self.gui_queue.put(("screen_flick", {"hold_sec": hold_sec, "fade_sec": fade_sec}))
                    
                    self.gui_queue.put(("night_care_toast", selected_slogan))
                    self._last_night_care = now

            except Exception as e:
                logger.error(f"Night Care loop error: {e}")

            time.sleep(1)

    def _location_check_loop(self):
        """Background thread: silently check geolocation periodically."""
        logger.info("Location auto-check thread started.")
        last_check_time = 0
        
        while self._running:
            try:
                now = time.time()
                interval_hours = self.settings.get("location_check_interval_hours", 1)
                
                if interval_hours <= 0:
                    # Location auto-check disabled
                    time.sleep(10)
                    continue
                
                interval_sec = interval_hours * 3600
                if now - last_check_time >= interval_sec:
                    self._perform_silent_location_check()
                    last_check_time = now
            except Exception as e:
                logger.error(f"Location check loop error: {e}")
            
            time.sleep(10)

    def _perform_silent_location_check(self):
        import urllib.request
        import json
        
        logger.info("[LOCATION] Running silent background geolocation check...")
        
        # Primary API
        try:
            req = urllib.request.Request("http://ip-api.com/json/", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                if "lat" in data and "lon" in data:
                    self._update_location_if_changed(float(data["lat"]), float(data["lon"]))
                    return
        except Exception as e:
            logger.warning(f"[LOCATION] Primary API (ip-api.com) failed: {e}. Trying fallback 1...")
            
        # Fallback 1
        try:
            req = urllib.request.Request("https://freeipapi.com/api/json", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                if "latitude" in data and "longitude" in data:
                    self._update_location_if_changed(float(data["latitude"]), float(data["longitude"]))
                    return
        except Exception as e:
            logger.warning(f"[LOCATION] Fallback 1 API (freeipapi.com) failed: {e}. Trying fallback 2...")
            
        # Fallback 2
        try:
            req = urllib.request.Request("https://ipapi.co/json/", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                if "latitude" in data and "longitude" in data:
                    self._update_location_if_changed(float(data["latitude"]), float(data["longitude"]))
                    return
        except Exception as e:
            logger.error(f"[LOCATION] Fallback 2 API (ipapi.co) failed: {e}. All location APIs failed.")

    def _update_location_if_changed(self, lat: float, lon: float):
        old_lat = self.settings.get("latitude", 13.08)
        old_lon = self.settings.get("longitude", 80.27)
        if abs(old_lat - lat) > 0.01 or abs(old_lon - lon) > 0.01:
            logger.info(f"[LOCATION] Geolocation updated: ({old_lat}, {old_lon}) -> ({lat}, {lon})")
            self.settings["latitude"] = lat
            self.settings["longitude"] = lon
            save_settings(self.settings)
            
            # Re-trigger color temp update
            threading.Thread(target=self._update_color_temp, daemon=True).start()
            
            # Sync GUI if Settings Window is open
            if hasattr(self, "_settings_window") and self._settings_window:
                try:
                    # Check if the settings window top-level exists and entries is populated
                    if "latitude" in self._settings_window.entries:
                        self._settings_window.entries["latitude"][0].set(str(lat))
                    if "longitude" in self._settings_window.entries:
                        self._settings_window.entries["longitude"][0].set(str(lon))
                except Exception as e:
                    logger.debug(f"Could not sync location to settings GUI: {e}")

    def _start_udp_listener(self):
        def _listen():
            logger.info("HealthApp UDP Listener starting on bound port 5098")
            while self._running:
                try:
                    data, addr = self.udp_sock.recvfrom(1024)
                    msg = data.decode("utf-8").strip()
                    if msg == "game_mode:on" and not self._game_mode:
                        logger.info(
                            "[UDP] Game Mode activated. Shifting to low-resource mode..."
                        )
                        self._game_mode = True
                        self._set_self_priority("idle")
                    elif msg == "game_mode:off" and self._game_mode:
                        logger.info(
                            "[UDP] Game Mode deactivated. Restoring normal mode..."
                        )
                        self._game_mode = False
                        self._set_self_priority("normal")
                except Exception as e:
                    if self._running:
                        logger.error(f"Error in UDP listener: {e}")

            try:
                self.udp_sock.close()
            except Exception:
                pass

        threading.Thread(target=_listen, daemon=True).start()

    def _process_gui_queue(self):
        while not self.gui_queue.empty():
            try:
                action, data = self.gui_queue.get_nowait()
                if action == "settings":
                    self._settings_window = SettingsWindow(
                        self.root, dict(self.settings), self._on_settings_saved, app=self
                    )
                    self._settings_window.show()
                elif action == "warning":
                    msg, duration = data
                    if hasattr(self, "_active_warning_toast") and self._active_warning_toast:
                        try:
                            self._active_warning_toast.force_close()
                        except Exception:
                            pass
                    self._active_warning_toast = WarningToast(
                        self.root, msg, duration, self.settings
                    )
                    self._active_warning_toast.show()
                elif action == "health_toast":
                    from services.aerohub_core.toast_utils import is_in_break_period_shared
                    if is_in_break_period_shared():
                        logger.info("Discarding health tip action during break period.")
                        continue
                    
                    toast_settings = dict(self.settings)
                    
                    # Apply Night Mode overrides if within night hours
                    nc_start = self.settings.get("nc_start_time", "23:59")
                    nc_end = self.settings.get("nc_end_time", "06:00")
                    if _is_time_between(nc_start, nc_end):
                        if "ht_night_duration_sec" in self.settings:
                            toast_settings["ht_duration_sec"] = self.settings["ht_night_duration_sec"]
                        if "ht_night_toast_pos" in self.settings:
                            toast_settings["ht_toast_pos"] = self.settings["ht_night_toast_pos"]

                    BaseToast(
                        self.root, "Health Tip", data, toast_settings, is_health_tip=True
                    ).show()
                elif action == "brightness_care":
                    from services.aerohub_core.toast_utils import is_in_break_period_shared
                    if is_in_break_period_shared():
                        logger.info("Discarding brightness care action during break period.")
                        continue
                    is_agg = data.get("is_aggressive", False) if data else False
                    BrightnessWarningToast(
                        self.root,
                        self.settings,
                        on_skip=self._skip_brightness_warning,
                        on_decrease=lambda agg=is_agg: self._decrease_brightness(agg),
                    ).show()
                elif action == "night_care_toast":
                    from services.aerohub_core.toast_utils import is_in_break_period_shared
                    if is_in_break_period_shared():
                        logger.info("Discarding night care action during break period.")
                        continue
                    temp_settings = dict(self.settings)
                    for k, v in self.settings.items():
                        if k.startswith("nc_toast_"):
                            suffix = k[len("nc_toast_"):]
                            temp_settings[f"toast_{suffix}"] = v
                    temp_settings["toast_enable_sound"] = self.settings.get(
                        "nc_toast_enable_sound", True
                    )
                    temp_settings["toast_sound_effect"] = self.settings.get(
                        "nc_toast_sound_effect", "mac_connect"
                    )
                    temp_settings["toast_duration"] = self.settings.get(
                        "nc_duration", 6
                    )
                    BaseToast(
                        self.root,
                        "Night Care",
                        data,
                        temp_settings,
                        is_health_tip=False,
                    ).show()
                elif action == "screen_flick":
                    from services.aerohub_core.toast_utils import is_in_break_period_shared
                    if is_in_break_period_shared():
                        continue
                    if data:
                        self._play_screen_flick(data.get("hold_sec", 1.0), data.get("fade_sec", 3.0))
                elif action == "break":
                    break_type, duration, completion_event, result = data

                    # Set break_active = True and break_pid in shared status
                    from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
                    status = read_shared_status()
                    status["break_active"] = True
                    status["break_pid"] = os.getpid()
                    status["break_end_time"] = time.time() + duration
                    write_shared_status(status)

                    # Close active warning toast on break start
                    if hasattr(self, "_active_warning_toast") and self._active_warning_toast:
                        try:
                            self._active_warning_toast.force_close()
                        except Exception:
                            pass
                        self._active_warning_toast = None

                    def on_overlay_complete(status_result):
                        from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
                        st = read_shared_status()
                        st["break_active"] = False
                        st["break_pid"] = None
                        st["break_end_time"] = 0.0
                        st["break_warning_active"] = False
                        st["break_warning_pid"] = None
                        st["break_warning_end_time"] = 0.0
                        st["last_break_end_time"] = time.time()
                        write_shared_status(st)

                        result["status"] = status_result
                        completion_event.set()

                    BreakOverlay(
                        self.root,
                        duration,
                        break_type,
                        self.settings,
                        on_overlay_complete,
                    ).show()
            except Exception as e:
                logger.error(f"Error processing GUI queue: {e}")

        if self._running:
            self.root.after(100, self._process_gui_queue)

    def run(self):
        logger.info("=" * 50)
        logger.info("Health App starting...")

        # Single instance check: try to bind to UDP port 5098 synchronously on the main thread
        import socket

        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.udp_sock.bind(("127.0.0.1", 5098))
        except Exception as e:
            logger.warning(
                f"Another instance of Health App is already running (failed to bind port 5098: {e}). Exiting."
            )
            print("Another instance of Health App is already running. Exiting.")
            import os

            os._exit(1)  # Exit with error so AeroHub will auto-restart us

        self._start_udp_listener()
        system_utils.monitor_parent_process(lambda: self._on_quit(self.tray_icon, None))
        logger.info(f"Settings: {json.dumps(self.settings, indent=2)}")

        generate_breathing_sound()
        ensure_sound_effects()

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
                pystray.MenuItem("⚙️ Settings", self._on_settings, default=True),
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

        health_toast_thread = threading.Thread(
            target=self._health_toast_loop, daemon=True
        )
        health_toast_thread.start()

        bc_thread = threading.Thread(target=self._brightness_care_loop, daemon=True)
        bc_thread.start()

        nc_thread = threading.Thread(target=self._night_care_loop, daemon=True)
        nc_thread.start()

        location_check_thread = threading.Thread(target=self._location_check_loop, daemon=True)
        location_check_thread.start()

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
        elif (
            len(sys.argv) > 2
            and sys.argv[1] == "/debug:break"
            and sys.argv[2] == "screen"
        ):
            is_debug_break = True

    if is_debug_break:
        generate_breathing_sound()
        ensure_sound_effects()

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
```

---

### File: `settings.json`
- **Path:** `settings.json`
- **Estimated Tokens:** 1,570
- **mtime:** 1781376776.281

```json
{
  "short_break_interval_min": 15,
  "short_break_duration_sec": 30,
  "long_break_interval_min": 40,
  "long_break_duration_sec": 40,
  "pre_warning_sec": 30,
  "enable_sound": true,
  "enable_dimming": false,
  "enable_weather_warmth": true,
  "latitude": 11.6602,
  "longitude": 78.1532,
  "paused": false,
  "night_light_start_hour": 18,
  "night_light_end_hour": 6,
  "run_during_game": true,
  "toast_pos": "Top-Center",
  "toast_custom_x": 100,
  "toast_custom_y": 100,
  "toast_width": 210,
  "toast_height": 70,
  "toast_bg_color": "#ffffff",
  "toast_fg_color": "#080808",
  "toast_accent_color": "#3fb5fc",
  "toast_font_size": 10,
  "toast_font_weight": "bold",
  "toast_font_family": "Segoe UI",
  "toast_emoji": "\u25d5\u203f\u25d5",
  "toast_radius": 8,
  "toast_padding_x": 10,
  "toast_padding_y": 15,
  "toast_anim_style": "Slide",
  "toast_opacity": 1.0,
  "toast_border_width": 1,
  "toast_border_color": "#020202",
  "toast_gradient": false,
  "toast_gradient_end": "#101625",
  "toast_shadow": true,
  "toast_accent_stripe": false,
  "toast_text_align": "center",
  "toast_auto_dismiss": true,
  "toast_click_action": "dismiss",
  "toast_progress_bar": true,
  "toast_enable_sound": true,
  "toast_sound_effect": "bubble_pop",
  "toast_volume": 100,
  "toast_border_style": "Solid",
  "toast_stripe_pos": "Bottom",
  "wellness_points": 600,
  "current_streak": 0,
  "ht_enabled": true,
  "ht_interval_min": 5,
  "ht_duration_sec": 6,
  "ht_night_enabled": true,
  "ht_night_interval_min": 30,
  "ht_night_duration_sec": 8,
  "ht_night_toast_pos": "Top-Right",
  "ht_cat_breathing": true,
  "ht_cat_eye_care": true,
  "ht_cat_posture": true,
  "ht_cat_stretch": true,
  "ht_cat_hydration": true,
  "ht_cat_mental": true,
  "ht_cat_hands_wrists": true,
  "ht_toast_pos": "Top-Center",
  "ht_toast_custom_x": 100,
  "ht_toast_custom_y": 100,
  "ht_toast_width": 250,
  "ht_toast_height": 70,
  "ht_toast_bg_color": "#ffff04",
  "ht_toast_fg_color": "#000000",
  "ht_toast_accent_color": "#7f7f7f",
  "ht_toast_font_size": 10,
  "ht_toast_font_weight": "normal",
  "ht_toast_font_family": "Segoe UI",
  "ht_toast_emoji": "\u26a1",
  "ht_toast_radius": 18,
  "ht_toast_padding_x": 12,
  "ht_toast_padding_y": 10,
  "ht_toast_anim_style": "Typewriter",
  "ht_toast_opacity": 0.95,
  "ht_toast_border_width": 1,
  "ht_toast_border_color": "#1a1a2e",
  "ht_toast_gradient": true,
  "ht_toast_gradient_end": "#101625",
  "ht_toast_shadow": true,
  "ht_toast_accent_stripe": false,
  "ht_toast_text_align": "left",
  "ht_toast_auto_dismiss": true,
  "ht_toast_click_action": "dismiss",
  "ht_toast_progress_bar": true,
  "ht_toast_enable_sound": true,
  "ht_toast_sound_effect": "zen_bowl",
  "ht_toast_volume": 80,
  "ht_toast_border_style": "Solid",
  "ht_toast_stripe_pos": "Left",
  "bc_enabled": true,
  "bc_start_time": "23:00",
  "bc_end_time": "06:00",
  "bc_target_brightness": 10,
  "bc_duration_minutes": 30,
  "bc_aggressive_target_brightness": 15,
  "bc_aggressive_duration_minutes": 5,
  "bc_transition_time_sec": 5,
  "bc_aggressive_transition_time_sec": 90,
  "bc_safe_brightness": 8,
  "bc_safe_duration_seconds": 120,
  "bc_toast_enable_sound": true,
  "bc_toast_sound_effect": "crystal_bell",
  "bc_toast_width": 280,
  "bc_toast_height": 125,
  "bc_toast_bg_color": "#ffffff",
  "bc_toast_fg_color": "#ff8448",
  "bc_toast_accent_color": "#590000",
  "bc_toast_border_width": 1,
  "bc_toast_border_color": "#000000",
  "bc_toast_radius": 16,
  "bc_toast_gradient": false,
  "bc_toast_gradient_end": "#00ff40",
  "bc_toast_shadow": false,
  "bc_toast_accent_stripe": false,
  "bc_toast_text_align": "left",
  "bc_toast_progress_bar": false,
  "bc_toast_click_action": "dismiss",
  "bc_toast_border_style": "Solid",
  "bc_toast_stripe_pos": "Left",
  "bc_toast_volume": 100,
  "bc_toast_opacity": 0.95,
  "bc_toast_emoji": "\u26a0\ufe0f",
  "bc_toast_padding_x": 12,
  "bc_toast_padding_y": 10,
  "nc_enabled": true,
  "nc_start_time": "23:59",
  "nc_end_time": "06:00",
  "nc_interval_minutes": 3,
  "nc_flick_enabled": true,
  "nc_flick_hold_sec": 0.5,
  "nc_flick_fade_sec": 0.5,
  "nc_slogans": "It's late. Your body needs rest. \ud83c\udf19|Go to sleep. Tomorrow is a new day. \ud83d\udca4|Screen time is over. Time for dream time. \u2728|Rest your eyes and your mind. \ud83d\udecc|Sleep is the best meditation. \ud83e\uddd8",
  "nc_toast_width": 250,
  "nc_toast_height": 40,
  "nc_toast_bg_color": "#ffffff",
  "nc_toast_fg_color": "#080808",
  "nc_toast_accent_color": "#58a6ff",
  "nc_toast_font_size": 12,
  "nc_toast_font_weight": "bold",
  "nc_toast_font_family": "Segoe UI",
  "nc_toast_emoji": "\ud83c\udf19",
  "nc_toast_radius": 18,
  "nc_toast_padding_x": 6,
  "nc_toast_padding_y": 22,
  "nc_toast_anim_style": "Slide",
  "nc_toast_opacity": 0.95,
  "nc_toast_border_width": 2,
  "nc_toast_border_color": "#30363d",
  "nc_toast_enable_sound": true,
  "nc_toast_sound_effect": "echo_ping",
  "nc_toast_gradient": false,
  "nc_toast_gradient_end": "#101625",
  "nc_toast_shadow": true,
  "nc_toast_accent_stripe": false,
  "nc_toast_text_align": "center",
  "nc_toast_progress_bar": true,
  "nc_toast_click_action": "dismiss",
  "nc_toast_border_style": "Dashed",
  "nc_toast_stripe_pos": "Bottom",
  "nc_toast_volume": 80,
  "nl_enabled": true,
  "nl_day_temp": 2500,
  "nl_night_temp": 2900,
  "nl_transition_duration": 25,
  "break_audio_source": "random",
  "voice_prompts_enabled": true,
  "voice_inhale_sec": 4,
  "voice_hold_in_sec": 4,
  "voice_exhale_sec": 4,
  "voice_hold_out_sec": 0,
  "voice_volume": 100,
  "voice_rate": 0,
  "voice_inhale_text": "Breathe in",
  "voice_exhale_text": "Breathe out",
  "voice_hold_in_text": "Hold",
  "voice_hold_out_text": "Hold",
  "voice_break_type": "Both",
  "voice_min_duration_sec": 15,
  "voice_name": "Microsoft Hazel Desktop - English (Great Britain)",
  "location_check_interval_hours": 1,
  "toast_show_clock": true,
  "ht_toast_show_clock": true,
  "bc_toast_anim_style": "Slide",
  "bc_toast_pos": "Left",
  "nc_toast_pos": "Left",
  "toast_transition_time_ms": 2000,
  "toast_duration_sec": 2000,
  "ht_toast_transition_time_ms": 2000,
  "bc_toast_duration_sec": 5,
  "bc_toast_transition_time_ms": 3000,
  "nc_toast_duration_sec": 10,
  "nc_toast_transition_time_ms": 1500
}
```

---

### File: `test_preview.py`
- **Path:** `test_preview.py`
- **Estimated Tokens:** 446
- **mtime:** 1781270919.237

```python
import sys
import tkinter as tk

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)
from health_app import HealthApp  # noqa: E402
from ui.settings_ui import SettingsWindow  # noqa: E402



def test_preview_window():
    root = tk.Tk()
    root.withdraw()
    try:
        app = HealthApp()
        app.root = root
        sw = SettingsWindow(root, app.settings, lambda x: print("saved", x), app=app)
        sw.show()

        # Test creating SettingsWindow without mainloop blocking
        assert sw is not None
        assert sw.parent is not None

        # Verify triggering desktop previews for each tab to catch any NameErrors/crashes
        sw._show_desktop_preview_for_tab("📅 Schedule") # Should return None gracefully
        sw._show_desktop_preview_for_tab("✨ Toast FX")
        sw._show_desktop_preview_for_tab("💡 Health Toast")
        sw._show_desktop_preview_for_tab("🔆 Brightness Care")
        sw._show_desktop_preview_for_tab("🌙 Night Care")
    finally:
        root.destroy()


if __name__ == "__main__":
    # Interactive manual preview
    root = tk.Tk()
    root.withdraw()
    app = HealthApp()
    app.root = root

    def run_interactive():
        sw = SettingsWindow(root, app.settings, lambda x: print("saved", x))
        sw.entries = {}
        for k in app.settings:
            v = tk.StringVar(value=str(app.settings[k]))
            sw.entries[k] = (
                v,
                True
                if isinstance(app.settings[k], bool)
                else (True if isinstance(app.settings[k], str) else False),
            )
        sw._show_desktop_preview_for_tab("General")
        root.destroy()

    root.after(100, run_interactive)
    root.mainloop()
```

---

### File: `tests/test_health_app.py`
- **Path:** `tests/test_health_app.py`
- **Estimated Tokens:** 2,570
- **mtime:** 1781116938.742

```python
import sys
import os

if "TCL_LIBRARY" not in os.environ:
    local_tcl = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs",
        "Python",
        "Python312",
        "tcl",
        "tcl8.6",
    )
    if os.path.isdir(local_tcl):
        os.environ["TCL_LIBRARY"] = local_tcl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
import datetime  # noqa: E402
from unittest.mock import patch  # noqa: E402
from core.gamma import kelvin_to_rgb, _is_night_hour  # noqa: E402
from health_app import HealthApp  # noqa: E402


def test_kelvin_to_rgb():
    # Test valid conversions
    r, g, b = kelvin_to_rgb(6500)
    assert r == 255 and g >= 250 and b >= 250

    r, g, b = kelvin_to_rgb(4000)
    assert r == 255 and g > 200 and b < 200  # Roughly warm

    # Test bounds
    r, g, b = kelvin_to_rgb(1000)
    assert r == 255 and g < 100 and b == 0


def test_is_night_hour():
    assert _is_night_hour(20, 18, 6) is True
    assert _is_night_hour(23, 18, 6) is True
    assert _is_night_hour(3, 18, 6) is True
    assert _is_night_hour(5, 18, 6) is True
    assert _is_night_hour(7, 18, 6) is False
    assert _is_night_hour(12, 18, 6) is False


@pytest.fixture
def app():
    with (
        patch(
            "health_app.load_settings",
            return_value={"bc_enabled": True, "nc_enabled": True},
        ),
        patch("health_app.generate_breathing_sound"),
        patch("health_app.get_media_controller"),
        patch(
            "health_app.system_utils.is_system_awake_and_unlocked", return_value=True
        ),
    ):
        # Instantiate safely without launching TK mainloop
        return HealthApp()


def test_is_time_in_range(app):
    # Test time within range overlapping midnight
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(23, 30)
        assert app._is_time_in_range("23:00", "06:00") is True

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(2, 0)
        assert app._is_time_in_range("23:00", "06:00") is True

    # Test time outside range overlapping midnight
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(12, 0)
        assert app._is_time_in_range("23:00", "06:00") is False

    # Test normal range (not overlapping midnight)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(14, 0)
        assert app._is_time_in_range("13:00", "15:00") is True

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(16, 0)
        assert app._is_time_in_range("13:00", "15:00") is False

    # Test invalid time format
    assert app._is_time_in_range("invalid", "format") is False


def test_default_settings_keys():
    from health_app import DEFAULT_SETTINGS

    assert DEFAULT_SETTINGS.get("nl_enabled") is True
    assert DEFAULT_SETTINGS.get("nl_day_temp") == 6500
    assert DEFAULT_SETTINGS.get("nl_night_temp") == 3500
    assert DEFAULT_SETTINGS.get("nl_transition_duration") == 20


def test_update_color_temp_disabled(app):
    app.settings["nl_enabled"] = False
    with patch("health_app.apply_gamma_ramp"):
        app._update_color_temp()
        assert app._current_kelvin == 6500
        assert app._target_kelvin_actual == 6500.0


def test_update_color_temp_enabled(app):
    app.settings["nl_enabled"] = True
    app.settings["nl_day_temp"] = 6000
    app.settings["nl_night_temp"] = 3000
    app.settings["enable_weather_warmth"] = False

    with (
        patch("health_app._is_night_hour", return_value=False),
        patch("health_app.apply_gamma_ramp"),
    ):
        app._update_color_temp()
        assert app._current_kelvin == 6000
        assert app._target_kelvin_actual == 6000.0

    with (
        patch("health_app._is_night_hour", return_value=True),
        patch("health_app.apply_gamma_ramp"),
    ):
        app._update_color_temp()
        assert app._current_kelvin == 3000
        assert app._target_kelvin_actual == 3000.0


def test_timer_synchronization(app):
    app.settings["short_break_interval_min"] = 20
    app.settings["long_break_interval_min"] = 60
    # Test settings save synchronization
    app._last_short_break = 100.0
    app._last_long_break = 200.0
    
    with patch("health_app.save_settings"), patch("health_app.apply_gamma_ramp"):
        app._on_settings_saved(dict(app.settings))
        
        # Check that they were reset to the same time
        assert abs(app._last_short_break - app._last_long_break) < 0.01
        assert app._short_warn_shown is False
        assert app._long_warn_shown is False

    # Test lock screen unlock synchronization
    app._last_short_break = 50.0
    app._last_long_break = 150.0
    
    with patch("health_app.is_workstation_locked", side_effect=[True, False]), patch("time.sleep"):
        # Trigger the lock handler
        result = app._handle_lock_screen(12345.0)
        assert result is True
        # Check that they were synchronized to the same time
        assert abs(app._last_short_break - app._last_long_break) < 0.01


def test_box_breathing_overlay_cycle():
    from ui.overlay import BreakOverlay
    import tkinter as tk
    from unittest.mock import MagicMock

    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tkinter/Tcl not fully configured on this system")

    settings = {
        "voice_prompts_enabled": True,
        "voice_inhale_sec": 4,
        "voice_hold_in_sec": 2,
        "voice_exhale_sec": 3,
        "voice_hold_out_sec": 1,
        "voice_inhale_text": "Inhale",
        "voice_exhale_text": "Exhale",
        "voice_hold_in_text": "Hold In",
        "voice_hold_out_text": "Hold Out",
        "voice_volume": 80,
        "voice_rate": 0,
        "voice_break_type": "Both",
        "voice_min_duration_sec": 5,
        "voice_name": "Default",
    }

    on_complete = MagicMock()
    overlay = BreakOverlay(root, duration_sec=20, break_type="short", settings=settings, on_complete=on_complete)

    # Initialize Mocks for Tkinter variables and windows
    overlay._countdown_var = MagicMock()
    overlay._breathing_var = MagicMock()
    overlay._breathing_label = MagicMock()
    overlay.window = MagicMock()

    # Test total cycle duration calculation
    T = overlay._inhale_sec + overlay._hold_in_sec + overlay._exhale_sec + overlay._hold_out_sec
    assert T == 10

    # Mock _speak_phase to assert custom text triggers
    overlay._speak_phase = MagicMock()

    # We manually tick the countdown at different remaining times (duration_sec = 20)
    # cycle = (duration_sec - remaining) % T

    # 1. remaining = 20 (cycle = 0): Inhale start
    overlay._remaining = 20
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Breathe In... 🌬️")
    overlay._speak_phase.assert_called_with("Inhale")
    overlay._speak_phase.reset_mock()

    # 2. remaining = 18 (cycle = 2): Inhale middle
    overlay._remaining = 18
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Breathe In... 🌬️")
    # Should not speak again in middle of phase
    overlay._speak_phase.assert_not_called()

    # 3. remaining = 16 (cycle = 4): Hold In start
    overlay._remaining = 16
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Hold... 🛑")
    overlay._speak_phase.assert_called_with("Hold In")
    overlay._speak_phase.reset_mock()

    # 4. remaining = 14 (cycle = 6): Exhale start
    overlay._remaining = 14
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Breathe Out... 💨")
    overlay._speak_phase.assert_called_with("Exhale")
    overlay._speak_phase.reset_mock()

    # 5. remaining = 11 (cycle = 9): Hold Out start
    overlay._remaining = 11
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Hold... 🛑")
    overlay._speak_phase.assert_called_with("Hold Out")
    overlay._speak_phase.reset_mock()

    root.destroy()


def test_speak_voice_prompts_conditions():
    from ui.overlay import BreakOverlay
    import tkinter as tk
    from unittest.mock import MagicMock

    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tkinter/Tcl not fully configured on this system")

    settings = {
        "voice_prompts_enabled": True,
        "voice_inhale_sec": 4,
        "voice_hold_in_sec": 2,
        "voice_exhale_sec": 3,
        "voice_hold_out_sec": 1,
        "voice_break_type": "Long Only",
        "voice_min_duration_sec": 15,
        "voice_name": "Default",
    }

    on_complete = MagicMock()
    
    # Condition: voice_break_type is Long Only but break is Short -> should be False
    overlay_short = BreakOverlay(root, duration_sec=30, break_type="short", settings=settings, on_complete=on_complete)
    assert overlay_short._should_speak_voice() is False

    # Condition: voice_break_type is Long Only, break is Long, duration is 30 -> should be True
    overlay_long = BreakOverlay(root, duration_sec=30, break_type="long", settings=settings, on_complete=on_complete)
    assert overlay_long._should_speak_voice() is True

    # Condition: duration is 10 (less than voice_min_duration_sec = 15) -> should be False
    overlay_long_short_dur = BreakOverlay(root, duration_sec=10, break_type="long", settings=settings, on_complete=on_complete)
    assert overlay_long_short_dur._should_speak_voice() is False

    # Condition: disabled in settings -> should be False
    settings_disabled = dict(settings)
    settings_disabled["voice_prompts_enabled"] = False
    overlay_disabled = BreakOverlay(root, duration_sec=30, break_type="long", settings=settings_disabled, on_complete=on_complete)
    assert overlay_disabled._should_speak_voice() is False

    root.destroy()


def test_get_sapi_voices_fallback():
    from core.audio import get_sapi_voices
    voices = get_sapi_voices()
    assert isinstance(voices, list)
    assert len(voices) >= 1

```

---

### File: `ui/__init__.py`
- **Path:** `ui/__init__.py`
- **Estimated Tokens:** 5
- **mtime:** 1781114456.469

```python
# HealthApp UI package
```

---

### File: `ui/overlay.py`
- **Path:** `ui/overlay.py`
- **Estimated Tokens:** 3,040
- **mtime:** 1781270763.961

```python
import os
import tkinter as tk
from core.logger import logger
from core.constants import TH
from core.media import get_media_controller
from core.audio import select_break_audio, pygame, PYGAME_AVAILABLE
from ui.theme import _add_hover

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BreakOverlay:
    """Full-screen black overlay on all monitors with countdown and breathing text."""

    def __init__(
        self, parent, duration_sec: int, break_type: str, settings: dict, on_complete
    ):
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

        self._voice_enabled = self.settings.get("voice_prompts_enabled", False)
        self._inhale_sec = int(self.settings.get("voice_inhale_sec", 4))
        self._hold_in_sec = int(self.settings.get("voice_hold_in_sec", 4))
        self._exhale_sec = int(self.settings.get("voice_exhale_sec", 4))
        self._hold_out_sec = int(self.settings.get("voice_hold_out_sec", 4))

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
            main_frame,
            text=type_text,
            font=("Segoe UI", 20),
            fg=TH["accent"],
            bg="black",
        ).pack(pady=(0, 20))

        self._countdown_var = tk.StringVar(value=str(self.duration))
        tk.Label(
            main_frame,
            textvariable=self._countdown_var,
            font=("Segoe UI Light", 96, "bold"),
            fg="white",
            bg="black",
        ).pack(pady=(0, 20))

        self._breathing_var = tk.StringVar(value="Breathe In...")
        self._breathing_label = tk.Label(
            main_frame,
            textvariable=self._breathing_var,
            font=("Segoe UI", 24),
            fg=TH["fg_dim"],
            bg="black",
        )
        self._breathing_label.pack(pady=(0, 10))

        btn_frame = tk.Frame(main_frame, bg="black")
        btn_frame.pack(pady=10)

        btn_skip = tk.Button(
            btn_frame,
            text="Skip ⏭",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg=TH["fg_dim"],
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=TH["bg2"],
            activeforeground="white",
            padx=20,
            pady=8,
            command=self._skip_break,
        )
        btn_skip.pack(side=tk.LEFT, padx=10)

        btn_postpone = tk.Button(
            btn_frame,
            text="Postpone (2m) ⏰",
            font=("Segoe UI", 12, "bold"),
            bg=TH["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=TH["accent_hover"],
            activeforeground="white",
            padx=20,
            pady=8,
            command=self._postpone_break,
        )
        btn_postpone.pack(side=tk.LEFT, padx=10)

        _add_hover(btn_skip, "#1a1a2e", TH["bg2"], TH["fg_dim"], "white")
        _add_hover(btn_postpone, TH["accent"], TH["accent_hover"])

        tk.Label(
            main_frame,
            text="Look away from the screen • Focus on something 20ft away",
            font=("Segoe UI", 12),
            fg="#444",
            bg="black",
        ).pack(pady=(20, 0))

    def _skip_break(self):
        self.status = "skipped"
        logger.info("Break skipped by user action.")
        self._cleanup()

    def _postpone_break(self):
        self.status = "postponed"
        logger.info("Break postponed by user action.")
        self._cleanup()

    def _restore(self):
        # Implement restore logic in case of failure or overlay close
        pass

    def _start_countdown(self):
        self._remaining = self.duration
        self._tick_countdown()

    def _tick_countdown(self):
        if self._remaining > 0:
            try:
                self._countdown_var.set(str(self._remaining))

                T = max(1, self._inhale_sec + self._hold_in_sec + self._exhale_sec + self._hold_out_sec)
                cycle = (self.duration - self._remaining) % T

                if cycle < self._inhale_sec:
                    self._breathing_var.set("Breathe In... 🌬️")
                    self._breathing_label.config(fg=TH["success"])
                    if cycle == 0:
                        self._speak_phase(self.settings.get("voice_inhale_text", "Breathe in"))
                elif cycle < self._inhale_sec + self._hold_in_sec:
                    self._breathing_var.set("Hold... 🛑")
                    self._breathing_label.config(fg=TH["warning"])
                    if cycle == self._inhale_sec:
                        self._speak_phase(self.settings.get("voice_hold_in_text", "Hold"))
                elif cycle < self._inhale_sec + self._hold_in_sec + self._exhale_sec:
                    self._breathing_var.set("Breathe Out... 💨")
                    self._breathing_label.config(fg=TH["accent"])
                    if cycle == self._inhale_sec + self._hold_in_sec:
                        self._speak_phase(self.settings.get("voice_exhale_text", "Breathe out"))
                else:
                    self._breathing_var.set("Hold... 🛑")
                    self._breathing_label.config(fg=TH["fg_dim"])
                    if cycle == self._inhale_sec + self._hold_in_sec + self._exhale_sec:
                        self._speak_phase(self.settings.get("voice_hold_out_text", "Hold"))

                self._remaining -= 1
                self.window.after(1000, self._tick_countdown)
            except tk.TclError:
                pass
        else:
            self._cleanup()

    def _should_speak_voice(self) -> bool:
        if not self._voice_enabled:
            return False
        
        # Check break type filter
        vt = self.settings.get("voice_break_type", "Both")
        if vt == "Short Only" and self.break_type != "short":
            return False
        if vt == "Long Only" and self.break_type != "long":
            return False
            
        # Check duration threshold
        min_dur = int(self.settings.get("voice_min_duration_sec", 15))
        if self.duration < min_dur:
            return False
            
        return True

    def _speak_phase(self, text):
        if self._should_speak_voice():
            from core.audio import speak_sapi_async
            voice_name = self.settings.get("voice_name", "Default")
            volume = int(self.settings.get("voice_volume", 80))
            rate = int(self.settings.get("voice_rate", 0))
            speak_sapi_async(text, voice_name, volume, rate)

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
                    logger.warning(
                        "Focus repeatedly lost. Applying windowed borderless fallback..."
                    )
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
            # Auto-resume media that was playing right before the break
            try:
                get_media_controller().resume_paused_media()
                logger.info("Executed resume for paused media sessions on break end.")
            except Exception as e:
                logger.error(f"Error resuming media on break end: {e}")

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

                    sound_path = os.path.join(
                        APP_ROOT, "resources", "on_stop_break.wav"
                    )
                    if os.path.exists(sound_path):
                        winsound.PlaySound(
                            sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
                        )
                except Exception:
                    pass
            if self.on_complete:
                self.on_complete(self.status)
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
```

---

### File: `ui/settings_ui.py`
- **Path:** `ui/settings_ui.py`
- **Estimated Tokens:** 15,355
- **mtime:** 1781288700.902

```python
import os
import time
import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import ImageTk

from core.logger import logger
from core.constants import TH, DEFAULT_SETTINGS, HEALTH_TIPS, SOUND_EFFECTS
from core.settings import save_settings
from core.gamma import apply_gamma_ramp
from ui.theme import _add_hover, apply_dwm_rounding, create_health_icon
from ui.toast import BrightnessWarningToast, WarningToast
from services.aerohub_core.toast_utils import BaseToast
from core.audio import get_sapi_voices

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SettingsWindow:
    def __init__(self, parent, settings: dict, on_save, app=None):
        self.parent = parent
        self.settings = settings
        self.on_save = on_save
        self.app = app
        self.entries = {}
        self.frames = {}
        self.live_preview_toast = None
        self.live_preview_tab = None

        # Pre-populate location check interval display value
        interval_map = {0: "Disabled", 1: "Every Hour", 2: "Every 2 Hours", 6: "Every 6 Hours", 12: "Every 12 Hours", 24: "Every 24 Hours"}
        val = self.settings.get("location_check_interval_hours", 1)
        self.settings["location_check_interval_display"] = interval_map.get(val, "Every Hour")

    def show(self):
        self._create()

    def _create(self):
        root = tk.Toplevel(self.parent)
        root.transient(None)
        root.title("SYSTEM OVERRIDE // HEALTH CONFIG")
        root.configure(bg=TH["bg"])
        root.resizable(True, True)

        try:
            icon_img = create_health_icon()
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(False, self.icon_photo)
        except Exception as e:
            logger.error(f"Failed to set window icon: {e}")

        try:
            apply_gamma_ramp(6500, log_action=False)  # Temp reset for configuration clarity
            apply_dwm_rounding(root)
        except Exception:
            pass

        def on_closing():
            try:
                self._save_silently()
            except Exception as e:
                logger.error(f"Error auto-saving settings on close: {e}")
                    
            if hasattr(self, "live_preview_toast") and self.live_preview_toast:
                try:
                    self.live_preview_toast.force_close()
                except Exception:
                    pass
                self.live_preview_toast = None
                
            for key in list(self.entries.keys()):
                try:
                    if key in self.entries:
                        var, var_type = self.entries.pop(key)
                        del var
                except Exception:
                    pass

            try:
                root.destroy()
            except Exception as e:
                logger.error(f"Error destroying root settings window: {e}")

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Centered settings window / maximized on start
        root.update_idletasks()
        w = 650
        h = 700
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.minsize(580, 600)
        try:
            root.state("zoomed")
        except Exception:
            pass

        # Main Layout: Sidebar (Left) and Content (Right)
        main_container = tk.Frame(root, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=210)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Title in Sidebar
        tk.Label(
            self.sidebar,
            text="HEALTH APP",
            font=("Segoe UI", 16, "bold"),
            bg=TH["bg2"],
            fg=TH["fg"],
        ).pack(pady=(32, 0))

        btn_restore = tk.Button(
            self.sidebar,
            text="Reset Defaults",
            font=("Segoe UI", 8, "underline"),
            bg=TH["bg2"],
            fg=TH["fg_dim"],
            activebackground=TH["bg2"],
            activeforeground=TH["danger"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._restore_defaults,
        )
        btn_restore.pack(pady=(0, 20))
        _add_hover(btn_restore, TH["bg2"], TH["bg2"], TH["fg_dim"], TH["danger"])
        
        # Zeigarnik Effect: Active Modules Dashboard
        self.status_frame = tk.Frame(self.sidebar, bg=TH["bg3"], padx=10, pady=10)
        self.status_frame.pack(fill=tk.X, padx=15, pady=(0, 20))
        
        tk.Label(self.status_frame, text="SYSTEM STATUS", font=("Consolas", 8, "bold"), bg=TH["bg3"], fg=TH["fg_dim"]).pack(anchor=tk.W)
        self.lbl_status_nl = tk.Label(self.status_frame, text="○ Night Light", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_nl.pack(anchor=tk.W, pady=(4, 0))
        self.lbl_status_ht = tk.Label(self.status_frame, text="○ Health Tips", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_ht.pack(anchor=tk.W)
        self.lbl_status_bc = tk.Label(self.status_frame, text="○ Brightness Care", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_bc.pack(anchor=tk.W)
        self.lbl_status_nc = tk.Label(self.status_frame, text="○ Night Care", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_nc.pack(anchor=tk.W)

        # Content Area
        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frames = {}
        self.nav_buttons = {}
        self.current_frame = None
        self.current_frame_name = None

        self.nav_names = [
            "📅 Schedule",
            "✨ Toast FX",
            "💡 Health Toast",
            "🔆 Brightness Care",
            "🌙 Night Care",
        ]

        for name in self.nav_names:
            tab_container = tk.Frame(self.content_area, bg=TH["bg"])
            self.frames[name] = tab_container

            tab_container.columnconfigure(0, weight=1)
            tab_container.rowconfigure(0, weight=1)

            left_container = tk.Frame(tab_container, bg=TH["bg"])
            left_container.grid(row=0, column=0, sticky="nsew")

            scroll_frame = self._create_scrollable_tab(left_container)
            scroll_frame.columnconfigure(0, weight=1)
            scroll_frame.columnconfigure(1, weight=1)

            if name.endswith("Schedule"):
                self._build_schedule_tab(scroll_frame)
            elif name.endswith("Toast FX"):
                self._build_toast_tab(scroll_frame)
            elif name.endswith("Health Toast"):
                self._build_health_toast_tab(scroll_frame)
            elif name.endswith("Brightness Care"):
                self._build_brightness_care_tab(scroll_frame)
            elif name.endswith("Night Care"):
                self._build_night_care_tab(scroll_frame)

        def switch_tab(name):
            if hasattr(self, "live_preview_toast") and self.live_preview_toast:
                self._save_silently()
                try:
                    self.live_preview_toast.force_close()
                except Exception:
                    pass
                self.live_preview_toast = None

            if self.current_frame:
                self.current_frame.pack_forget()
                self._style_tab_button(self.current_frame_name, active=False)

            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            self._style_tab_button(name, active=True)
            self._on_settings_modified(is_tab_switch=True)

        # Navigation Buttons in Sidebar
        for name in self.nav_names:
            btn = tk.Button(
                self.sidebar,
                text=f"   {name}",
                font=("Segoe UI", 11, "bold"),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg3"],
                activeforeground=TH["fg"],
                relief=tk.FLAT,
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda n=name: switch_tab(n),
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

            def bind_tab_hover(b=btn, n=name):
                def on_enter(e):
                    if self.current_frame_name != n:
                        b.config(bg=TH["bg3"], fg=TH["fg"])
                def on_leave(e):
                    if self.current_frame_name != n:
                        b.config(bg=TH["bg2"], fg=TH["fg_dim"])
                b.bind("<Enter>", on_enter)
                b.bind("<Leave>", on_leave)
            bind_tab_hover()

        # Save Button in Sidebar (Bottom)
        self.btn_save = tk.Button(
            self.sidebar,
            text="Save Settings",
            font=("Segoe UI", 11, "bold"),
            bg=TH["accent"],
            fg="#000000",
            activebackground=TH["accent_hover"],
            activeforeground="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            pady=16,
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(5, 20))
        _add_hover(self.btn_save, TH["accent"], TH["accent_hover"], "#000000", "#000000")

        self.lbl_saved = tk.Label(
            self.sidebar, text="", font=("Segoe UI", 10, "bold"), bg=TH["bg2"], fg=TH["success"]
        )
        self.lbl_saved.pack(side=tk.BOTTOM, pady=(10, 0))



        # Play Preview Button in Sidebar
        self.btn_preview = tk.Button(
            self.sidebar,
            text="▶ Play Preview",
            font=("Segoe UI", 11, "bold"),
            bg=TH["bg3"],
            fg=TH["fg"],
            activebackground=TH["accent"],
            activeforeground="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            pady=16,
            command=self._play_preview_clicked,
        )
        self.btn_preview.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(5, 5))
        _add_hover(self.btn_preview, TH["bg3"], TH["accent"], TH["fg"], "#000000")

        # Upcoming Break countdown panel in sidebar
        upcoming_frame = tk.Frame(
            self.sidebar,
            bg=TH["bg"],
            highlightthickness=1,
            highlightbackground=TH["border"],
            padx=16,
            pady=16,
        )
        upcoming_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(10, 20))

        self.upcoming_title_label = tk.Label(
            upcoming_frame,
            text="UPCOMING BREAK",
            font=("Segoe UI", 9, "bold"),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor="w",
        )
        self.upcoming_title_label.pack(fill=tk.X, pady=(0, 6))

        self.upcoming_type_label = tk.Label(
            upcoming_frame,
            text="Short Break",
            font=("Segoe UI", 11, "bold"),
            bg=TH["bg"],
            fg=TH["accent"],
            anchor="w",
        )
        self.upcoming_type_label.pack(fill=tk.X)

        self.upcoming_time_label = tk.Label(
            upcoming_frame,
            text="00m 00s",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
            anchor="w",
        )
        self.upcoming_time_label.pack(fill=tk.X, pady=4)

        self.upcoming_clock_label = tk.Label(
            upcoming_frame,
            text="at --:--:--",
            font=("Segoe UI", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor="w",
        )
        self.upcoming_clock_label.pack(fill=tk.X)

        self._update_upcoming_break()

        switch_tab("📅 Schedule")

    def _style_tab_button(self, name, active):
        btn = self.nav_buttons[name]
        if active:
            btn.config(bg=TH["bg3"], fg=TH["accent"], text=f"●  {name[2:].strip()}")
        else:
            btn.config(bg=TH["bg2"], fg=TH["fg_dim"], text=f"   {name}")

    def _create_scrollable_tab(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)

        canvas = tk.Canvas(parent, bg=TH["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])

        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        def update_scrollregion(e=None):
            req_w = scrollable_frame.winfo_reqwidth()
            req_h = scrollable_frame.winfo_reqheight()
            canvas.configure(scrollregion=(0, 0, req_w, req_h))

            canvas_h = canvas.winfo_height()
            if req_h > canvas_h and canvas_h > 1:
                scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                scrollbar.grid_remove()

        scrollable_frame.bind("<Configure>", update_scrollregion)

        def _on_canvas_configure(e):
            canvas.itemconfig(canvas_window, width=e.width)
            req_h = scrollable_frame.winfo_reqheight()
            if req_h > e.height:
                scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                scrollbar.grid_remove()

        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(event):
            if scrollbar.winfo_ismapped():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        return scrollable_frame

    def _create_card(self, parent, title, row, col, rowspan=1, columnspan=1):
        card = tk.Frame(
            parent,
            bg=TH["bg2"],
            highlightthickness=1,
            highlightbackground=TH["border"],
            padx=20,
            pady=20,
        )
        card.grid(
            row=row,
            column=col,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky="nsew",
            padx=10,
            pady=10,
        )
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
            anchor=tk.W,
        ).pack(anchor=tk.W, pady=(0, 12))

        content_frame = tk.Frame(card, bg=TH["bg2"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        return card, content_frame

    def _add_field(self, parent_frame, label, key, row, col=0, is_str=False):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.StringVar(value=str(self.settings.get(key, "")))
        entry = tk.Entry(
            cell,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["fg"],
            relief=tk.FLAT,
        )
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.entries[key] = (var, is_str)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return entry

    def _add_slider_field(self, parent_frame, label, key, row, col=0, from_=0, to=100, resolution=1):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        val = self.settings.get(key, from_)
        try:
            val = float(val)
        except (ValueError, TypeError):
            val = float(from_)
        var = tk.DoubleVar(value=val)
        slider = tk.Scale(
            cell,
            variable=var,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            bg=bg,
            fg=TH["fg"],
            troughcolor=TH["bg"],
            highlightthickness=0,
            activebackground=TH["accent"],
            length=120,
            showvalue=True
        )
        slider.pack(side=tk.RIGHT)

        # Store as string variable to match standard format
        str_var = tk.StringVar(value=str(var.get()))
        def _update_str(*args):
            str_var.set(str(var.get()))
        var.trace_add("write", _update_str)

        self.entries[key] = (str_var, False)
        str_var.trace_add("write", lambda *args: self._on_settings_modified())
        return slider

    def _add_combo(self, parent_frame, label, key, row, values, col=0):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.StringVar(value=self.settings.get(key, values[0]))

        if key.endswith("_sound_effect"):
            prefix = key[:-len("sound_effect")]
            btn_test = tk.Button(
                cell,
                text="🔊",
                font=("Segoe UI Symbol", 8),
                bg=TH["bg3"],
                fg=TH["accent"],
                activebackground=TH["bg2"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                width=3,
                command=lambda k=key, p=prefix: self._test_sound_by_key_and_prefix(k, p)
            )
            btn_test.pack(side=tk.RIGHT, padx=(5, 0))
            _add_hover(btn_test, TH["bg3"], TH["bg2"], TH["accent"], TH["accent"])

        combo = ttk.Combobox(
            cell,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=14,
        )
        combo.pack(side=tk.RIGHT, padx=(10, 0))

        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return combo

    def _test_sound_by_key_and_prefix(self, key, prefix):
        if key in self.entries:
            snd_choice = self.entries[key][0].get()
        else:
            snd_choice = self.settings.get(key, "mac_connect")

        vol_key = f"{prefix}volume"
        if vol_key in self.entries:
            try:
                volume = float(self.entries[vol_key][0].get())
            except ValueError:
                volume = 80.0
        else:
            volume = float(self.settings.get(vol_key, 80))

        try:
            import winsound

            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]
            
            if snd_choice in system_aliases:
                winsound.PlaySound(snd_choice, winsound.SND_ALIAS | winsound.SND_ASYNC)
                return

            if not snd_choice.endswith(".wav"):
                snd_choice += ".wav"

            path = os.path.join(APP_ROOT, "resources", "sounds", snd_choice)
            if not os.path.exists(path):
                path = os.path.join(
                    os.path.dirname(APP_ROOT),
                    "BatteryMonitor",
                    "sounds",
                    snd_choice,
                )

            try:
                import pygame
                if pygame.mixer.get_init() and path and os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(volume / 100.0)
                    sound.play()
                    return
            except Exception:
                pass

            if os.path.exists(path):
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            logger.error(f"Error testing sound: {e}")

    def _add_color_field(self, parent_frame, label, key, row, col=0):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.StringVar(value=str(self.settings.get(key, "")))

        def choose_color(v=var):
            color_code = colorchooser.askcolor(
                title=f"Choose {label}", initialcolor=v.get()
            )[1]
            if color_code:
                v.set(color_code)
                self._on_settings_modified()

        btn = tk.Button(
            cell,
            bg=var.get() if var.get() else TH["accent"],
            width=3,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.pack(side=tk.RIGHT, padx=(10, 0))

        entry = tk.Entry(
            cell,
            textvariable=var,
            width=9,
            font=("Consolas", 10),
            bg=TH["bg3"],
            fg=TH["fg"],
            insertbackground=TH["fg"],
            relief=tk.FLAT,
        )
        entry.pack(side=tk.RIGHT)

        def _update_btn_bg(*args):
            try:
                # Basic validation for hex
                val = var.get().strip()
                if val.startswith("#") and len(val) in (4, 7):
                    btn.config(bg=val)
            except Exception:
                pass

        var.trace_add("write", _update_btn_bg)
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return entry

    def _create_toggle_canvas(self, parent, var):
        cv = tk.Canvas(
            parent, width=44, height=24, bg=parent.cget("bg"), highlightthickness=0
        )

        def draw_toggle(*args):
            cv.delete("all")
            state = var.get()
            color = TH["success"] if state else TH["border"]
            cv.create_oval(2, 2, 22, 22, fill=color, outline=color)
            cv.create_oval(22, 2, 42, 22, fill=color, outline=color)
            cv.create_rectangle(12, 2, 32, 22, fill=color, outline=color)
            if state:
                cv.create_oval(24, 4, 40, 20, fill="#ffffff", outline="#ffffff")
            else:
                cv.create_oval(4, 4, 20, 20, fill="#ffffff", outline="#ffffff")

        draw_toggle()

        def toggle(e=None):
            var.set(not var.get())
            draw_toggle()
            self._on_settings_modified()

        cv.bind("<Button-1>", toggle)
        return cv

    def _add_chk(self, parent, label, key):
        bg = parent.cget("bg")
        frame = tk.Frame(parent, bg=bg)
        frame.pack(fill=tk.X, pady=8)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 10),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT)

        var = tk.BooleanVar(value=self.settings.get(key, True))
        self.entries[key] = (var, "bool")

        cv = self._create_toggle_canvas(frame, var)
        cv.pack(side=tk.RIGHT)
        return frame

    def _add_grid_chk(self, parent_frame, label, key, row, col=0):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        var = tk.BooleanVar(value=self.settings.get(key, True))
        self.entries[key] = (var, "bool")

        tk.Label(
            cell,
            text=label,
            font=("Segoe UI", 10),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        cv = self._create_toggle_canvas(cell, var)
        cv.pack(side=tk.RIGHT, padx=(10, 0))
        return cv

    def _build_schedule_tab(self, tab):
        card1, f1 = self._create_card(tab, "Break Times", 0, 0)
        self._add_field(f1, "Short Interval (min):", "short_break_interval_min", 0, col=0)
        self._add_field(f1, "Short Duration (sec):", "short_break_duration_sec", 0, col=1)
        self._add_field(f1, "Long Interval (min):", "long_break_interval_min", 1, col=0)
        self._add_field(f1, "Long Duration (sec):", "long_break_duration_sec", 1, col=1)
        self._add_field(f1, "Pre-warning (sec):", "pre_warning_sec", 2, col=0)

        card2, f2 = self._create_card(tab, "Environment & Astro", 0, 1)
        self._add_field(f2, "Latitude:", "latitude", 0, col=0)
        self._add_field(f2, "Longitude:", "longitude", 0, col=1)
        
        def _auto_detect():
            import urllib.request
            import json
            try:
                btn_detect.config(text="Detecting...")
                btn_detect.update()
                with urllib.request.urlopen("http://ip-api.com/json/", timeout=5) as r:
                    data = json.loads(r.read().decode())
                    if "lat" in data and "lon" in data:
                        self.entries["latitude"][0].set(str(data["lat"]))
                        self.entries["longitude"][0].set(str(data["lon"]))
            except Exception:
                pass
            finally:
                btn_detect.config(text="Auto-Detect IP")

        btn_detect = tk.Button(f2, text="Auto-Detect IP", font=("Consolas", 8), bg=TH["bg3"], fg=TH["fg"], relief=tk.FLAT, cursor="hand2", command=_auto_detect)
        btn_detect.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        self._add_field(f2, "Night Start (hr):", "night_light_start_hour", 2, col=0)
        self._add_field(f2, "Night End (hr):", "night_light_end_hour", 2, col=1)
        self._add_field(f2, "Transition (sec):", "nl_transition_duration", 3, col=0)
        
        location_options = [
            "Disabled", "Every Hour", "Every 2 Hours", "Every 6 Hours", "Every 12 Hours", "Every 24 Hours"
        ]
        self._add_combo(f2, "Location Auto-Check:", "location_check_interval_display", 3, location_options, col=1)

        card3, f3 = self._create_card(tab, "Audio Source & Options", 1, 0)
        audio_sources = [
            "default", "random", "campfire", "forest", "night", "ocean", "rain", "waterfall"
        ]
        self._add_combo(f3, "Break Audio Source:", "break_audio_source", 0, audio_sources, col=0)

        self._add_grid_chk(f3, "Enable breathing sound", "enable_sound", 1, col=0)
        self._add_grid_chk(f3, "Dim screen during breaks", "enable_dimming", 1, col=1)
        self._add_grid_chk(f3, "Weather color warmth", "enable_weather_warmth", 2, col=0)
        self._add_grid_chk(f3, "Run breaks during games", "run_during_game", 2, col=1)
        self._add_grid_chk(f3, "Enable Night Light", "nl_enabled", 3, col=0)

        card4, f4 = self._create_card(tab, "Box Breathing & Voice Guide", 1, 1)
        self._add_grid_chk(f4, "Enable voice guide", "voice_prompts_enabled", 0, col=0)
        self._add_combo(f4, "Voice Model:", "voice_name", 0, get_sapi_voices(), col=1)
        
        self._add_field(f4, "Inhale (sec):", "voice_inhale_sec", 1, col=0)
        self._add_field(f4, "Hold In (sec):", "voice_hold_in_sec", 1, col=1)
        self._add_field(f4, "Exhale (sec):", "voice_exhale_sec", 2, col=0)
        self._add_field(f4, "Hold Out (sec):", "voice_hold_out_sec", 2, col=1)
        
        self._add_field(f4, "Volume (0-100):", "voice_volume", 3, col=0)
        self._add_field(f4, "Speed Rate:", "voice_rate", 3, col=1)
        
        self._add_combo(f4, "Break Type:", "voice_break_type", 4, ["Both", "Short Only", "Long Only"], col=0)
        self._add_field(f4, "Min Duration (s):", "voice_min_duration_sec", 4, col=1)
        
        self._add_field(f4, "Inhale Text:", "voice_inhale_text", 5, col=0, is_str=True)
        self._add_field(f4, "Exhale Text:", "voice_exhale_text", 5, col=1, is_str=True)
        self._add_field(f4, "Hold In Text:", "voice_hold_in_text", 6, col=0, is_str=True)
        self._add_field(f4, "Hold Out Text:", "voice_hold_out_text", 6, col=1, is_str=True)

    def _build_toast_tab(self, tab):
        card1, f1 = self._create_card(tab, "Layout & Animation", 0, 0, columnspan=2)
        self._add_combo(
            f1, "Position:", "toast_pos", 0, col=0,
            values=["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"]
        )
        self._add_combo(
            f1, "Animation:", "toast_anim_style", 0, col=1,
            values=["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"]
        )
        self._add_field(f1, "Transition Time (ms):", "toast_transition_time_ms", 1, col=0)
        self._add_field(f1, "Display Duration (sec):", "toast_duration_sec", 1, col=1)
        self._add_field(f1, "Width (px):", "toast_width", 2, col=0)
        self._add_field(f1, "Height (px):", "toast_height", 2, col=1)
        self._add_field(f1, "Font Size:", "toast_font_size", 3, col=0)
        self._add_combo(f1, "Font Weight:", "toast_font_weight", 3, ["normal", "bold"], col=1)
        self._add_field(f1, "Emoji Icon:", "toast_emoji", 4, col=0, is_str=True)
        self._add_combo(f1, "Text Align:", "toast_text_align", 4, ["left", "center", "right"], col=1)
        self._add_grid_chk(f1, "Show Clock Time", "toast_show_clock", 5, col=0)

        card2, f2 = self._create_card(tab, "Visual Styling", 1, 0, columnspan=2)
        self._add_color_field(f2, "Background Color:", "toast_bg_color", 0, col=0)
        self._add_color_field(f2, "Text Color:", "toast_fg_color", 0, col=1)
        self._add_color_field(f2, "Accent Color:", "toast_accent_color", 1, col=0)
        self._add_color_field(f2, "Gradient End:", "toast_gradient_end", 1, col=1)
        self._add_field(f2, "Border Radius (px):", "toast_radius", 2, col=0)
        self._add_field(f2, "Border Width (px):", "toast_border_width", 2, col=1)
        self._add_color_field(f2, "Border Color:", "toast_border_color", 3, col=0)
        self._add_combo(f2, "Border Style:", "toast_border_style", 3, ["Solid", "Dashed", "Dotted"], col=1)
        self._add_combo(f2, "Stripe Position:", "toast_stripe_pos", 4, ["Left", "Right", "Top", "Bottom"], col=0)
        self._add_slider_field(f2, "Opacity:", "toast_opacity", 4, col=1, from_=0.1, to=1.0, resolution=0.05)
        self._add_grid_chk(f2, "Enable Gradient", "toast_gradient", 5, col=0)
        self._add_grid_chk(f2, "Enable Shadow", "toast_shadow", 5, col=1)
        self._add_grid_chk(f2, "Accent Stripe", "toast_accent_stripe", 6, col=0)
        self._add_grid_chk(f2, "Progress Bar", "toast_progress_bar", 6, col=1)
        self._add_field(f2, "Padding X (px):", "toast_padding_x", 7, col=0)
        self._add_field(f2, "Padding Y (px):", "toast_padding_y", 7, col=1)

        card3, f3 = self._create_card(tab, "Audio & Interaction", 2, 0, columnspan=2)
        self._add_grid_chk(f3, "Play Warning Sound", "toast_enable_sound", 0, col=0)
        self._add_combo(f3, "Sound Effect:", "toast_sound_effect", 0, SOUND_EFFECTS, col=1)
        self._add_slider_field(f3, "Volume:", "toast_volume", 1, col=0, from_=0, to=100, resolution=1)
        self._add_combo(f3, "Click Action:", "toast_click_action", 1, ["dismiss", "snooze", "settings"], col=1)

    def _build_health_toast_tab(self, tab):
        card1, f1 = self._create_card(tab, "Scheduling & Animation", 0, 0, columnspan=2)
        self._add_grid_chk(f1, "Enable Health Tips", "ht_enabled", 0, col=0)
        self._add_field(f1, "Interval (min):", "ht_interval_min", 0, col=1)
        self._add_field(f1, "Display Duration (sec):", "ht_duration_sec", 1, col=0)
        self._add_field(f1, "Transition Time (ms):", "ht_toast_transition_time_ms", 1, col=1)
        self._add_combo(
            f1, "Position:", "ht_toast_pos", 2, col=0,
            values=["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"]
        )
        self._add_combo(
            f1, "Animation:", "ht_toast_anim_style", 2, col=1,
            values=["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"]
        )
        self._add_grid_chk(f1, "Show Clock Time", "ht_toast_show_clock", 3, col=0)

        card1_night, f1_night = self._create_card(tab, "Night Mode Overrides (During Night Care Hours)", 1, 0, columnspan=2)
        self._add_grid_chk(f1_night, "Enable at Night", "ht_night_enabled", 0, col=0)
        self._add_field(f1_night, "Night Interval (min):", "ht_night_interval_min", 0, col=1)
        self._add_field(f1_night, "Night Duration (sec):", "ht_night_duration_sec", 1, col=0)
        self._add_combo(
            f1_night, "Night Position:", "ht_night_toast_pos", 1, col=1,
            values=["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"]
        )

        card2, f2 = self._create_card(tab, "Tip Categories", 2, 0, columnspan=2)
        self._add_grid_chk(f2, "Breathing Exercises", "ht_cat_breathing", 0, col=0)
        self._add_grid_chk(f2, "Eye Care Tips", "ht_cat_eye_care", 0, col=1)
        self._add_grid_chk(f2, "Posture Adjustment", "ht_cat_posture", 1, col=0)
        self._add_grid_chk(f2, "Muscle Stretching", "ht_cat_stretch", 1, col=1)
        self._add_grid_chk(f2, "Hydration Reminders", "ht_cat_hydration", 2, col=0)
        self._add_grid_chk(f2, "Mental Ease Moments", "ht_cat_mental", 2, col=1)
        self._add_grid_chk(f2, "Hands & Wrists", "ht_cat_hands_wrists", 3, col=0)

        card3, f3 = self._create_card(tab, "Toast Style & Audio", 3, 0, columnspan=2)
        self._add_field(f3, "Width (px):", "ht_toast_width", 0, col=0)
        self._add_field(f3, "Height (px):", "ht_toast_height", 0, col=1)
        self._add_color_field(f3, "Background Color:", "ht_toast_bg_color", 1, col=0)
        self._add_color_field(f3, "Text Color:", "ht_toast_fg_color", 1, col=1)
        self._add_color_field(f3, "Accent Color:", "ht_toast_accent_color", 2, col=0)
        self._add_color_field(f3, "Gradient End:", "ht_toast_gradient_end", 2, col=1)
        self._add_field(f3, "Font Size:", "ht_toast_font_size", 3, col=0)
        self._add_field(f3, "Border Radius (px):", "ht_toast_radius", 3, col=1)
        self._add_field(f3, "Border Width (px):", "ht_toast_border_width", 4, col=0)
        self._add_color_field(f3, "Border Color:", "ht_toast_border_color", 4, col=1)
        self._add_combo(f3, "Border Style:", "ht_toast_border_style", 5, ["Solid", "Dashed", "Dotted"], col=0)
        self._add_combo(f3, "Stripe Position:", "ht_toast_stripe_pos", 5, ["Left", "Right", "Top", "Bottom"], col=1)
        self._add_slider_field(f3, "Opacity:", "ht_toast_opacity", 6, col=0, from_=0.1, to=1.0, resolution=0.05)
        self._add_combo(f3, "Text Align:", "ht_toast_text_align", 6, ["left", "center", "right"], col=1)
        self._add_grid_chk(f3, "Enable Gradient", "ht_toast_gradient", 7, col=0)
        self._add_grid_chk(f3, "Enable Shadow", "ht_toast_shadow", 7, col=1)
        self._add_grid_chk(f3, "Accent Stripe", "ht_toast_accent_stripe", 8, col=0)
        self._add_grid_chk(f3, "Progress Bar", "ht_toast_progress_bar", 8, col=1)
        self._add_grid_chk(f3, "Play Tip Sound", "ht_toast_enable_sound", 9, col=0)
        self._add_combo(f3, "Sound Effect:", "ht_toast_sound_effect", 9, SOUND_EFFECTS, col=1)
        self._add_slider_field(f3, "Volume:", "ht_toast_volume", 10, col=0, from_=0, to=100, resolution=1)
        self._add_combo(f3, "Click Action:", "ht_toast_click_action", 10, ["dismiss", "snooze", "settings"], col=1)
        self._add_field(f3, "Padding X (px):", "ht_toast_padding_x", 11, col=0)
        self._add_field(f3, "Padding Y (px):", "ht_toast_padding_y", 11, col=1)

    def _build_brightness_care_tab(self, tab):
        card1, f1 = self._create_card(tab, "Auto Dimming Scheduler", 0, 0, columnspan=2)
        self._add_grid_chk(f1, "Enable Brightness Care", "bc_enabled", 0, col=0)
        self._add_field(f1, "Start Time (HH:MM):", "bc_start_time", 0, col=1, is_str=True)
        self._add_field(f1, "End Time (HH:MM):", "bc_end_time", 1, col=0, is_str=True)
        self._add_field(f1, "Target Brightness (%):", "bc_target_brightness", 1, col=1)
        self._add_field(f1, "Transition Duration (min):", "bc_duration_minutes", 2, col=0)
        self._add_field(f1, "Normal Fade (sec):", "bc_transition_time_sec", 2, col=1)

        card2, f2 = self._create_card(tab, "Aggressive & Safe Limits", 1, 0, columnspan=2)
        self._add_field(f2, "Aggressive Target (%):", "bc_aggressive_target_brightness", 0, col=0)
        self._add_field(f2, "Aggressive Duration (min):", "bc_aggressive_duration_minutes", 0, col=1)
        self._add_field(f2, "Aggressive Fade (sec):", "bc_aggressive_transition_time_sec", 1, col=0)
        self._add_field(f2, "Safe Brightness (%):", "bc_safe_brightness", 2, col=0)
        self._add_field(f2, "Safe Duration (sec):", "bc_safe_duration_seconds", 2, col=1)

        card3, f3 = self._create_card(tab, "Toast Visuals & Audio", 2, 0, columnspan=2)
        self._add_field(f3, "Display Duration (sec):", "bc_toast_duration_sec", 0, col=0)
        self._add_field(f3, "Transition Time (ms):", "bc_toast_transition_time_ms", 0, col=1)
        self._add_combo(f3, "Animation Style:", "bc_toast_anim_style", 1, ["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"], col=0)
        self._add_combo(f3, "Position:", "bc_toast_pos", 1, ["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"], col=1)
        self._add_field(f3, "Width (px):", "bc_toast_width", 2, col=0)
        self._add_field(f3, "Height (px):", "bc_toast_height", 2, col=1)
        self._add_color_field(f3, "Background Color:", "bc_toast_bg_color", 3, col=0)
        self._add_color_field(f3, "Text Color:", "bc_toast_fg_color", 3, col=1)
        self._add_color_field(f3, "Accent Color:", "bc_toast_accent_color", 4, col=0)
        self._add_color_field(f3, "Gradient End:", "bc_toast_gradient_end", 4, col=1)
        self._add_field(f3, "Emoji Icon:", "bc_toast_emoji", 5, col=0, is_str=True)
        self._add_field(f3, "Border Radius (px):", "bc_toast_radius", 5, col=1)
        self._add_field(f3, "Border Width (px):", "bc_toast_border_width", 6, col=0)
        self._add_color_field(f3, "Border Color:", "bc_toast_border_color", 6, col=1)
        self._add_combo(f3, "Border Style:", "bc_toast_border_style", 7, ["Solid", "Dashed", "Dotted"], col=0)
        self._add_combo(f3, "Stripe Position:", "bc_toast_stripe_pos", 7, ["Left", "Right", "Top", "Bottom"], col=1)
        self._add_slider_field(f3, "Opacity:", "bc_toast_opacity", 8, col=0, from_=0.1, to=1.0, resolution=0.05)
        self._add_combo(f3, "Text Align:", "bc_toast_text_align", 8, ["left", "center", "right"], col=1)
        self._add_grid_chk(f3, "Enable Gradient", "bc_toast_gradient", 9, col=0)
        self._add_grid_chk(f3, "Enable Shadow", "bc_toast_shadow", 9, col=1)
        self._add_grid_chk(f3, "Accent Stripe", "bc_toast_accent_stripe", 10, col=0)
        self._add_grid_chk(f3, "Progress Bar", "bc_toast_progress_bar", 10, col=1)
        self._add_grid_chk(f3, "Play Warning Sound", "bc_toast_enable_sound", 11, col=0)
        self._add_combo(f3, "Sound Effect:", "bc_toast_sound_effect", 11, SOUND_EFFECTS, col=1)
        self._add_slider_field(f3, "Volume:", "bc_toast_volume", 12, col=0, from_=0, to=100, resolution=1)
        self._add_combo(f3, "Click Action:", "bc_toast_click_action", 12, ["dismiss", "snooze", "settings"], col=1)
        self._add_field(f3, "Padding X (px):", "bc_toast_padding_x", 13, col=0)
        self._add_field(f3, "Padding Y (px):", "bc_toast_padding_y", 13, col=1)

    def _build_night_care_tab(self, tab):
        card1, f1 = self._create_card(tab, "Late Night Caution", 0, 0, columnspan=2)
        self._add_grid_chk(f1, "Enable Night Care", "nc_enabled", 0, col=0)
        self._add_field(f1, "Start Time (HH:MM):", "nc_start_time", 0, col=1, is_str=True)
        self._add_field(f1, "End Time (HH:MM):", "nc_end_time", 1, col=0, is_str=True)
        self._add_field(f1, "Check Interval (min):", "nc_interval_minutes", 1, col=1)
        self._add_field(f1, "Slogans (pipe-separated):", "nc_slogans", 2, col=0, is_str=True)
        self._add_grid_chk(f1, "Enable Screen Flick", "nc_flick_enabled", 3, col=0)
        self._add_field(f1, "Flick Hold (sec):", "nc_flick_hold_sec", 3, col=1)
        self._add_field(f1, "Flick Fade (sec):", "nc_flick_fade_sec", 4, col=0)

        card2, f2 = self._create_card(tab, "Toast Visuals & Audio", 1, 0, columnspan=2)
        self._add_field(f2, "Display Duration (sec):", "nc_toast_duration_sec", 0, col=0)
        self._add_field(f2, "Transition Time (ms):", "nc_toast_transition_time_ms", 0, col=1)
        self._add_combo(f2, "Animation Style:", "nc_toast_anim_style", 1, ["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"], col=0)
        self._add_combo(f2, "Position:", "nc_toast_pos", 1, ["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"], col=1)
        self._add_field(f2, "Width (px):", "nc_toast_width", 2, col=0)
        self._add_field(f2, "Height (px):", "nc_toast_height", 2, col=1)
        self._add_color_field(f2, "Background Color:", "nc_toast_bg_color", 3, col=0)
        self._add_color_field(f2, "Text Color:", "nc_toast_fg_color", 3, col=1)
        self._add_color_field(f2, "Accent Color:", "nc_toast_accent_color", 4, col=0)
        self._add_color_field(f2, "Gradient End:", "nc_toast_gradient_end", 4, col=1)
        self._add_field(f2, "Font Size:", "nc_toast_font_size", 5, col=0)
        self._add_field(f2, "Emoji Icon:", "nc_toast_emoji", 5, col=1, is_str=True)
        self._add_field(f2, "Border Radius (px):", "nc_toast_radius", 6, col=0)
        self._add_field(f2, "Border Width (px):", "nc_toast_border_width", 6, col=1)
        self._add_color_field(f2, "Border Color:", "nc_toast_border_color", 7, col=0)
        self._add_combo(f2, "Border Style:", "nc_toast_border_style", 7, ["Solid", "Dashed", "Dotted"], col=1)
        self._add_combo(f2, "Stripe Position:", "nc_toast_stripe_pos", 8, ["Left", "Right", "Top", "Bottom"], col=0)
        self._add_slider_field(f2, "Opacity:", "nc_toast_opacity", 8, col=1, from_=0.1, to=1.0, resolution=0.05)
        self._add_combo(f2, "Text Align:", "nc_toast_text_align", 9, ["left", "center", "right"], col=0)
        self._add_grid_chk(f2, "Enable Gradient", "nc_toast_gradient", 9, col=1)
        self._add_grid_chk(f2, "Enable Shadow", "nc_toast_shadow", 10, col=0)
        self._add_grid_chk(f2, "Accent Stripe", "nc_toast_accent_stripe", 10, col=1)
        self._add_grid_chk(f2, "Progress Bar", "nc_toast_progress_bar", 11, col=0)
        self._add_grid_chk(f2, "Play Warning Sound", "nc_toast_enable_sound", 11, col=1)
        self._add_combo(f2, "Sound Effect:", "nc_toast_sound_effect", 12, SOUND_EFFECTS, col=0)
        self._add_slider_field(f2, "Volume:", "nc_toast_volume", 12, col=1, from_=0, to=100, resolution=1)
        self._add_combo(f2, "Click Action:", "nc_toast_click_action", 13, ["dismiss", "snooze", "settings"], col=0)
        self._add_field(f2, "Padding X (px):", "nc_toast_padding_x", 13, col=1)
        self._add_field(f2, "Padding Y (px):", "nc_toast_padding_y", 14, col=0)

    def _get_toast_type_for_tab(self, tab_name):
        if "Toast FX" in tab_name:
            return "General Warning"
        if "Health Toast" in tab_name:
            return "Health Tip"
        if "Brightness Care" in tab_name:
            return "Brightness Care"
        if "Night Care" in tab_name:
            return "Night Care"
        return None

    def _update_status_dashboard(self):
        def _update_lbl(lbl, key):
            val = self.settings.get(key, False)
            if key in self.entries:
                val = self.entries[key][0].get()
                if isinstance(val, str):
                    val = val.lower() in ("1", "true")
            if val:
                lbl.config(text="● " + lbl.cget("text")[2:], fg=TH["success"])
            else:
                lbl.config(text="○ " + lbl.cget("text")[2:], fg=TH["fg_dim"])
        
        if hasattr(self, "lbl_status_nl"):
            _update_lbl(self.lbl_status_nl, "nl_enabled")
            _update_lbl(self.lbl_status_ht, "ht_enabled")
            _update_lbl(self.lbl_status_bc, "bc_enabled")
            _update_lbl(self.lbl_status_nc, "nc_enabled")

    def _on_settings_modified(self, is_tab_switch=False):
        self.is_dirty = True
        self._update_status_dashboard()
        if not hasattr(self, "_save_timer"):
            self._save_timer = None

        toast_type = self._get_toast_type_for_tab(self.current_frame_name)
        if toast_type:
            temp_settings = dict(self.settings)
            for key, (var, var_type) in self.entries.items():
                if var_type == "bool":
                    val = var.get()
                else:
                    val = var.get()
                    if hasattr(val, "strip"):
                        val = val.strip()
                    else:
                        val = str(val).strip()

                try:
                    if var_type == "bool":
                        temp_settings[key] = val == "1" or val == "True" or val is True
                    elif key in (
                        "latitude",
                        "longitude",
                        "toast_opacity",
                        "ht_toast_opacity",
                        "nc_toast_opacity",
                        "nc_flick_hold_sec",
                        "nc_flick_fade_sec",
                    ):
                        temp_settings[key] = float(val)
                    elif var_type is False:
                        temp_settings[key] = int(val)
                    else:
                        temp_settings[key] = val
                except ValueError:
                    pass

            if toast_type == "Night Care":
                for k, v in list(temp_settings.items()):
                    if k.startswith("nc_toast_"):
                        suffix = k[len("nc_toast_"):]
                        temp_settings[f"toast_{suffix}"] = v
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
            elif toast_type == "General Warning":
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
            elif toast_type == "Health Tip":
                temp_settings["ht_toast_auto_dismiss"] = False
                temp_settings["ht_toast_enable_sound"] = False
            elif toast_type == "Brightness Care":
                temp_settings["bc_safe_duration_seconds"] = 999999
                temp_settings["bc_toast_enable_sound"] = False

            # Check if a matching toast is already showing
            toast_exists = False
            try:
                from services.aerohub_core.toast_utils import BaseToast
                for t in list(BaseToast._active_toasts):
                    if toast_type == "General Warning" and t.__class__.__name__ == "WarningToast":
                        toast_exists = True
                    elif toast_type == "Brightness Care" and t.__class__.__name__ == "BrightnessWarningToast":
                        toast_exists = True
                    elif toast_type == "Health Tip" and t.__class__.__name__ == "BaseToast" and getattr(t, "is_health_tip", False):
                        toast_exists = True
                    elif toast_type == "Night Care" and t.__class__.__name__ == "BaseToast" and not getattr(t, "is_health_tip", False) and getattr(t, "title", "") == "NIGHT CARE":
                        toast_exists = True
            except Exception as e:
                logger.error(f"Error checking active toasts: {e}")

            # Update active matching toasts
            try:
                from services.aerohub_core.toast_utils import BaseToast
                for t in list(BaseToast._active_toasts):
                    is_match = False
                    if toast_type == "General Warning" and t.__class__.__name__ == "WarningToast":
                        is_match = True
                    elif toast_type == "Brightness Care" and t.__class__.__name__ == "BrightnessWarningToast":
                        is_match = True
                    elif toast_type == "Health Tip" and t.__class__.__name__ == "BaseToast" and getattr(t, "is_health_tip", False):
                        is_match = True
                    elif toast_type == "Night Care" and t.__class__.__name__ == "BaseToast" and not getattr(t, "is_health_tip", False) and getattr(t, "title", "") == "NIGHT CARE":
                        is_match = True
                    
                    if is_match:
                        try:
                            t.update_settings(temp_settings)
                            self.live_preview_toast = t
                        except Exception as ex:
                            logger.error(f"Error updating active toast instance: {ex}")
            except Exception as e:
                logger.error(f"Error updating active toasts: {e}")

            # If no matching toast was showing and we are not switching tabs, spawn a new one
            if not toast_exists and not is_tab_switch:
                self._show_desktop_preview_for_tab(self.current_frame_name, is_auto_edit=True)

    def _play_preview_clicked(self):
        if self.current_frame_name:
            # First quietly save settings so the preview uses latest input values that haven't been debounced yet
            self._save_silently()
            self._show_desktop_preview_for_tab(self.current_frame_name)

    def _show_desktop_preview_for_tab(self, tab_name, is_auto_edit=False):
        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            try:
                self.live_preview_toast.force_close()
            except Exception:
                pass
            self.live_preview_toast = None

        toast_type = self._get_toast_type_for_tab(tab_name)
        if not toast_type:
            return

        temp_settings = dict(self.settings)
        temp_settings["is_preview"] = True
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                ):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit:
            if toast_type == "Night Care":
                for k, v in list(temp_settings.items()):
                    if k.startswith("nc_toast_"):
                        suffix = k[len("nc_toast_"):]
                        temp_settings[f"toast_{suffix}"] = v
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
            elif toast_type == "General Warning":
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
            elif toast_type == "Health Tip":
                temp_settings["ht_toast_auto_dismiss"] = False
                temp_settings["ht_toast_enable_sound"] = False
            elif toast_type == "Brightness Care":
                temp_settings["bc_safe_duration_seconds"] = 999999
                temp_settings["bc_toast_enable_sound"] = False

        if toast_type == "General Warning":
            toast = WarningToast(
                self.parent, "Time to take a break!", 30, temp_settings
            )
            toast.show()
            self.live_preview_toast = toast
        elif toast_type == "Health Tip":
            toast = BaseToast(
                self.parent,
                "HEALTH TIP",
                "Take a slow, deep breath. Inhale for 4s.",
                temp_settings,
                is_health_tip=True,
            )
            toast.show()
            self.live_preview_toast = toast
        elif toast_type == "Brightness Care":
            
            def _on_skip():
                pass
            def _on_decrease():
                pass
                
            toast = BrightnessWarningToast(
                self.parent, temp_settings, _on_skip, _on_decrease
            )
            toast.show()
            self.live_preview_toast = toast
        else:  # Night Care
            nc_settings = dict(temp_settings)
            for k, v in temp_settings.items():
                if k.startswith("nc_toast_"):
                    suffix = k[len("nc_toast_"):]
                    nc_settings[f"toast_{suffix}"] = v
            toast = BaseToast(
                self.parent,
                "NIGHT CARE",
                "It's late. Your body needs rest. 🌙",
                nc_settings,
            )
            toast.show()
            self.live_preview_toast = toast

    def _save_silently(self):
        from core.constants import DEFAULT_SETTINGS
        for key, (var, var_type) in self.entries.items():
            if var_type == "bool":
                val = var.get()
            else:
                val = var.get().strip()
            
            # Apply default if blank
            if val == "" and var_type != "bool":
                default_val = DEFAULT_SETTINGS.get(key, "")
                var.set(str(default_val))
                val = str(default_val)

            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                    "nc_flick_hold_sec",
                    "nc_flick_fade_sec",
                ):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                # Revert to last valid setting
                last_valid = self.settings.get(key, DEFAULT_SETTINGS.get(key, ""))
                var.set(str(last_valid))

        # Map display interval back to integer hours
        interval_map = {"Disabled": 0, "Every Hour": 1, "Every 2 Hours": 2, "Every 6 Hours": 6, "Every 12 Hours": 12, "Every 24 Hours": 24}
        display_val = self.settings.get("location_check_interval_display", "Every Hour")
        self.settings["location_check_interval_hours"] = interval_map.get(display_val, 1)
        if "location_check_interval_display" in self.settings:
            del self.settings["location_check_interval_display"]

        save_settings(self.settings)
        self.on_save(self.settings)
        self.is_dirty = False
        return True

    def _restore_defaults(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to restore all settings to default? This cannot be undone."):
            self.settings = dict(DEFAULT_SETTINGS)
            for key, (var, var_type) in self.entries.items():
                val = self.settings.get(key, "")
                if var_type == "bool":
                    var.set(bool(val))
                else:
                    var.set(str(val))
            self._on_settings_modified()

    def _save_settings_clicked(self):
        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            try:
                self.live_preview_toast.force_close()
            except Exception:
                pass
            self.live_preview_toast = None

        if not self._save_silently():
            return
        
        self.btn_save.config(text="Saved!", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="Save Settings", state=tk.NORMAL)
            except Exception:
                pass
        self.parent.after(2000, reset_btn)

    def _save_and_close(self, root):
        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            try:
                self.live_preview_toast.force_close()
            except Exception:
                pass
            self.live_preview_toast = None

        self._save_silently()
        
        for key in list(self.entries.keys()):
            var, var_type = self.entries.pop(key)
            del var

        root.grab_release()
        root.destroy()

    def _update_upcoming_break(self):
        if not hasattr(self, "upcoming_title_label") or not self.upcoming_title_label.winfo_exists():
            return

        if not self.app:
            self.upcoming_type_label.config(text="N/A")
            self.upcoming_time_label.config(text="--:--")
            self.upcoming_clock_label.config(text="No App Connection")
            return

        now = time.time()
        
        # Calculate next break times using settings values
        short_interval = self.app.settings.get("short_break_interval_min", 20) * 60
        long_interval = self.app.settings.get("long_break_interval_min", 60) * 60
        
        next_short = self.app._last_short_break + short_interval
        next_long = self.app._last_long_break + long_interval
        
        # Determine which break is sooner
        if next_long <= next_short:
            break_type = "Long Break"
            next_break_time = next_long
        else:
            break_type = "Short Break"
            next_break_time = next_short
            
        remaining = next_break_time - now
        
        if self.app._paused:
            self.upcoming_type_label.config(text=break_type, fg=TH["warning"])
            self.upcoming_time_label.config(text="PAUSED")
            
            # Format scheduled time
            local_time_struct = time.localtime(next_break_time)
            time_str = time.strftime("%H:%M:%S", local_time_struct)
            self.upcoming_clock_label.config(text=f"Scheduled at {time_str}")
        elif remaining <= 0:
            self.upcoming_type_label.config(text=break_type, fg=TH["accent"])
            self.upcoming_time_label.config(text="00m 00s")
            self.upcoming_clock_label.config(text="Starting...")
        else:
            self.upcoming_type_label.config(text=break_type, fg=TH["accent"])
            
            # Format remaining time (e.g., "12m 45s" or "45s")
            rem_sec = int(remaining)
            rem_min = rem_sec // 60
            rem_sec = rem_sec % 60
            if rem_min > 0:
                time_text = f"{rem_min:02d}m {rem_sec:02d}s"
            else:
                time_text = f"{rem_sec:02d}s"
            self.upcoming_time_label.config(text=time_text)
            
            # Format scheduled time
            local_time_struct = time.localtime(next_break_time)
            time_str = time.strftime("%H:%M:%S", local_time_struct)
            self.upcoming_clock_label.config(text=f"at {time_str}")
            
        # Schedule next update in 1 second
        self.sidebar.after(1000, self._update_upcoming_break)
```

---

### File: `ui/theme.py`
- **Path:** `ui/theme.py`
- **Estimated Tokens:** 729
- **mtime:** 1781114542.243

```python
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
```

---

### File: `ui/toast.py`
- **Path:** `ui/toast.py`
- **Estimated Tokens:** 6,085
- **mtime:** 1781288700.904

```python
import os
import time
import tkinter as tk
from core.logger import logger
from ui.theme import _add_hover

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class WarningToast:
    def __init__(self, parent, message: str, duration_sec: int, settings: dict):
        self.parent = parent
        self.message = message
        self.duration = duration_sec
        self.settings = settings
        self.closing = False
        self.window = None
        self.pos = "center"
        self.slot_index = 0

    def show(self):
        try:
            from services.aerohub_core.toast_utils import ToastQueue
            ToastQueue.add(self)
        except Exception:
            self._create_toast()

    def _create_toast(self):
        toast = tk.Toplevel(self.parent)
        self.window = toast
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        trans_color = "#010203"
        toast.configure(bg=trans_color)
        toast.attributes("-transparentcolor", trans_color)
        toast.attributes("-alpha", 0.0)

        # Register in active toasts
        from services.aerohub_core.toast_utils import BaseToast
        with BaseToast._lock:
            BaseToast._active_toasts.append(self)

        # Register in shared status
        from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
        status = read_shared_status()
        status["active_toast_pid"] = os.getpid()
        status["active_toast_end_time"] = time.time() + self.duration + 2
        write_shared_status(status)

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

        # Sanitize
        opacity = max(0.0, min(1.0, opacity))
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"
        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

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

        self.canvas = tk.Canvas(
            toast, width=tw, height=th, bg=trans_color, highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._draw_toast_bg(self.canvas, tw, th, radius, bg_col, border_width, border_color)
        self._draw_toast_text(self.canvas, padx, pady, font_size, font_weight, emoji, fg_col)

        toast.update_idletasks()

        def close_toast(event=None):
            if self.closing:
                return
            self.closing = True
            from services.aerohub_core.toast_utils import BaseToast
            with BaseToast._lock:
                if self in BaseToast._active_toasts:
                    BaseToast._active_toasts.remove(self)
            try:
                from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
                status = read_shared_status()
                if status.get("active_toast_pid") == os.getpid():
                    status["active_toast_pid"] = None
                    status["active_toast_end_time"] = 0.0
                    write_shared_status(status)
            except Exception:
                pass
            try:
                toast.destroy()
            except Exception:
                pass
            try:
                from services.aerohub_core.toast_utils import ToastQueue
                ToastQueue.on_toast_closed(self.parent)
            except Exception:
                pass

        self.force_close = close_toast

        toast.bind("<Button-1>", close_toast)
        self.canvas.bind("<Button-1>", close_toast)
        toast.bind("<ButtonRelease-1>", close_toast)
        self.canvas.bind("<ButtonRelease-1>", close_toast)

        self._animate_in(
            toast,
            tw,
            th,
            start_x,
            start_y,
            final_x,
            final_y,
            anim_style,
            opacity,
            close_toast,
        )
        if self.duration > 0:
            self._play_pre_break_sound()

    def _draw_toast_bg(
        self, canvas, tw, th, radius, bg_col, border_width, border_color
    ):
        points = [
            radius, 0, tw - radius, 0, tw, 0, tw, radius, tw, th - radius, tw, th,
            tw - radius, th, radius, th, 0, th, 0, th - radius, 0, radius, 0, 0
        ]
        if border_width > 0:
            canvas.create_polygon(
                points,
                smooth=True,
                fill=bg_col,
                outline=border_color,
                width=border_width,
            )
        else:
            canvas.create_polygon(points, smooth=True, fill=bg_col)

    def _draw_toast_text(
        self, canvas, padx, pady, font_size, font_weight, emoji, fg_col
    ):
        msg_font = ("Segoe UI", font_size, font_weight)
        sub_font = ("Segoe UI", max(8, font_size - 2))
        tw = int(self.settings.get("toast_width", 260))

        canvas.create_text(
            padx + 10,
            pady,
            anchor=tk.NW,
            text=f"{emoji}  {self.message}",
            font=msg_font,
            fill=fg_col,
            width=tw - (padx + 10) * 2,
        )
        self.countdown_text_id = canvas.create_text(
            padx + 10,
            pady + font_size + 8,
            anchor=tk.NW,
            text=f"Break in {self.duration} seconds",
            font=sub_font,
            fill="#8892b0",
        )

    def tick_countdown(self):
        if self.closing:
            return
        if self.duration > 0:
            self.duration -= 1
            try:
                self.canvas.itemconfig(
                    self.countdown_text_id,
                    text=f"Break in {self.duration} seconds"
                )
            except Exception:
                pass
            if self.duration <= 0:
                self.force_close()
            else:
                self.parent.after(1000, self.tick_countdown)

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
                self.tick_countdown()

        slide_in(0)

    def _play_pre_break_sound(self):
        if not self.settings.get("toast_enable_sound", True):
            return
        try:
            import winsound
            sound_path = os.path.join(APP_ROOT, "resources", "on_pre_break.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(
                    sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
                )
        except Exception:
            pass

    def update_settings(self, settings):
        self.settings = settings
        if not self.window or not self.window.winfo_exists():
            return

        trans_color = "#010203"
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
        opacity = float(self.settings.get("toast_opacity", 0.92))
        border_width = int(self.settings.get("toast_border_width", 0))
        border_color = self.settings.get("toast_border_color", "#7c3aed")

        opacity = max(0.0, min(1.0, opacity))
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"
        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

        sw = self.window.winfo_screenwidth()
        final_y = 60

        if pos == "left":
            final_x = 20
        elif pos == "right":
            final_x = sw - tw - 20
        else:
            final_x = (sw - tw) // 2

        try:
            self.window.geometry(f"{tw}x{th}+{final_x}+{final_y}")
            self.window.attributes("-alpha", opacity)
        except Exception:
            pass

        self.canvas.delete("all")
        self.canvas.configure(width=tw, height=th)
        self._draw_toast_bg(self.canvas, tw, th, radius, bg_col, border_width, border_color)
        self._draw_toast_text(self.canvas, padx, pady, font_size, font_weight, emoji, fg_col)


class BrightnessWarningToast:
    def __init__(self, parent, settings, on_skip, on_decrease):
        self.parent = parent
        self.settings = settings
        self.on_skip = on_skip
        self.on_decrease = on_decrease
        self.window = None
        self.pos = "center"
        self.slot_index = 0

    def show(self):
        from services.aerohub_core.toast_utils import is_in_break_period_shared
        if is_in_break_period_shared():
            logger.info("Discarding BrightnessWarningToast because we are in a break period.")
            return
        if self.settings.get("is_preview", False):
            self._create_toast()
            return
        try:
            from services.aerohub_core.toast_utils import ToastQueue
            ToastQueue.add(self)
        except Exception:
            self._create_toast()

    def _create_toast(self):
        self.window = tk.Toplevel(self.parent)
        
        from services.aerohub_core.toast_utils import BaseToast
        with BaseToast._lock:
            BaseToast._active_toasts.append(self)
        self.window.title("Brightness Warning")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)

        trans_color = "#010203"
        self.window.configure(bg=trans_color)
        self.window.attributes("-transparentcolor", trans_color)

        bg_color = self.settings.get("bc_toast_bg_color", "#101625")
        fg_color = self.settings.get("bc_toast_fg_color", "#e2e8f0")
        accent_color = self.settings.get("bc_toast_accent_color", "#ff2a2a")
        emoji = self.settings.get("bc_toast_emoji", "⚠️")
        radius = int(self.settings.get("bc_toast_radius", 16))
        bw = int(self.settings.get("bc_toast_border_width", 1))
        bc = self.settings.get("bc_toast_border_color", "#7c3aed")
        pady = int(self.settings.get("bc_toast_padding_y", 10))

        # Sanitize empty/invalid colors
        if not bg_color or not bg_color.startswith("#"):
            bg_color = "#101625"
        if not fg_color or not fg_color.startswith("#"):
            fg_color = "#e2e8f0"
        if not accent_color or not accent_color.startswith("#"):
            accent_color = "#ff2a2a"
        if not emoji:
            emoji = "⚠️"
        if bg_color == trans_color:
            bg_color = "#020304"
        if fg_color == trans_color:
            fg_color = "#020304"
        if bc == trans_color:
            bc = "#020304"

        pos = self.settings.get("toast_pos", "Center").lower()
        w = int(self.settings.get("bc_toast_width", 320))
        h = int(self.settings.get("bc_toast_height", 145))
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()

        padding = 20
        if "left" in pos:
            x = padding
        elif "right" in pos:
            x = sw - w - padding
        else:
            x = (sw - w) // 2

        if "top" in pos or pos in ("left", "center", "right"):
            y = padding
        elif "bottom" in pos:
            y = sh - h - 50
        else:
            y = padding

        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # Register in shared status
        from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
        status = read_shared_status()
        status["active_toast_pid"] = os.getpid()
        duration = self.settings.get("bc_safe_duration_seconds", 30)
        status["active_toast_end_time"] = time.time() + duration + 2
        write_shared_status(status)

        self.canvas = tk.Canvas(
            self.window, width=w, height=h, bg=trans_color, highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        points = [
            radius, 0, w - radius, 0, w, 0, w, radius, w, h - radius, w, h,
            w - radius, h, radius, h, 0, h, 0, h - radius, 0, radius, 0, 0
        ]
        if bw > 0:
            self.canvas.create_polygon(
                points, smooth=True, fill=bg_color, outline=bc, width=bw
            )
        else:
            self.canvas.create_polygon(points, smooth=True, fill=bg_color)

        # Header text
        self.canvas.create_text(
            w // 2,
            15 + pady,
            anchor=tk.CENTER,
            text=f"{emoji} BRIGHTNESS TOO HIGH",
            font=("Consolas", 12, "bold"),
            fill=accent_color,
        )
        # Subtitle
        self.canvas.create_text(
            w // 2,
            15 + pady + 30,
            anchor=tk.CENTER,
            text="Reduce brightness for eye health?",
            font=("Consolas", 10),
            fill=fg_color,
        )

        # We can place buttons using canvas.create_window
        self._btn_frame = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.create_window(w // 2, 15 + pady + 75, window=self._btn_frame)

        btn_skip = tk.Button(
            self._btn_frame,
            text="SKIP",
            command=self._skip,
            bg="#1a233a",
            fg=fg_color,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=4,
        )
        btn_skip.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_skip, "#1a233a", bg_color, fg_color, fg_color)

        btn_dec = tk.Button(
            self._btn_frame,
            text="DECREASE",
            command=self._decrease,
            bg=accent_color,
            fg="#070b14",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=4,
        )
        btn_dec.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_dec, accent_color, "#ffffff", "#070b14", "#000000")

        self.window.bind("<Destroy>", self._on_destroy)

        def click_dismiss(event=None):
            if event and event.widget in (self.window, self.canvas):
                self._skip()

        self.window.bind("<Button-1>", click_dismiss)
        self.canvas.bind("<Button-1>", click_dismiss)
        self.window.bind("<ButtonRelease-1>", click_dismiss)
        self.canvas.bind("<ButtonRelease-1>", click_dismiss)

        # Auto-dismiss timer
        if duration > 0:
            self._auto_close_id = self.window.after(int(duration * 1000), self._skip)

        if self.settings.get("bc_toast_enable_sound", True):
            self._play_sound()

    def update_settings(self, settings):
        self.settings = settings
        if not self.window or not self.window.winfo_exists():
            return

        trans_color = "#010203"
        bg_color = self.settings.get("bc_toast_bg_color", "#101625")
        fg_color = self.settings.get("bc_toast_fg_color", "#e2e8f0")
        accent_color = self.settings.get("bc_toast_accent_color", "#ff2a2a")
        emoji = self.settings.get("bc_toast_emoji", "⚠️")
        radius = int(self.settings.get("bc_toast_radius", 16))
        bw = int(self.settings.get("bc_toast_border_width", 1))
        bc = self.settings.get("bc_toast_border_color", "#7c3aed")
        pady = int(self.settings.get("bc_toast_padding_y", 10))

        if not bg_color or not bg_color.startswith("#"):
            bg_color = "#101625"
        if not fg_color or not fg_color.startswith("#"):
            fg_color = "#e2e8f0"
        if not accent_color or not accent_color.startswith("#"):
            accent_color = "#ff2a2a"
        if not emoji:
            emoji = "⚠️"
        if bg_color == trans_color:
            bg_color = "#020304"
        if fg_color == trans_color:
            fg_color = "#020304"
        if bc == trans_color:
            bc = "#020304"

        pos = self.settings.get("toast_pos", "Center").lower()
        w = int(self.settings.get("bc_toast_width", 320))
        h = int(self.settings.get("bc_toast_height", 145))
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()

        padding = 20
        if "left" in pos:
            x = padding
        elif "right" in pos:
            x = sw - w - padding
        else:
            x = (sw - w) // 2

        if "top" in pos or pos in ("left", "center", "right"):
            y = padding
        elif "bottom" in pos:
            y = sh - h - 50
        else:
            y = padding

        try:
            self.window.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

        self.canvas.delete("all")
        self.canvas.configure(width=w, height=h)

        points = [
            radius, 0, w - radius, 0, w, 0, w, radius, w, h - radius, w, h,
            w - radius, h, radius, h, 0, h, 0, h - radius, 0, radius, 0, 0
        ]
        if bw > 0:
            self.canvas.create_polygon(points, smooth=True, fill=bg_color, outline=bc, width=bw)
        else:
            self.canvas.create_polygon(points, smooth=True, fill=bg_color)

        self.canvas.create_text(
            w // 2, 15 + pady, anchor=tk.CENTER,
            text=f"{emoji} BRIGHTNESS TOO HIGH", font=("Consolas", 12, "bold"), fill=accent_color
        )
        self.canvas.create_text(
            w // 2, 15 + pady + 30, anchor=tk.CENTER,
            text="Reduce brightness for eye health?", font=("Consolas", 10), fill=fg_color
        )

        if hasattr(self, "_btn_frame") and self._btn_frame:
            try:
                self._btn_frame.destroy()
            except Exception:
                pass
        self._btn_frame = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.create_window(w // 2, 15 + pady + 75, window=self._btn_frame)

        btn_skip = tk.Button(
            self._btn_frame, text="SKIP", command=self._skip,
            bg="#1a233a", fg=fg_color, relief=tk.FLAT, cursor="hand2", padx=15, pady=4
        )
        btn_skip.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_skip, "#1a233a", bg_color, fg_color, fg_color)

        btn_dec = tk.Button(
            self._btn_frame, text="DECREASE", command=self._decrease,
            bg=accent_color, fg="#070b14", relief=tk.FLAT, cursor="hand2", padx=15, pady=4
        )
        btn_dec.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_dec, accent_color, "#ffffff", "#070b14", "#000000")

    def force_close(self):
        try:
            self.window.destroy()
        except Exception:
            pass

    def _play_sound(self):
        try:
            import winsound

            snd_choice = self.settings.get("bc_toast_sound_effect", "mac_connect")
            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]

            if snd_choice in system_aliases:
                winsound.PlaySound(snd_choice, winsound.SND_ALIAS | winsound.SND_ASYNC)
            else:
                if not snd_choice.endswith(".wav"):
                    snd_choice += ".wav"

                path = os.path.join(APP_ROOT, "resources", "sounds", snd_choice)
                if not os.path.exists(path):
                    path = os.path.join(
                        os.path.dirname(APP_ROOT),
                        "BatteryMonitor",
                        "sounds",
                        snd_choice,
                    )

                if os.path.exists(path):
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            logger.error(f"Brightness Warning sound play error: {e}")

    def _skip(self):
        if hasattr(self, "_auto_close_id") and self._auto_close_id:
            try:
                self.window.after_cancel(self._auto_close_id)
            except Exception:
                pass
            self._auto_close_id = None
        if self.on_skip:
            self.on_skip()
        try:
            self.window.destroy()
        except Exception:
            pass

    def _decrease(self):
        if hasattr(self, "_auto_close_id") and self._auto_close_id:
            try:
                self.window.after_cancel(self._auto_close_id)
            except Exception:
                pass
            self._auto_close_id = None
        if self.on_decrease:
            self.on_decrease()
        try:
            self.window.destroy()
        except Exception:
            pass

    def _on_destroy(self, event):
        if event.widget == self.window:
            from services.aerohub_core.toast_utils import BaseToast
            with BaseToast._lock:
                if self in BaseToast._active_toasts:
                    BaseToast._active_toasts.remove(self)
            if hasattr(self, "_auto_close_id") and self._auto_close_id:
                try:
                    self.window.after_cancel(self._auto_close_id)
                except Exception:
                    pass
                self._auto_close_id = None
            try:
                from services.aerohub_core.toast_utils import read_shared_status, write_shared_status
                status = read_shared_status()
                if status.get("active_toast_pid") == os.getpid():
                    status["active_toast_pid"] = None
                    status["active_toast_end_time"] = 0.0
                    write_shared_status(status)
            except Exception:
                pass
            try:
                if not self.settings.get("is_preview", False):
                    from services.aerohub_core.toast_utils import ToastQueue
                    ToastQueue.on_toast_closed(self.parent)
            except Exception:
                pass
```

---

