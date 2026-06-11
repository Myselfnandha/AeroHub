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
