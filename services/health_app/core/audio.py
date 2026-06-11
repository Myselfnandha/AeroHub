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

