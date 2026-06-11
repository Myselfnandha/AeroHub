<div align="center">

# AeroHub

**The Ultimate Windows Automation & Wellness Suite**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Windows 10/11](https://img.shields.io/badge/Windows-10%20%7C%2011-0078d4?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-Private-444?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Active-00ff88?style=for-the-badge)](.)

A highly modular suite of **8 background daemons, system tray utilities, and productivity toggles** — all orchestrated through a central headless System Tray Hub with a floating dashboard widget.

</div>

---

## Architecture

AeroHub follows a **hub-and-spoke** architecture. The central orchestrator (`AeroHub_Core`) manages the lifecycle of every child utility — starting, stopping, health-monitoring, and auto-restarting crashed processes.

```
AeroHub_Core (Orchestrator)
│
├── ClipboardManager ─── Background clipboard history with SQLite + GUI
├── HealthApp ────────── Eye break reminders, 8D audio, weather-based display warmth
├── MediaControl ─────── System-wide tray media controls (Prev │ Play/Pause │ Next)
├── BatteryMonitor ───── macOS-style charge/discharge toast notifications
├── TempMonitor ──────── CPU/GPU thermal monitoring with color-coded tray icon
├── TouchToggle ──────── One-click touchscreen enable/disable via tray
├── TgFdmProxy ──────── Telegram → Download Manager bridge (FDM / IDM / Neat)
└── TaskbarScroll ────── Scroll-wheel volume control on the Windows taskbar
```

### Developer Quickstart

- Install Python 3.12+ and add it to `PATH`
- Create a local `.env` from `.env.example`
- Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Run in development mode:

```powershell
./run.ps1 --env dev --port 8555
```

- Run in production mode:

```powershell
./run.ps1 --env prod --port 8555
```

- Run a utility with a consistent wrapper:

```powershell
./run_utility.ps1 --name BatteryMonitor
```

- Install AeroHub as a Windows service wrapper:

```powershell
./Launchers/install_aerohub_service.ps1
```

- Run AeroHub headless/service mode:

```powershell
python AeroHub_Core/aerohub.py --service
```

- Perform a self-update from git and restart AeroHub:

```powershell
python AeroHub_Core/aerohub.py --self-update
```

- Install TouchToggle startup service:

```powershell
./TouchToggle/install_touch_toggle_service.ps1
```

- Or install/uninstall from the Makefile:

```powershell
make service-install-touch
make service-uninstall-touch
```

- Local control API:

  - `GET http://127.0.0.1:8200/health`
  - `GET http://127.0.0.1:8200/status`
  - `GET http://127.0.0.1:8200/metrics`
  - `GET http://127.0.0.1:8200/control?action=start&service=<id>`
  - `GET http://127.0.0.1:8200/self-update`

  Use `X-Local-Token: <token>` or `?token=<token>` when `control_token` is configured.

- Validate formatting and linting:

```powershell
make precommit
make lint
```

- Run tests:

```powershell
make test
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **Per-utility `pythonw.exe` hardlinks** | Each tray icon gets its own unique process name so Windows groups them correctly in the system tray |
| **Native Win32 `DwmSetWindowAttribute`** | All GUI windows use DWM rounded corners on Windows 11 (DWMWA_WINDOW_CORNER_PREFERENCE = 33) |
| **UDP IPC for game mode** | AeroHub Core sends lightweight UDP packets to child services to pause/resume during fullscreen gaming |
| **Rotated log files** | Every module writes to `Logs/` with `RotatingFileHandler` (2–5 MB cap, 2–3 backups) — no log bloat |
| **Unique AppUserModelIDs** | Each process calls `SetCurrentProcessExplicitAppUserModelID` so Windows identifies each tray icon separately |

---

## Modules

### 1. AeroHub Core — The Orchestrator

> `AeroHub_Core/aerohub.py` · ~1120 lines

The nerve center. Runs in the background with a **system tray icon** and a **draggable floating dashboard widget** in the desktop corner.

- **Lifecycle Manager** — Auto-starts configured processes, monitors health every 3 seconds, auto-restarts crashes after a configurable delay
- **Floating Dashboard** — Shows each process name, status dot (●), uptime, toggle (▶/■), and restart (↻) buttons
- **AeroEco Game Mode** — Detects fullscreen/DirectX games via `SHQueryUserNotificationState` and foreground window analysis:
  - **Pauses TempMonitor** completely during gameplay
  - **Restricts HealthApp** to `IDLE` priority, disabling heavy UI/audio calls
  - Resumes all services after game exits with hysteresis (15s cooldown)
- **Config-driven** — `aerohub_config.json` defines all managed processes with `auto_start` and `enabled` flags

---

### 2. Clipboard Manager

> `ClipboardManager/clipboard_manager.py` · ~924 lines

A full-featured clipboard history tracker with persistent storage and a searchable GUI.

- **Win32 Clipboard Listener** — Uses `WM_CLIPBOARDUPDATE` via a hidden window (64-bit safe `WNDPROC` ctypes definitions)
- **SQLite Storage** — Unlimited history with MD5 deduplication against the last entry
- **Searchable GUI** — Split-pane layout with list + preview, right-click context menu, double-click to re-copy
- **Auto-Export** — When entries exceed a configurable threshold (default 1000), the oldest batch is exported to Markdown and pruned
- **Settings Window** — Configurable max entries, export batch size, and auto-export toggle

---

### 3. Health App — Eye Break Reminder

> `HealthApp/health_app.py` · ~1688 lines

A premium desktop wellness companion with configurable break schedules, fullscreen lock overlays, and ambient audio.

- **Break Schedule** — Configurable short breaks (default 20min/15s) and long breaks (60min/60s)
- **Pre-Break Warning Toast** — Animated slide-in notification with customizable position, colors, fonts, border, and animation style (slide or fade)
- **Full-Screen Break Overlay** — Black overlay on all monitors with countdown timer, breathing text animation, and forced focus keeping
- **8D Spatial Audio** — Procedurally generates a stereo WAV with breathing-like tones and binaural panning effect. Also supports random ambient tracks from `resources/ambient/`
- **Media-Aware** — Pauses active media sessions via Windows SDK (`GlobalSystemMediaTransportControlsSessionManager`) before breaks and resumes them after. Falls back to global `VK_MEDIA_PLAY_PAUSE` key
- **Weather-Based Display Warmth** — Fetches weather from Open-Meteo API, applies color temperature via Windows gamma ramps (`SetDeviceGammaRamp`). Dynamic Kelvin adjustment based on sunset/sunrise and ambient temperature
- **Late-Night Dimming** — Gradual screen brightness reduction during configurable night hours
- **Workstation Lock Detection** — Skips breaks when the workstation is locked (`OpenInputDesktop`)
- **Settings GUI** — Full tkinter settings panel for break intervals, sound, dimming, weather coordinates, and toast appearance

---

### 4. Media Control

> `MediaControl/media_control.py` · ~886 lines

System-wide media playback controls running as three separate **Win32 notification area icons** in the taskbar.

- **3 Tray Icons** — Previous │ Play/Pause │ Next, each as an independent system tray icon with click-to-action
- **Windows SDK Integration** — Uses `winsdk.windows.media.control.SessionManager` for real-time playback status detection and per-session control
- **Dynamic Play/Pause State** — Icon automatically switches between ▶ and ⏸ based on active playback status
- **Click Animation** — Press-and-release visual feedback with 120ms revert timing
- **Theme-Aware** — Detects Windows light/dark mode + accent color via registry, regenerates all icons on theme change
- **Pycaw Fallback** — For media players that don't register SMTC sessions (VLC, MPC-HC, iTunes), falls back to pycaw audio session enumeration
- **Smart Multi-Session** — Deduplicates sessions by app ID, pauses all when multiple are playing

---

### 5. Battery Monitor

> `BatteryMonitor/battery_monitor.py` · ~662 lines

macOS-style charging notifications for Windows laptops.

- **Plug/Unplug Detection** — Plays custom WAV sound effects (`mac_connect.wav` / `mac_disconnect.wav`) on charger state change
- **Animated Toast Notifications** — macOS-style slide-in toasts with rounded corners, icon background, close-on-hover, and auto-dismiss. Multiple toasts stack vertically
- **Threshold Alerts** — Configurable low battery warning (default 20%) and full charge alert (default 93%)
- **Theme-Aware Tray Icon** — Battery-shaped icon with fill level, color coding (green=charging, gray=discharging, red=low), and a lightning bolt overlay when plugged in. Adapts to Windows light/dark theme
- **Settings GUI** — Configurable thresholds and sound toggle

---

### 6. Temperature Monitor

> `TempMonitor/temp_monitor.py` · ~911 lines

CPU/GPU thermal monitoring with a live temperature display in the system tray.

- **Multi-Backend Reader**:
  1. **LibreHardwareMonitor** — Primary. Uses pythonnet to load `LibreHardwareMonitorLib.dll` for accurate CPU, GPU, SSD, and motherboard readings
  2. **WMI** — Fallback. Reads `MSAcpi_ThermalZoneTemperature` or `OpenHardwareMonitor` WMI namespace
  3. **Simulated** — Final fallback with sine-wave oscillating dummy data for display testing
- **Color-Coded Tray Icon** — Displays temperature as a number on a colored rounded rectangle (green < 60°C, yellow < 75°C, orange < 85°C, red ≥ 85°C)
- **Temperature Alerts** — Warning and critical toast notifications with flashing animation for critical severity
- **Dynamic Tooltip** — Shows all detected sensor temperatures in the tray hover tooltip with intelligent sensor name shortening
- **Sensor Selection Menu** — Right-click menu lets you pick which sensor drives the tray icon display
- **Settings GUI** — Configurable warning/critical temperature thresholds

---

### 7. Touch Toggle

> `TouchToggle/touch_toggle.py` · ~506 lines

Instantly enables or disables the laptop touchscreen from the system tray.

- **One-Click Toggle** — Left-click the tray icon to toggle the HID touch screen device
- **Elevated Execution** — Runs `TouchToggle.ps1` via `ShellExecuteExW` with `runas` verb for proper UAC elevation (no extra console window)
- **State Detection** — Queries `Get-PnpDevice -Class 'HIDClass'` to determine current touch screen status
- **Toast FX Customization** — Sleek animated toast notifications (Slide/Fade) indicating the touchscreen status, with full control over colors, sizing, corner rounding, and border strokes.
- **Settings GUI** — Dedicated Tkinter dashboard to customize the toast appearance and preview animations in real-time.
- **Visual Feedback** — Green circle (ON) / Red circle (OFF) tray icon indicating the system state.

---

### 8. Telegram FDM Proxy

> `TgFdmProxy/tg_fdm_proxy.py` · ~2166 lines

A Telegram bot that bridges file messages to your installed download manager (FDM, IDM, or Neat DM).

- **Multi-Manager Support** — Auto-detects installed download managers via Windows Registry → `where.exe` → hardcoded fallback paths. Priority: FDM → IDM → Neat DM
- **HTTP Range Proxy** — Runs a local `aiohttp` server that streams Telegram media chunks, supporting HTTP Range headers for multi-threaded downloading
- **Parallel Chunk Downloader** — Optional parallel download mode with configurable concurrency and retry logic
- **Smart Auto-Rename** — Cleans raw filenames into `Title (Year) [Resolution].ext` format, stripping codec/audio/source noise
- **Quality Variant Selection** — Waits for multiple quality variants (configurable delay) before picking the best
- **Keyword Filters** — Block/allow lists for automated content filtering
- **Duplicate Guard** — Tracks `(chat_id, message_id)` with TTL to prevent re-triggering
- **Interactive Setup** — First-run wizard prompts for API_ID, API_HASH, and BOT_TOKEN
- **Live Event Dashboard** — In-memory structured event log with a GUI log viewer
- **Docker Support** — Includes `Dockerfile` and `docker-compose.yml`

---

### 9. Taskbar Scroll Controller

> `TaskbarScroll/taskbar_scroll.py` · ~222 lines

Scroll-wheel volume control when hovering over the Windows taskbar.

- **Taskbar Detection** — Identifies `Shell_TrayWnd` and `Shell_SecondaryTrayWnd` window classes using `WindowFromPoint` with DPI-aware cursor coordinates
- **Configurable** — Invert scroll direction and volume step multiplier via settings GUI
- **Singleton Guard** — Uses a Windows named mutex to prevent duplicate instances
- **Settings GUI** — AeroHub-themed settings window with DWM rounded corners

---

## Directory Structure

```
UTILITIES/
├── AeroHub_Core/           # Central orchestrator
│   ├── aerohub.py
│   └── aerohub_config.json
├── ClipboardManager/       # Clipboard history daemon
│   ├── clipboard_manager.py
│   ├── clipboard_history.db
│   ├── config.json
│   └── exports/
├── HealthApp/              # Eye break & wellness
│   ├── health_app.py
│   ├── settings.json
│   ├── breathing_8d.wav
│   └── resources/
│       ├── ambient/        # Break audio tracks
│       ├── on_pre_break.wav
│       └── on_stop_break.wav
├── MediaControl/           # Tray media controls
│   ├── media_control.py
│   ├── assets/
│   └── requirements.txt
├── BatteryMonitor/         # Battery notifications
│   ├── battery_monitor.py
│   ├── settings.json
│   └── sounds/             # mac_connect.wav, mac_disconnect.wav
├── TempMonitor/            # Thermal monitoring
│   └── temp_monitor.py
├── TouchToggle/            # Touchscreen toggle
│   ├── touch_toggle.py
│   ├── touch_settings.json
│   ├── TouchToggle.ps1
│   ├── TouchToggle.exe
│   └── tooltip_notifier.py
├── TgFdmProxy/             # Telegram download bridge
│   ├── tg_fdm_proxy.py
│   ├── .env
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── tg_fdm_proxy.exe
├── TaskbarScroll/          # Volume scroll control
│   ├── taskbar_scroll.py
│   └── settings.json
├── Launchers/              # Setup & startup scripts
│   ├── install.bat
│   ├── install_elevated_startup.bat
│   ├── run_aerohub.bat
│   ├── run_aerohub.vbs
│   └── check_logs.ps1
├── Logs/                   # Centralized rotating logs
├── services/               # Runtime data (sessions, DBs)
└── requirements.txt        # Python dependencies
```

---

## Installation

### Prerequisites

- **Python 3.10+** — must be on your System `PATH`
- **Windows 10 / 11**
- **pip** — included with Python

### Quick Start

```cmd
:: 1. Clone the repository
git clone https://github.com/Myselfnandha/AeroHub.git
cd AeroHub

:: 2. Install dependencies
Launchers\install.bat

:: 3. Launch AeroHub
Launchers\run_aerohub.bat
```

### Silent Startup (Administrator)

To configure AeroHub to start **automatically and silently** as Administrator on system logon (bypasses UAC prompts via Windows Task Scheduler):

```cmd
:: Right-click → Run as Administrator
Launchers\install_elevated_startup.bat
```

This creates a scheduled task (`AeroHub_ElevatedStartup`) that runs `run_aerohub.vbs` at logon with highest privileges.

### Individual Modules

Each module can run independently:

```cmd
python AeroHub_Core\aerohub.py         # Full orchestrator
python ClipboardManager\clipboard_manager.py
python HealthApp\health_app.py
python MediaControl\media_control.py
python BatteryMonitor\battery_monitor.py
python TempMonitor\temp_monitor.py
python TouchToggle\touch_toggle.py
python TgFdmProxy\tg_fdm_proxy.py
python TaskbarScroll\taskbar_scroll.py
```

---

## Dependencies

```
pywin32>=306        # Win32 API access (clipboard, COM)
psutil>=5.9         # Process management, battery info
pystray>=0.19       # System tray icons
Pillow>=10.0        # Icon generation
pygame>=2.5         # Audio playback (Health App)
requests>=2.31      # Weather API (Health App)
wmi>=1.5            # Temperature reading fallback
screen-brightness-control>=0.22  # Brightness management
pythonnet>=3.0      # LibreHardwareMonitor DLL loading
plyer>=2.1          # Cross-platform notifications
```

Additional per-module dependencies:
- **MediaControl**: `winsdk`, `pycaw`, `pywin32`
- **TaskbarScroll**: `pynput`
- **TgFdmProxy**: `telethon`, `aiohttp`, `python-dotenv`

---

## Configuration

### AeroHub Core Config

Edit `AeroHub_Core/aerohub_config.json` to control which processes auto-start:

```json
{
  "auto_start": true,
  "restart_delay_sec": 5,
  "processes": [
    {
      "id": "clipboard_manager",
      "name": "Clipboard Manager",
      "script": "ClipboardManager/clipboard_manager.py",
      "auto_start": true,
      "enabled": true
    }
  ]
}
```

### Per-Module Settings

Each module stores its settings in a local `settings.json` or `config.json` within its directory. All settings are editable via the module's tray icon right-click → Settings GUI.

---

## Design Philosophy

| Principle | Implementation |
|---|---|
| **Non-Intrusive** | All services run headless via `pythonw.exe` with `CREATE_NO_WINDOW`. No command prompts spawn unless explicitly requested |
| **Context-Aware Theming** | Reads Windows registry (`SystemUsesLightTheme`, `ColorPrevalence`, `AccentColor`) to adapt tray icons and GUIs dynamically |
| **Frictionless UX** | Hover states on all interactive elements, generous click targets, smooth fade/slide animations (ease-out cubic), no layout shifts |
| **Terminal Aesthetics** | Setup scripts use ANSI colors — Cyan for steps, Green for success, Red for errors |
| **Crash Resilience** | AeroHub Core monitors child process health every 3 seconds and auto-restarts crashed services with configurable delay |

---

## License

Private repository. All rights reserved.
