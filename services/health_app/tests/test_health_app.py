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

