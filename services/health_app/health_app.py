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
        self._brightness_is_adjusting = False

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

                if getattr(self, "_brightness_is_adjusting", False):
                    high_start = None
                    time.sleep(5)
                    continue

                if not self.settings.get("bc_enabled", True) or not SBC_AVAILABLE or time.time() < self.settings.get("bc_skip_until", 0.0):
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
                        try:
                            start_parts = start_time.split(":")
                            dt_now = datetime.datetime.now()
                            dt_start = dt_now.replace(
                                hour=int(start_parts[0]),
                                minute=int(start_parts[1]),
                                second=0,
                                microsecond=0,
                            )
                            if dt_start > dt_now:
                                dt_start -= datetime.timedelta(days=1)
                            high_start = dt_start.timestamp()
                        except Exception:
                            high_start = now
                    
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

    def _decrease_brightness(self, is_aggressive=False, on_update=None, on_complete=None):
        if SBC_AVAILABLE:
            try:
                self._brightness_is_adjusting = True
                target_b = self.settings.get("bc_target_brightness", 2)
                trans_sec = self.settings.get("bc_aggressive_transition_time_sec", 30) if is_aggressive else self.settings.get("bc_transition_time_sec", 5)
                
                b_list = sbc.get_brightness()
                start_b = int(b_list[0]) if isinstance(b_list, list) and b_list else int(b_list)
                
                def fade():
                    try:
                        total_diff = target_b - start_b
                        if total_diff == 0:
                            if on_complete:
                                on_complete()
                            logger.info(f"Target brightness {target_b}% reached. Cooling down for 10s...")
                            time.sleep(10)
                            return

                        # Ensure WMI is not flooded; limit steps to at most 2 updates per second (min 0.5s delay)
                        min_delay = 0.5
                        max_updates = int(trans_sec / min_delay)
                        if max_updates <= 0:
                            max_updates = 1
                        
                        num_updates = min(abs(total_diff), max_updates)
                        step_delay = trans_sec / num_updates
                        
                        last_set_val = start_b
                        for i in range(1, num_updates + 1):
                            val = start_b + total_diff * (i / num_updates)
                            curr_val = int(round(val))
                            if curr_val != last_set_val:
                                sbc.set_brightness(curr_val)
                                last_set_val = curr_val
                            if on_update:
                                on_update(curr_val)
                            time.sleep(step_delay)
                        
                        if last_set_val != target_b:
                            sbc.set_brightness(target_b)
                        if on_update:
                            on_update(target_b)
                            
                        # Immediately trigger GUI completion (which destroys the toast window)
                        if on_complete:
                            on_complete()
                        
                        # Cool down for 10 seconds post-fade to allow OS brightness values to settle
                        logger.info(f"Target brightness {target_b}% reached. Cooling down for 10s...")
                        time.sleep(10)
                    except Exception as fe:
                        logger.error(f"Fading error: {fe}")
                        if on_complete:
                            on_complete()
                    finally:
                        self._brightness_is_adjusting = False
                
                threading.Thread(target=fade, daemon=True).start()
            except Exception as e:
                self._brightness_is_adjusting = False
                logger.error(f"Failed to decrease brightness: {e}")
                if on_complete:
                    on_complete()
        else:
            if on_complete:
                on_complete()

    def _skip_brightness_warning(self):
        logger.info("Brightness warning skipped by user.")

    def _skip_brightness_permanent(self):
        logger.info("Brightness warning skipped permanently (until midnight) by user.")
        import datetime
        now = datetime.datetime.now()
        tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time.min)
        midnight_ts = tomorrow.timestamp()
        self.settings["bc_skip_until"] = midnight_ts
        save_settings(self.settings)

    def _skip_brightness_duration(self, minutes):
        logger.info(f"Brightness warning skipped for {minutes} minutes by user.")
        self.settings["bc_skip_until"] = time.time() + minutes * 60
        save_settings(self.settings)

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
                    
                    toast_ref = BrightnessWarningToast(
                        self.root,
                        self.settings,
                        on_skip=self._skip_brightness_warning,
                        on_decrease=lambda on_complete, agg=is_agg: self._decrease_brightness(
                            agg,
                            on_update=lambda val: toast_ref.update_progress_text(val),
                            on_complete=on_complete
                        ),
                        on_skip_permanent=self._skip_brightness_permanent,
                        on_skip_duration=self._skip_brightness_duration,
                    )
                    toast_ref.show()
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
