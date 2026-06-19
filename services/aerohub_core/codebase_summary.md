# Codebase Summary: aerohub_core

## Overview
- **Scan Date:** 2026-06-14 00:29:50
- **Source Folder:** `C:\Users\NANDHA A\Desktop\FOLDERS\UTILITIES\services\aerohub_core`
- **Total Text Files:** 7
- **Estimated Token Count:** 51,764

## Directory Tree
```text
aerohub_core/
├── Logs/
│   └── app.log
├── aerohub.py
├── aerohub_config.json
├── remote_control.py
├── system_utils.py
├── toast_status.json
└── toast_utils.py
```

## File Contents

### File: `Logs/app.log`
- **Path:** `Logs/app.log`
- **Estimated Tokens:** 22,080
- **mtime:** 1781376560.116

```
{"timestamp": "2026-06-10 00:14:05,606", "level": "INFO", "logger": "AeroHub", "message": "✓ Running with Administrator privileges.", "module": "aerohub", "filename": "aerohub.py", "line": 1334}
{"timestamp": "2026-06-10 00:14:05,612", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1237}
{"timestamp": "2026-06-10 00:14:05,613", "level": "INFO", "logger": "AeroHub", "message": "  AeroHub Core starting...", "module": "aerohub", "filename": "aerohub.py", "line": 1238}
{"timestamp": "2026-06-10 00:14:05,613", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1239}
{"timestamp": "2026-06-10 00:14:05,614", "level": "INFO", "logger": "AeroHub", "message": "Utilities directory: C:\\Users\\NANDHA A\\Desktop\\FOLDERS\\UTILITIES", "module": "aerohub", "filename": "aerohub.py", "line": 1240}
{"timestamp": "2026-06-10 00:14:05,614", "level": "INFO", "logger": "AeroHub", "message": "Managed processes: 8", "module": "aerohub", "filename": "aerohub.py", "line": 1241}
{"timestamp": "2026-06-10 00:14:05,614", "level": "INFO", "logger": "AeroHub", "message": "Headless mode: False", "module": "aerohub", "filename": "aerohub.py", "line": 1242}
{"timestamp": "2026-06-10 00:14:05,621", "level": "INFO", "logger": "AeroHub", "message": "Cleared 5 stale tray icon registry entries.", "module": "aerohub", "filename": "aerohub.py", "line": 1184}
{"timestamp": "2026-06-10 00:14:05,698", "level": "INFO", "logger": "AeroHub", "message": "Control API listening on http://127.0.0.1:8200", "module": "aerohub", "filename": "aerohub.py", "line": 1259}
{"timestamp": "2026-06-10 00:14:05,699", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Clipboard Manager", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:06,884", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Started (PID 15708)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:07,885", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Health App", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:07,896", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 11868)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:08,340", "level": "INFO", "logger": "AeroHub", "message": "AeroHub dashboard running.", "module": "aerohub", "filename": "aerohub.py", "line": 1321}
{"timestamp": "2026-06-10 00:14:08,897", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Media Control", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:08,922", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Started (PID 21028)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:09,924", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Battery Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:09,959", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Started (PID 22336)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:10,960", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Temp Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:10,972", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Started (PID 23124)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:11,973", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Touch Toggle", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:11,987", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Started (PID 13984)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:12,990", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Telegram FDM Proxy", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:13,003", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 9380)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:13,626", "level": "INFO", "logger": "AeroHub", "message": "Promoted 4 tray icon(s) to always-visible.", "module": "aerohub", "filename": "aerohub.py", "line": 1225}
{"timestamp": "2026-06-10 00:14:14,004", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Taskbar Scroll Controller", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 00:14:14,021", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Started (PID 7796)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:20,813", "level": "WARNING", "logger": "AeroHub", "message": "[health_app] Exited with code 0", "module": "aerohub", "filename": "aerohub.py", "line": 359}
{"timestamp": "2026-06-10 00:14:51,352", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 16120)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 00:14:54,207", "level": "WARNING", "logger": "AeroHub", "message": "[health_app] Exited with code 0", "module": "aerohub", "filename": "aerohub.py", "line": 359}
{"timestamp": "2026-06-10 15:24:11,418", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 975}
{"timestamp": "2026-06-10 15:24:11,420", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 919}
{"timestamp": "2026-06-10 15:24:11,422", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 919}
{"timestamp": "2026-06-10 15:24:14,424", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 962}
{"timestamp": "2026-06-10 15:24:20,427", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 989}
{"timestamp": "2026-06-10 15:24:20,427", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 919}
{"timestamp": "2026-06-10 15:24:50,438", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1012}
{"timestamp": "2026-06-10 15:31:27,140", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 18252)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 15:32:08,282", "level": "INFO", "logger": "AeroHub", "message": "AeroHub shutting down — stopping all processes...", "module": "aerohub", "filename": "aerohub.py", "line": 1132}
{"timestamp": "2026-06-10 15:32:08,328", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Stopped (PID 15708)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,365", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Stopped (PID 18252)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,384", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Stopped (PID 21028)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,403", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Stopped (PID 22336)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,426", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Stopped (PID 23124)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,442", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Stopped (PID 13984)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,464", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Stopped (PID 9380)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 15:32:08,481", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Stopped (PID 7796)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:43:54,042", "level": "INFO", "logger": "AeroHub", "message": "✓ Running with Administrator privileges.", "module": "aerohub", "filename": "aerohub.py", "line": 1334}
{"timestamp": "2026-06-10 23:43:54,057", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1237}
{"timestamp": "2026-06-10 23:43:54,057", "level": "INFO", "logger": "AeroHub", "message": "  AeroHub Core starting...", "module": "aerohub", "filename": "aerohub.py", "line": 1238}
{"timestamp": "2026-06-10 23:43:54,058", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1239}
{"timestamp": "2026-06-10 23:43:54,058", "level": "INFO", "logger": "AeroHub", "message": "Utilities directory: C:\\Users\\NANDHA A\\Desktop\\FOLDERS\\UTILITIES", "module": "aerohub", "filename": "aerohub.py", "line": 1240}
{"timestamp": "2026-06-10 23:43:54,059", "level": "INFO", "logger": "AeroHub", "message": "Managed processes: 8", "module": "aerohub", "filename": "aerohub.py", "line": 1241}
{"timestamp": "2026-06-10 23:43:54,059", "level": "INFO", "logger": "AeroHub", "message": "Headless mode: False", "module": "aerohub", "filename": "aerohub.py", "line": 1242}
{"timestamp": "2026-06-10 23:43:54,096", "level": "INFO", "logger": "AeroHub", "message": "Control API listening on http://127.0.0.1:8200", "module": "aerohub", "filename": "aerohub.py", "line": 1259}
{"timestamp": "2026-06-10 23:43:54,098", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Clipboard Manager", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:43:54,297", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Started (PID 26484)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:43:55,299", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Health App", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:43:55,314", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 14740)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:43:55,852", "level": "INFO", "logger": "AeroHub", "message": "AeroHub dashboard running.", "module": "aerohub", "filename": "aerohub.py", "line": 1321}
{"timestamp": "2026-06-10 23:43:56,315", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Media Control", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:43:56,332", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Started (PID 10152)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:43:57,333", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Battery Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:43:57,354", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Started (PID 21284)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:43:58,355", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Temp Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:43:58,371", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Started (PID 23316)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:43:59,373", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Touch Toggle", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:43:59,392", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Started (PID 4152)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:44:00,392", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Telegram FDM Proxy", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:44:00,410", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 22240)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:44:01,412", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Taskbar Scroll Controller", "module": "aerohub", "filename": "aerohub.py", "line": 794}
{"timestamp": "2026-06-10 23:44:01,429", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Started (PID 19676)", "module": "aerohub", "filename": "aerohub.py", "line": 299}
{"timestamp": "2026-06-10 23:46:18,376", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 975}
{"timestamp": "2026-06-10 23:46:18,378", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 919}
{"timestamp": "2026-06-10 23:46:18,379", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 919}
{"timestamp": "2026-06-10 23:46:21,381", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 962}
{"timestamp": "2026-06-10 23:46:30,386", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 989}
{"timestamp": "2026-06-10 23:46:30,387", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 919}
{"timestamp": "2026-06-10 23:47:00,406", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1012}
{"timestamp": "2026-06-10 23:56:23,873", "level": "INFO", "logger": "AeroHub", "message": "AeroHub shutting down — stopping all processes...", "module": "aerohub", "filename": "aerohub.py", "line": 1132}
{"timestamp": "2026-06-10 23:56:23,906", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Stopped (PID 26484)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:23,952", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Stopped (PID 14740)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:23,980", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Stopped (PID 10152)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:24,006", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Stopped (PID 21284)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:24,042", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Stopped (PID 23316)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:24,066", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Stopped (PID 4152)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:24,100", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Stopped (PID 22240)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-10 23:56:24,127", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Stopped (PID 19676)", "module": "aerohub", "filename": "aerohub.py", "line": 332}
{"timestamp": "2026-06-12 14:40:12,895", "level": "INFO", "logger": "AeroHub", "message": "✓ Running with Administrator privileges.", "module": "aerohub", "filename": "aerohub.py", "line": 1336}
{"timestamp": "2026-06-12 14:40:12,899", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1239}
{"timestamp": "2026-06-12 14:40:12,899", "level": "INFO", "logger": "AeroHub", "message": "  AeroHub Core starting...", "module": "aerohub", "filename": "aerohub.py", "line": 1240}
{"timestamp": "2026-06-12 14:40:12,899", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1241}
{"timestamp": "2026-06-12 14:40:12,899", "level": "INFO", "logger": "AeroHub", "message": "Utilities directory: C:\\Users\\NANDHA A\\Desktop\\FOLDERS\\UTILITIES", "module": "aerohub", "filename": "aerohub.py", "line": 1242}
{"timestamp": "2026-06-12 14:40:12,899", "level": "INFO", "logger": "AeroHub", "message": "Managed processes: 8", "module": "aerohub", "filename": "aerohub.py", "line": 1243}
{"timestamp": "2026-06-12 14:40:12,899", "level": "INFO", "logger": "AeroHub", "message": "Headless mode: False", "module": "aerohub", "filename": "aerohub.py", "line": 1244}
{"timestamp": "2026-06-12 14:40:12,910", "level": "INFO", "logger": "AeroHub", "message": "Cleared 10 stale tray icon registry entries.", "module": "aerohub", "filename": "aerohub.py", "line": 1186}
{"timestamp": "2026-06-12 14:40:12,932", "level": "INFO", "logger": "AeroHub", "message": "Control API listening on http://127.0.0.1:8200", "module": "aerohub", "filename": "aerohub.py", "line": 1261}
{"timestamp": "2026-06-12 14:40:12,932", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Clipboard Manager", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:13,095", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Started (PID 15844)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:14,097", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Health App", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:14,120", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 13124)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:14,479", "level": "INFO", "logger": "AeroHub", "message": "AeroHub dashboard running.", "module": "aerohub", "filename": "aerohub.py", "line": 1323}
{"timestamp": "2026-06-12 14:40:15,121", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Media Control", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:15,129", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Started (PID 21272)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:16,130", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Battery Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:16,164", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Started (PID 23576)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:17,164", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Temp Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:17,215", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Started (PID 23260)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:18,216", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Touch Toggle", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:18,244", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Started (PID 4000)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:19,245", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Telegram FDM Proxy", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:19,264", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 18028)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:20,265", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Taskbar Scroll Controller", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 14:40:20,300", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Started (PID 4228)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:21,959", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Exited with code 1", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 14:40:21,960", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Detected crash for running process", "module": "aerohub", "filename": "aerohub.py", "line": 809}
{"timestamp": "2026-06-12 14:40:21,960", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 14:40:26", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 14:40:24,974", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 14:40:26", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 14:40:28,061", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Crashed! Auto-restarting in 5s...", "module": "aerohub", "filename": "aerohub.py", "line": 822}
{"timestamp": "2026-06-12 14:40:33,137", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 15904)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:36,195", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Exited with code 1", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 14:40:36,195", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Detected crash for running process", "module": "aerohub", "filename": "aerohub.py", "line": 809}
{"timestamp": "2026-06-12 14:40:36,195", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 14:40:46", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 14:40:39,214", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 14:40:46", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 14:40:42,322", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 14:40:46", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 14:40:45,485", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 14:40:46", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 14:40:48,496", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Crashed! Auto-restarting in 5s...", "module": "aerohub", "filename": "aerohub.py", "line": 822}
{"timestamp": "2026-06-12 14:40:53,499", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 3456)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 14:40:56,649", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Exited with code 1", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 14:40:56,650", "level": "ERROR", "logger": "AeroHub", "message": "[tg_fdm_proxy] Circuit breaker triggered after 3 failures", "module": "aerohub", "filename": "aerohub.py", "line": 374}
{"timestamp": "2026-06-12 14:52:20,730", "level": "INFO", "logger": "AeroHub", "message": "AeroHub shutting down — stopping all processes...", "module": "aerohub", "filename": "aerohub.py", "line": 1134}
{"timestamp": "2026-06-12 14:52:20,761", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Stopped (PID 15844)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 14:52:20,823", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Stopped (PID 13124)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 14:52:20,862", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Stopped (PID 21272)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 14:52:20,901", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Stopped (PID 23576)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 14:52:20,946", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Stopped (PID 23260)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 14:52:20,979", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Stopped (PID 4000)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 14:52:21,009", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Stopped (PID 4228)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 15:02:46,933", "level": "INFO", "logger": "AeroHub", "message": "✓ Running with Administrator privileges.", "module": "aerohub", "filename": "aerohub.py", "line": 1336}
{"timestamp": "2026-06-12 15:02:46,940", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1239}
{"timestamp": "2026-06-12 15:02:46,940", "level": "INFO", "logger": "AeroHub", "message": "  AeroHub Core starting...", "module": "aerohub", "filename": "aerohub.py", "line": 1240}
{"timestamp": "2026-06-12 15:02:46,940", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1241}
{"timestamp": "2026-06-12 15:02:46,940", "level": "INFO", "logger": "AeroHub", "message": "Utilities directory: C:\\Users\\NANDHA A\\Desktop\\FOLDERS\\UTILITIES", "module": "aerohub", "filename": "aerohub.py", "line": 1242}
{"timestamp": "2026-06-12 15:02:46,940", "level": "INFO", "logger": "AeroHub", "message": "Managed processes: 8", "module": "aerohub", "filename": "aerohub.py", "line": 1243}
{"timestamp": "2026-06-12 15:02:46,940", "level": "INFO", "logger": "AeroHub", "message": "Headless mode: False", "module": "aerohub", "filename": "aerohub.py", "line": 1244}
{"timestamp": "2026-06-12 15:02:46,943", "level": "INFO", "logger": "AeroHub", "message": "Cleared 1 stale tray icon registry entries.", "module": "aerohub", "filename": "aerohub.py", "line": 1186}
{"timestamp": "2026-06-12 15:02:46,964", "level": "INFO", "logger": "AeroHub", "message": "Control API listening on http://127.0.0.1:8200", "module": "aerohub", "filename": "aerohub.py", "line": 1261}
{"timestamp": "2026-06-12 15:02:46,964", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Clipboard Manager", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:47,120", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Started (PID 21784)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:48,122", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Health App", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:48,211", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 20464)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:48,548", "level": "INFO", "logger": "AeroHub", "message": "AeroHub dashboard running.", "module": "aerohub", "filename": "aerohub.py", "line": 1323}
{"timestamp": "2026-06-12 15:02:49,212", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Media Control", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:49,225", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Started (PID 23932)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:50,226", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Battery Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:50,235", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Started (PID 9016)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:51,236", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Temp Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:51,250", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Started (PID 17656)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:52,251", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Touch Toggle", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:52,266", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Started (PID 9740)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:53,267", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Telegram FDM Proxy", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:53,281", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 2920)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:02:54,282", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Taskbar Scroll Controller", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 15:02:54,299", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Started (PID 9040)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 15:50:47,274", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Exited with code 1", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 15:50:47,275", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Detected crash for running process", "module": "aerohub", "filename": "aerohub.py", "line": 809}
{"timestamp": "2026-06-12 15:50:47,276", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 15:50:52", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 15:50:50,331", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 15:50:52", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 15:50:53,385", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Crashed! Auto-restarting in 5s...", "module": "aerohub", "filename": "aerohub.py", "line": 822}
{"timestamp": "2026-06-12 15:50:58,415", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 23584)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 17:22:14,132", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 17:22:14,134", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 17:22:14,135", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 18:32:49,882", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 18:33:04,922", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 18:33:04,924", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 18:33:34,937", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 18:33:46,942", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 18:33:46,943", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 18:33:46,943", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 18:33:49,952", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 18:48:17,333", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 18:48:17,334", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 18:48:47,345", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 19:02:56,614", "level": "INFO", "logger": "AeroHub", "message": "AeroHub shutting down — stopping all processes...", "module": "aerohub", "filename": "aerohub.py", "line": 1134}
{"timestamp": "2026-06-12 19:02:56,633", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Stopped (PID 21784)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,672", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Stopped (PID 20464)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,697", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Stopped (PID 23932)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,726", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Stopped (PID 9016)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,752", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Stopped (PID 17656)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,772", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Stopped (PID 9740)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,815", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Stopped (PID 23584)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:02:56,832", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Stopped (PID 9040)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:03:02,673", "level": "INFO", "logger": "AeroHub", "message": "✓ Running with Administrator privileges.", "module": "aerohub", "filename": "aerohub.py", "line": 1336}
{"timestamp": "2026-06-12 19:03:02,689", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1239}
{"timestamp": "2026-06-12 19:03:02,690", "level": "INFO", "logger": "AeroHub", "message": "  AeroHub Core starting...", "module": "aerohub", "filename": "aerohub.py", "line": 1240}
{"timestamp": "2026-06-12 19:03:02,691", "level": "INFO", "logger": "AeroHub", "message": "============================================================", "module": "aerohub", "filename": "aerohub.py", "line": 1241}
{"timestamp": "2026-06-12 19:03:02,692", "level": "INFO", "logger": "AeroHub", "message": "Utilities directory: C:\\Users\\NANDHA A\\Desktop\\FOLDERS\\UTILITIES", "module": "aerohub", "filename": "aerohub.py", "line": 1242}
{"timestamp": "2026-06-12 19:03:02,693", "level": "INFO", "logger": "AeroHub", "message": "Managed processes: 8", "module": "aerohub", "filename": "aerohub.py", "line": 1243}
{"timestamp": "2026-06-12 19:03:02,695", "level": "INFO", "logger": "AeroHub", "message": "Headless mode: False", "module": "aerohub", "filename": "aerohub.py", "line": 1244}
{"timestamp": "2026-06-12 19:03:02,709", "level": "INFO", "logger": "AeroHub", "message": "Cleared 1 stale tray icon registry entries.", "module": "aerohub", "filename": "aerohub.py", "line": 1186}
{"timestamp": "2026-06-12 19:03:02,750", "level": "INFO", "logger": "AeroHub", "message": "Control API listening on http://127.0.0.1:8200", "module": "aerohub", "filename": "aerohub.py", "line": 1261}
{"timestamp": "2026-06-12 19:03:02,751", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Clipboard Manager", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:02,889", "level": "INFO", "logger": "AeroHub", "message": "[clipboard_manager] Started (PID 19504)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:03,764", "level": "INFO", "logger": "AeroHub", "message": "AeroHub dashboard running.", "module": "aerohub", "filename": "aerohub.py", "line": 1323}
{"timestamp": "2026-06-12 19:03:03,891", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Health App", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:03,909", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 9152)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:04,910", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Media Control", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:04,910", "level": "INFO", "logger": "AeroHub", "message": "[media_control] Started (PID 7616)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:05,920", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Battery Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:05,927", "level": "INFO", "logger": "AeroHub", "message": "[battery_monitor] Started (PID 11596)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:06,931", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Temp Monitor", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:06,940", "level": "INFO", "logger": "AeroHub", "message": "[temp_monitor] Started (PID 17880)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:07,941", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Touch Toggle", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:07,955", "level": "INFO", "logger": "AeroHub", "message": "[touch_toggle] Started (PID 21352)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:08,956", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Telegram FDM Proxy", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:08,970", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 12428)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:09,971", "level": "INFO", "logger": "AeroHub", "message": "Auto-starting: Taskbar Scroll Controller", "module": "aerohub", "filename": "aerohub.py", "line": 796}
{"timestamp": "2026-06-12 19:03:10,006", "level": "INFO", "logger": "AeroHub", "message": "[taskbar_scroll_controller] Started (PID 9636)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:03:17,894", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 19:03:17,896", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:03:17,898", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:03:20,900", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 19:04:29,930", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 19:04:29,933", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:04:59,967", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 19:08:17,980", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Stopped (PID 9152)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 19:08:18,985", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 22884)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:13:37,288", "level": "WARNING", "logger": "AeroHub", "message": "[health_app] Exited with code 0", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 19:13:42,873", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 10436)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:14:45,253", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 19:14:45,254", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:14:45,254", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:14:48,255", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 19:16:18,319", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 19:16:18,320", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:16:27,323", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 19:16:27,324", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:16:27,325", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:16:30,327", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 19:17:48,393", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 19:17:48,394", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:17:53,935", "level": "WARNING", "logger": "AeroHub", "message": "[health_app] Exited with code 0", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 19:18:18,410", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 19:21:17,556", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 13916)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 19:21:39,492", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 19:21:39,493", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:21:39,493", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:21:42,498", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 19:21:45,499", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 19:21:45,500", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:22:15,523", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 19:23:15,542", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 19:23:15,543", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:23:15,543", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:23:18,545", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 19:36:15,906", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 19:36:15,908", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:36:24,914", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 19:36:24,915", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:36:24,915", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:36:27,917", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 19:36:36,920", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 19:36:36,920", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 19:37:06,932", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 21:26:00,001", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 21:26:00,005", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 21:26:00,006", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 21:26:03,008", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 21:43:33,553", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 21:43:33,555", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 21:44:03,573", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 22:38:15,092", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 22:38:15,101", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 22:38:15,103", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 22:38:18,105", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 22:40:04,504", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Exited with code 1", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-12 22:40:04,505", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Detected crash for running process", "module": "aerohub", "filename": "aerohub.py", "line": 809}
{"timestamp": "2026-06-12 22:40:04,505", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 22:40:09", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 22:40:07,554", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 22:40:09", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-12 22:40:10,573", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Crashed! Auto-restarting in 5s...", "module": "aerohub", "filename": "aerohub.py", "line": 822}
{"timestamp": "2026-06-12 22:40:15,647", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 23820)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 23:12:10,929", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 23:12:10,933", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:12:40,944", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 23:12:58,960", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 23:12:58,961", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:12:58,961", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:13:01,962", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 23:14:16,993", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 23:14:16,993", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:14:47,005", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 23:15:47,140", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 23:15:47,140", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:15:47,141", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:15:50,141", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 23:24:47,554", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 23:24:47,555", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:25:17,571", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 23:26:56,784", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Stopped (PID 13916)", "module": "aerohub", "filename": "aerohub.py", "line": 334}
{"timestamp": "2026-06-12 23:26:57,792", "level": "INFO", "logger": "AeroHub", "message": "[health_app] Started (PID 17172)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-12 23:45:15,547", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 23:45:15,547", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:45:15,547", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:45:18,549", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-12 23:45:30,556", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-12 23:45:30,561", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:46:00,574", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-12 23:55:51,313", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-12 23:55:51,317", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:55:51,321", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-12 23:55:54,324", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 00:09:11,520", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 00:09:11,521", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:09:41,532", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 00:10:50,560", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 00:10:50,560", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:10:50,560", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:10:53,561", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 00:39:51,741", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 00:39:51,741", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:40:21,776", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 00:43:57,884", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 00:43:57,884", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:43:57,884", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:44:00,886", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 00:48:25,083", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 00:48:25,083", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:48:52,098", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 00:48:52,099", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:48:52,099", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:48:55,100", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 00:51:34,177", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 00:51:34,178", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:52:04,191", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 00:53:01,210", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 00:53:01,210", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:53:01,212", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 00:53:04,212", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 01:08:52,896", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 01:08:52,897", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:09:01,903", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 01:09:01,904", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:09:01,905", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:09:04,906", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 01:20:56,297", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 01:20:56,298", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:21:26,309", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 01:23:17,368", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 01:23:17,368", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:23:17,369", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:23:20,370", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 01:44:39,756", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 01:44:39,758", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:45:03,793", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 01:45:03,801", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:45:03,814", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 01:45:06,817", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 11:06:14,437", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 11:06:14,447", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 11:06:44,461", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 11:07:05,468", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 11:07:05,468", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 11:07:05,471", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 11:07:08,472", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 11:07:14,475", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 11:07:14,476", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 11:07:32,482", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 11:07:32,482", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 11:07:32,483", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 11:07:35,485", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 11:37:04,712", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 11:37:04,714", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 16:58:32,375", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 16:58:32,378", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 16:58:32,379", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 16:58:35,436", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 16:58:47,508", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 16:58:47,509", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 16:59:17,522", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 16:59:32,533", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 16:59:32,535", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 16:59:32,536", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 16:59:36,790", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 17:09:43,079", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 17:09:43,080", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 17:10:07,115", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 17:10:07,116", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 17:10:07,117", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 17:10:10,118", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 17:30:44,071", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 17:30:44,073", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 17:31:14,087", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 17:34:32,174", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 17:34:32,175", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 17:34:32,175", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 17:34:35,176", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 19:00:26,023", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 19:00:26,025", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 19:00:35,029", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 19:00:35,030", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 19:00:35,033", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 19:00:38,035", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 19:00:41,903", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Exited with code 1", "module": "aerohub", "filename": "aerohub.py", "line": 361}
{"timestamp": "2026-06-13 19:00:41,907", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Detected crash for running process", "module": "aerohub", "filename": "aerohub.py", "line": 809}
{"timestamp": "2026-06-13 19:00:41,908", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 19:00:51", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-13 19:00:44,993", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 19:00:51", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-13 19:00:47,040", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 19:00:47,042", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 19:00:48,028", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 19:00:51", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-13 19:00:51,051", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Waiting for backoff until 19:00:51", "module": "aerohub", "filename": "aerohub.py", "line": 813}
{"timestamp": "2026-06-13 19:00:54,069", "level": "WARNING", "logger": "AeroHub", "message": "[tg_fdm_proxy] Crashed! Auto-restarting in 5s...", "module": "aerohub", "filename": "aerohub.py", "line": 822}
{"timestamp": "2026-06-13 19:00:59,111", "level": "INFO", "logger": "AeroHub", "message": "[tg_fdm_proxy] Started (PID 19352)", "module": "aerohub", "filename": "aerohub.py", "line": 301}
{"timestamp": "2026-06-13 19:01:11,054", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 19:01:11,054", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 19:01:11,056", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 19:01:14,058", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 19:11:56,435", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 19:11:56,437", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:42:52,103", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
{"timestamp": "2026-06-13 23:42:55,107", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 23:42:55,108", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:42:55,108", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:42:58,110", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 23:43:10,113", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 23:43:10,113", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:43:19,117", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 23:43:19,117", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:43:19,118", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:43:22,120", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-13 23:46:58,202", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-13 23:46:58,204", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:47:28,214", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game detected. Activating AeroEco...", "module": "aerohub", "filename": "aerohub.py", "line": 977}
{"timestamp": "2026-06-13 23:47:28,214", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:47:28,215", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:on' to port 5099", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-13 23:47:31,216", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] temp_monitor manually started by user. Overriding pause.", "module": "aerohub", "filename": "aerohub.py", "line": 964}
{"timestamp": "2026-06-14 00:18:50,101", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown...", "module": "aerohub", "filename": "aerohub.py", "line": 991}
{"timestamp": "2026-06-14 00:18:50,102", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Sent IPC 'game_mode:off' to port 5098", "module": "aerohub", "filename": "aerohub.py", "line": 921}
{"timestamp": "2026-06-14 00:19:20,115", "level": "INFO", "logger": "AeroHub", "message": "[GAME MODE] Cooldown expired. Resuming temp_monitor.", "module": "aerohub", "filename": "aerohub.py", "line": 1014}
```

---

### File: `aerohub.py`
- **Path:** `aerohub.py`
- **Estimated Tokens:** 12,782
- **mtime:** 1781177313.798

```python
"""
AeroHub Core — Central background orchestrator with floating dashboard widget.
Manages the lifecycle (start, stop, restart, monitor) of all child utility processes.
Tray icon + floating mini-widget showing process status in the desktop corner.
"""

import argparse
import importlib
import os
import sys
import json
import time
import subprocess
import threading
import logging
import logging.handlers
import psutil
import tkinter as tk
import queue

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICES_DIR = os.path.dirname(SCRIPT_DIR)
ROOT_DIR = os.path.dirname(SERVICES_DIR)
UTILS_DIR = ROOT_DIR
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, SERVICES_DIR)

remote_control = importlib.import_module("aerohub_core.remote_control")
LocalControlHandler = remote_control.LocalControlHandler
LocalControlServer = remote_control.LocalControlServer

try:
    from config.loader import load_config as load_runtime_config
    from config.logging import setup_logging
except ImportError:
    def load_runtime_config():
        return {}

    def setup_logging(*args, **kwargs):
        return logging.getLogger()

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None

LOG_PATH = os.path.join(UTILS_DIR, "aerohub.log")
LOGS_DIR = os.path.join(UTILS_DIR, "Logs")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "aerohub_config.json")
os.makedirs(SCRIPT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes

    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.Core")
except Exception:
    pass

# ── Logging ──
runtime_settings = load_runtime_config()
setup_logging("aerohub", config=runtime_settings)
logger = logging.getLogger("AeroHub")

# ── Theme ──
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg_card": "#1a1a3e",
    "accent": "#7c3aed",
    "accent_hover": "#9b59f5",
    "success": "#00ff88",
    "danger": "#ff3366",
    "warning": "#ffdd00",
    "fg": "#f0f0f0",
    "fg_dim": "#6a7080",
    "border": "#2d2d5e",
    "running": "#00ff88",
    "stopped": "#ff3366",
}

# ── Default Config ──
DEFAULT_CONFIG = {
    "auto_start": True,
    "restart_delay_sec": 5,
    "processes": [
        {
            "id": "clipboard_manager",
            "name": "Clipboard Manager",
            "icon": "📋",
            "script": "services/clipboard_manager/ClipboardManager/clipboard_manager.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "health_app",
            "name": "Health App",
            "icon": "👁️",
            "script": "services/health_app/health_app.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "media_control",
            "name": "Media Control",
            "icon": "🎵",
            "script": "services/media_control/media_control.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "battery_monitor",
            "name": "Battery Monitor",
            "icon": "🔋",
            "script": "toggles/battery_monitor/battery_monitor.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "temp_monitor",
            "name": "Temp Monitor",
            "icon": "🌡️",
            "script": "toggles/temp_monitor/temp_monitor.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "touch_toggle",
            "name": "Touch Toggle",
            "icon": "👆",
            "script": "toggles/touch_toggle/touch_toggle.py",
            "auto_start": False,
            "enabled": True,
        },
        {
            "id": "tg_fdm_proxy",
            "name": "Telegram FDM Proxy",
            "icon": "📡",
            "script": "services/tg_fdm_proxy/TgFdmProxy/tg_fdm_proxy.py",
            "auto_start": False,
            "enabled": True,
        },
        {
            "id": "taskbar_scroll_controller",
            "name": "Taskbar Scroll Controller",
            "icon": "🔊",
            "script": "tools/taskbar_scroll/taskbar_scroll.py",
            "auto_start": True,
            "enabled": True,
        },
    ],
}


# ══════════════════════════════════════════════════════════
#  Config Management
# ══════════════════════════════════════════════════════════
def load_config() -> dict:
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Config load error: {e}")
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        logger.error(f"Config save error: {e}")


# ══════════════════════════════════════════════════════════
#  Process Manager
# ══════════════════════════════════════════════════════════
class ProcessEntry:
    """Represents a managed child process."""

    def __init__(self, config: dict, utils_dir: str):
        self.id = config["id"]
        self.name = config["name"]
        self.icon = config.get("icon", "⚙️")
        self.script = config["script"]
        self.auto_start = config.get("auto_start", False)
        self.enabled = config.get("enabled", True)
        self.restart_delay = config.get("restart_delay_sec", 5)
        self.max_restarts = config.get("max_restarts", 3)
        self.restart_backoff = config.get("restart_backoff", 2)
        self.utils_dir = utils_dir

        self.process: subprocess.Popen = None
        self.pid = None
        self.status = "stopped"  # running, stopped, crashed, starting
        self.start_time = None
        self.restart_count = 0
        self.last_crash = None
        self.consecutive_crashes = 0
        self.next_restart_time = 0.0

    @property
    def full_path(self) -> str:
        return os.path.join(self.utils_dir, self.script)

    @property
    def uptime_str(self) -> str:
        if not self.start_time:
            return "—"
        elapsed = time.time() - self.start_time
        if elapsed < 60:
            return "<1m"
        h, m = divmod(int(elapsed), 3600)
        m, _ = divmod(m, 60)
        if h > 0:
            return f"{h}h {m}m"
        return f"{m}m"

    def start(self):
        """Start the process."""
        if self.status == "running" and self.process and self.process.poll() is None:
            logger.info(f"[{self.id}] Already running (PID {self.pid})")
            return

        now = time.time()
        if self.status == "crashed" and now < self.next_restart_time:
            logger.warning(
                f"[{self.id}] Restart backoff active until "
                f"{time.strftime('%H:%M:%S', time.localtime(self.next_restart_time))}"
            )
            return

        if self.last_crash and now - self.last_crash > 300:
            self.consecutive_crashes = 0

        script_path = self.full_path
        if not os.path.exists(script_path):
            logger.error(f"[{self.id}] Script not found: {script_path}")
            self.status = "stopped"
            return

        try:
            self.status = "starting"
            cwd = os.path.dirname(script_path)

            if script_path.lower().endswith(".exe"):
                self.process = subprocess.Popen(
                    [script_path],
                    cwd=cwd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                    if sys.platform == "win32"
                    else 0,
                )
            else:
                # Use a per-utility hardlink of pythonw.exe so Windows shows
                # each tray icon separately (identified by unique exe path)
                python_exe = sys.executable
                python_dir = os.path.dirname(python_exe)
                pythonw = os.path.join(python_dir, "pythonw.exe")

                # Create a uniquely-named hardlink for this utility
                unique_exe_name = f"pythonw_{self.id}.exe"
                unique_exe = os.path.join(python_dir, unique_exe_name)

                if not os.path.exists(unique_exe):
                    try:
                        os.link(pythonw, unique_exe)  # NTFS hardlink, zero extra space
                        logger.info(f"[{self.id}] Created hardlink: {unique_exe}")
                    except OSError:
                        try:
                            import shutil

                            shutil.copy2(pythonw, unique_exe)
                            logger.info(f"[{self.id}] Copied exe: {unique_exe}")
                        except Exception as e:
                            logger.warning(
                                f"[{self.id}] Could not create unique exe, using shared pythonw: {e}"
                            )
                            unique_exe = pythonw

                exe = unique_exe if os.path.exists(unique_exe) else pythonw

                self.process = subprocess.Popen(
                    [exe, script_path],
                    cwd=cwd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                    if sys.platform == "win32"
                    else 0,
                )
            self.pid = self.process.pid
            self.start_time = time.time()
            self.status = "running"
            logger.info(f"[{self.id}] Started (PID {self.pid})")

        except Exception as e:
            logger.error(f"[{self.id}] Start failed: {e}")
            self.status = "crashed"
            self.last_crash = time.time()

    def stop(self):
        """Stop the process gracefully."""
        if self.process:
            try:
                # Try to terminate the entire process tree
                parent = psutil.Process(self.pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.terminate()
                    except psutil.NoSuchProcess:
                        pass
                parent.terminate()

                # Wait up to 5 seconds
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill
                    parent.kill()
                    for child in children:
                        try:
                            child.kill()
                        except psutil.NoSuchProcess:
                            pass

                logger.info(f"[{self.id}] Stopped (PID {self.pid})")
            except (psutil.NoSuchProcess, ProcessLookupError):
                pass
            except Exception as e:
                logger.error(f"[{self.id}] Stop error: {e}")

        self.process = None
        self.pid = None
        self.status = "stopped"
        self.start_time = None

    def restart(self):
        """Restart the process."""
        self.stop()
        time.sleep(1)
        self.start()
        self.restart_count += 1

    def check_health(self) -> bool:
        """Check if the process is still alive."""
        if not self.process or self.status != "running":
            return False

        poll = self.process.poll()
        if poll is not None:
            # Process has exited
            exit_code = poll
            logger.warning(f"[{self.id}] Exited with code {exit_code}")
            if exit_code == 0:
                self.status = "stopped"
            else:
                self.status = "crashed"
                self.last_crash = time.time()
                self.consecutive_crashes += 1
                backoff = self.restart_delay * (
                    self.restart_backoff ** max(0, self.consecutive_crashes - 1)
                )
                self.next_restart_time = time.time() + min(backoff, 300)
                if self.consecutive_crashes >= self.max_restarts:
                    self.status = "circuit_breaker"
                    logger.error(
                        f"[{self.id}] Circuit breaker triggered after {self.consecutive_crashes} failures"
                    )
            self.process = None
            self.pid = None
            return False

        # Double-check with psutil
        try:
            proc = psutil.Process(self.pid)
            if not proc.is_running():
                self.status = "crashed"
                self.last_crash = time.time()
                return False
        except psutil.NoSuchProcess:
            self.status = "crashed"
            self.last_crash = time.time()
            return False

        return True


# ══════════════════════════════════════════════════════════
#  Floating Dashboard Widget
# ══════════════════════════════════════════════════════════
class DashboardWidget:
    """Floating mini-widget on the desktop corner showing process status."""

    def __init__(
        self,
        processes: list,
        on_toggle,
        on_restart,
        on_start_all=None,
        on_stop_all=None,
        on_exit=None,
    ):
        self.processes = processes
        self.on_toggle = on_toggle
        self.on_restart = on_restart
        self.on_start_all = on_start_all
        self.on_stop_all = on_stop_all
        self.on_exit = on_exit
        self.queue = queue.Queue()
        self.root = None
        self._visible = False
        self._drag_data = {"x": 0, "y": 0}
        self._status_labels = {}
        self._uptime_labels = {}
        self._btn_labels = {}

    def create(self):
        """Create the floating dashboard."""
        self.root = tk.Tk()
        self.root.title("AeroHub")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.0)
        self.root.configure(bg=TH["bg"])

        n = len(self.processes)
        widget_w = 380
        widget_h = 50 + n * 38 + 10
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - widget_w - 16
        y = screen_h - widget_h - 60

        self.root.geometry(f"{widget_w}x{widget_h}+{x}+{y}")

        # ── Title bar ──
        title_bar = tk.Frame(self.root, bg=TH["bg2"], height=36)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="🚀 AeroHub",
            font=("Segoe UI", 11, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(side=tk.LEFT, padx=(12, 6))

        # Hover effect helper for title buttons
        def add_hover(widget, hover_fg):
            default_fg = widget.cget("fg")
            widget.bind(
                "<Enter>", lambda e: widget.config(bg=TH["bg_card"], fg=hover_fg)
            )
            widget.bind("<Leave>", lambda e: widget.config(bg=TH["bg2"], fg=default_fg))

        if self.on_start_all:
            btn = tk.Button(
                title_bar,
                text="▶",
                font=("Segoe UI", 10),
                bg=TH["bg2"],
                fg=TH["running"],
                activebackground=TH["bg_card"],
                activeforeground=TH["running"],
                relief=tk.FLAT,
                cursor="hand2",
                command=self.on_start_all,
            )
            btn.pack(side=tk.LEFT, padx=2)
            add_hover(btn, hover_fg=TH["running"])

        if self.on_stop_all:
            btn = tk.Button(
                title_bar,
                text="■",
                font=("Segoe UI", 10),
                bg=TH["bg2"],
                fg=TH["danger"],
                activebackground=TH["bg_card"],
                activeforeground=TH["danger"],
                relief=tk.FLAT,
                cursor="hand2",
                command=self.on_stop_all,
            )
            btn.pack(side=tk.LEFT, padx=2)
            add_hover(btn, hover_fg=TH["danger"])

        if self.on_exit:
            btn = tk.Button(
                title_bar,
                text="⏻",
                font=("Segoe UI", 10),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg_card"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                command=self.on_exit,
            )
            btn.pack(side=tk.LEFT, padx=2)
            add_hover(btn, hover_fg=TH["accent"])

        # Running count
        self._running_count_var = tk.StringVar(value="")
        tk.Label(
            title_bar,
            textvariable=self._running_count_var,
            font=("Segoe UI", 9),
            bg=TH["bg2"],
            fg=TH["fg_dim"],
        ).pack(side=tk.RIGHT, padx=12)

        # Drag support on title bar
        title_bar.bind("<Button-1>", self._start_drag)
        title_bar.bind("<B1-Motion>", self._do_drag)

        # ── Process rows ──
        container = tk.Frame(self.root, bg=TH["bg"], padx=8, pady=4)
        container.pack(fill=tk.BOTH, expand=True)

        for i, proc in enumerate(self.processes):
            row = tk.Frame(container, bg=TH["bg_card"], pady=3, padx=6)
            row.pack(fill=tk.X, pady=2)

            # Icon + Name
            tk.Label(
                row,
                text=proc.icon,
                font=("Segoe UI Emoji", 12),
                bg=TH["bg_card"],
                fg=TH["fg"],
            ).pack(side=tk.LEFT, padx=(2, 4))

            tk.Label(
                row,
                text=proc.name,
                font=("Segoe UI", 9),
                bg=TH["bg_card"],
                fg=TH["fg"],
                width=24,
                anchor=tk.W,
            ).pack(side=tk.LEFT)

            # Status dot
            status_label = tk.Label(
                row, text="●", font=("Segoe UI", 10), bg=TH["bg_card"], fg=TH["stopped"]
            )
            status_label.pack(side=tk.LEFT, padx=4)
            self._status_labels[proc.id] = status_label

            # Uptime
            uptime_label = tk.Label(
                row,
                text="—",
                font=("Consolas", 8),
                bg=TH["bg_card"],
                fg=TH["fg_dim"],
                width=7,
            )
            uptime_label.pack(side=tk.LEFT, padx=2)
            self._uptime_labels[proc.id] = uptime_label

            # Toggle button
            btn = tk.Button(
                row,
                text="▶",
                font=("Segoe UI", 8),
                bg=TH["accent"],
                fg="white",
                relief=tk.FLAT,
                width=3,
                cursor="hand2",
                command=lambda p=proc: self._toggle(p),
            )
            btn.pack(side=tk.RIGHT, padx=2)
            self._btn_labels[proc.id] = btn

            # Restart button
            restart_btn = tk.Button(
                row,
                text="↻",
                font=("Segoe UI", 9),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                relief=tk.FLAT,
                width=2,
                cursor="hand2",
                command=lambda p=proc: self._restart(p),
            )
            restart_btn.pack(side=tk.RIGHT, padx=1)

        # Apply DWM native rounded corners (DWMWA_WINDOW_CORNER_PREFERENCE = 33, DWMWCP_ROUND = 2)
        self.root.update_idletasks()
        try:
            import ctypes

            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if hwnd == 0:
                hwnd = self.root.winfo_id()
            dwmapi = ctypes.windll.dwmapi
            corner_pref = ctypes.c_int(2)
            dwmapi.DwmSetWindowAttribute(
                ctypes.c_void_p(hwnd),
                33,
                ctypes.byref(corner_pref),
                ctypes.sizeof(corner_pref),
            )
        except Exception as e:
            logger.error(f"DWM rounding error: {e}")

        self.root.after(100, self._poll_queue)
        self.root.withdraw()
        self._visible = False

    def _toggle(self, proc):
        threading.Thread(target=self.on_toggle, args=(proc,), daemon=True).start()

    def _restart(self, proc):
        threading.Thread(target=self.on_restart, args=(proc,), daemon=True).start()

    def _start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_data["x"])
        y = self.root.winfo_y() + (event.y - self._drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def update_status(self):
        """Update all process status displays."""
        running = 0
        for proc in self.processes:
            sid = proc.id

            if sid in self._status_labels:
                if proc.status == "running":
                    self._status_labels[sid].config(fg=TH["running"])
                    self._btn_labels[sid].config(text="■", bg=TH["danger"])
                    running += 1
                elif proc.status == "crashed":
                    self._status_labels[sid].config(fg=TH["warning"])
                    self._btn_labels[sid].config(text="▶", bg=TH["accent"])
                else:
                    self._status_labels[sid].config(fg=TH["stopped"])
                    self._btn_labels[sid].config(text="▶", bg=TH["accent"])

            if sid in self._uptime_labels:
                self._uptime_labels[sid].config(text=proc.uptime_str)

        self._running_count_var.set(f"{running}/{len(self.processes)}")

    def _periodic_update(self):
        """Update status every 2 seconds."""
        if self._visible and self.root:
            self.update_status()
            self.root.after(2000, self._periodic_update)

    def _fade_in(self, step=0):
        total = 15
        if step <= total:
            alpha = min(0.92, step / total * 0.92)
            try:
                self.root.attributes("-alpha", alpha)
                self.root.after(20, lambda: self._fade_in(step + 1))
            except tk.TclError:
                pass

    def show(self):
        if self.root:
            self.root.deiconify()
            self.root.focus_force()
            self._visible = True
            self._fade_in()
            self._periodic_update()

            # Bind FocusOut to automatically hide when clicking elsewhere
            def on_focus_out(event):
                if event.widget == self.root:

                    def check_focus():
                        if self.root.focus_displayof() is None:
                            self.hide_safe()

                    self.root.after(100, check_focus)

            self.root.bind("<FocusOut>", on_focus_out)

    def hide(self):
        if self.root:
            self.root.withdraw()
            self._visible = False

    def show_safe(self):
        if self.root:
            self.queue.put((self.show, ()))

    def hide_safe(self):
        if self.root:
            self.queue.put((self.hide, ()))

    def _poll_queue(self):
        if not self.root:
            return
        try:
            while not self.queue.empty():
                callback, args = self.queue.get_nowait()
                callback(*args)
        except Exception as e:
            logger.error(f"Error in queue poll: {e}")
        try:
            self.root.after(100, self._poll_queue)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
def create_aerohub_icon(running_count: int, total: int) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    if running_count == total:
        bg_color = (0, 255, 136, 220)  # all running - green
    elif running_count > 0:
        bg_color = (124, 58, 237, 220)  # some running - purple
    else:
        bg_color = (100, 100, 100, 220)  # none running - gray

    draw.rounded_rectangle([2, 2, 62, 62], radius=10, fill=bg_color)

    # Rocket icon (simple triangle)
    draw.polygon([(32, 8), (20, 48), (44, 48)], fill=(255, 255, 255, 220))
    # Exhaust
    draw.polygon([(26, 48), (32, 58), (38, 48)], fill=(255, 200, 50, 200))

    return img


# ══════════════════════════════════════════════════════════
#  AeroHub Core
# ══════════════════════════════════════════════════════════
class AeroHubCore:
    def __init__(self, headless: bool = False):
        self.config = load_config()
        self.runtime_settings = load_runtime_config()
        self.processes: list[ProcessEntry] = []
        self.tray_icon = None
        self.widget = None
        self._running = True
        self.headless = headless
        self.control_port = int(
            self.runtime_settings.get("app", {}).get("control_port", 8200)
        )
        self.control_token = (
            self.runtime_settings.get("app", {}).get("control_token")
            or os.environ.get("AEROHUB_CONTROL_TOKEN")
        )
        self.control_server = None

        # Initialize process entries
        for proc_config in self.config.get("processes", DEFAULT_CONFIG["processes"]):
            entry = ProcessEntry(proc_config, UTILS_DIR)
            self.processes.append(entry)

    def _on_toggle(self, proc: ProcessEntry):
        """Toggle a process on/off."""
        if proc.status == "running":
            proc.stop()
        else:
            proc.start()
        self._update_tray_icon()

    def _on_restart(self, proc: ProcessEntry):
        """Restart a process."""
        proc.restart()
        self._update_tray_icon()

    def _auto_start_all(self):
        """Start all processes that have auto_start enabled."""
        for proc in self.processes:
            if proc.auto_start and proc.enabled:
                logger.info(f"Auto-starting: {proc.name}")
                proc.start()
                time.sleep(1)  # Stagger starts

    def _health_monitor(self):
        """Background thread: monitor all processes and auto-restart crashed ones."""
        restart_delay = self.config.get("restart_delay_sec", 5)

        while self._running:
            for proc in self.processes:
                if proc.status == "running":
                    alive = proc.check_health()
                    if not alive and proc.status == "crashed":
                        logger.warning(f"[{proc.id}] Detected crash for running process")
                if proc.status == "crashed" and proc.enabled and proc.auto_start:
                    now = time.time()
                    if now < proc.next_restart_time:
                        logger.warning(
                            f"[{proc.id}] Waiting for backoff until "
                            f"{time.strftime('%H:%M:%S', time.localtime(proc.next_restart_time))}"
                        )
                    elif proc.consecutive_crashes >= proc.max_restarts:
                        logger.error(
                            f"[{proc.id}] Restart disabled by circuit breaker"
                        )
                    else:
                        logger.warning(
                            f"[{proc.id}] Crashed! Auto-restarting in {restart_delay}s..."
                        )
                        time.sleep(restart_delay)
                        if self._running:
                            proc.start()
                            proc.restart_count += 1

            self._update_tray_icon()
            time.sleep(3)

    def _is_system_in_game_mode(self) -> bool:
        """Checks if the system is running a fullscreen DirectX/OpenGL game or fullscreen app."""
        import ctypes.wintypes

        try:
            # 1. SHQueryUserNotificationState check
            state = ctypes.c_int()
            res = ctypes.windll.shell32.SHQueryUserNotificationState(
                ctypes.byref(state)
            )
            if res == 0:
                # 1: QUNS_BUSY covers fullscreen/presenting.
                # 2: QUNS_RUNNING_D3D_FULL_SCREEN covers exclusive fullscreen games.
                if state.value in (1, 2):
                    return True
        except Exception:
            pass

        # 2. Fallback to Active Bounding Window Check
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return False

            # Ignore common desktop and shell windows
            class_name = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_name, 256)
            cname = class_name.value
            if cname in ("Progman", "WorkerW", "Shell_TrayWnd", "Button"):
                return False

            # Get window rect
            rect = ctypes.wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            width = rect.right - rect.left
            height = rect.bottom - rect.top

            # Get active monitor info
            monitor = ctypes.windll.user32.MonitorFromWindow(
                hwnd, 1
            )  # MONITOR_DEFAULTTOPRIMARY = 1

            # MONITORINFO structure size is 40 bytes
            class MONITORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_ulong),
                    ("rcMonitor", ctypes.wintypes.RECT),
                    ("rcWork", ctypes.wintypes.RECT),
                    ("dwFlags", ctypes.c_ulong),
                ]

            info = MONITORINFO()
            info.cbSize = ctypes.sizeof(MONITORINFO)
            if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
                m_width = info.rcMonitor.right - info.rcMonitor.left
                m_height = info.rcMonitor.bottom - info.rcMonitor.top
                # Check if dimensions match active monitor dimensions
                if width >= m_width and height >= m_height:
                    # Check window styles: WS_POPUP (0x80000000) or lack of WS_CAPTION (0x00C00000)
                    style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
                    if (style & 0x80000000) or not (style & 0x00C00000):
                        return True
        except Exception:
            pass
        return False

    def _set_service_priority(self, service_id: str, priority_class: int):
        """Set process priority of a managed service."""
        for proc in self.processes:
            if proc.id == service_id:
                if proc.status == "running" and proc.pid:
                    try:
                        p = psutil.Process(proc.pid)
                        p.nice(priority_class)
                    except Exception as e:
                        logger.warning(
                            f"[GAME MODE] Failed to set priority of {service_id}: {e}"
                        )

    def _send_udp_ipc_message(self, port: int, message: str):
        """Send a UDP packet to local port."""
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.encode("utf-8"), ("127.0.0.1", port))
            sock.close()
            logger.info(f"[GAME MODE] Sent IPC '{message}' to port {port}")
        except Exception as e:
            logger.error(f"[GAME MODE] IPC send failed: {e}")

    def _control_service(self, service_id: str, action: str):
        """Start or stop a service by its ID."""
        for proc in self.processes:
            if proc.id == service_id:
                if action == "stop":
                    if proc.status == "running":
                        logger.info(f"[GAME MODE] Stopping service: {service_id}")
                        proc.stop()
                elif action == "start":
                    if proc.enabled and proc.status != "running":
                        logger.info(f"[GAME MODE] Starting service: {service_id}")
                        proc.start()

    def _game_mode_monitor(self):
        """Periodically polls to check if game/fullscreen mode is active and manages utilities."""
        game_mode_active = False
        cooldown_end_time = 0
        temp_monitor_paused = False
        consecutive_gaming = 0
        consecutive_nongaming = 0

        while self._running:
            try:
                is_gaming = self._is_system_in_game_mode()
            except Exception as e:
                logger.error(f"Error checking game mode: {e}")
                is_gaming = False

            if is_gaming:
                consecutive_gaming += 1
                consecutive_nongaming = 0
            else:
                consecutive_gaming = 0
                consecutive_nongaming += 1

            # If we paused it, check if user manually started it
            if temp_monitor_paused:
                for proc in self.processes:
                    if proc.id == "temp_monitor" and proc.status == "running":
                        logger.info(
                            "[GAME MODE] temp_monitor manually started by user. Overriding pause."
                        )
                        temp_monitor_paused = False

            # --- STATE TRANSITIONS ---
            if not game_mode_active and consecutive_gaming >= 2:
                # Entering game mode (detected for 2 consecutive polls, ~6s)
                cooldown_end_time = 0  # reset cooldown

                # Force IDLE priority
                self._set_service_priority("health_app", psutil.IDLE_PRIORITY_CLASS)

                logger.info(
                    "[GAME MODE] Fullscreen/Game detected. Activating AeroEco..."
                )
                game_mode_active = True

                # Send UDP IPC packet game_mode:on to health_app
                self._send_udp_ipc_message(5098, "game_mode:on")

                # Send UDP IPC packet game_mode:on to temp_monitor to pause it
                self._send_udp_ipc_message(5099, "game_mode:on")
                temp_monitor_paused = True

            elif game_mode_active and consecutive_nongaming >= 2:
                # Exiting game mode (not detected for 2 consecutive polls, ~6s)
                logger.info(
                    "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown..."
                )
                game_mode_active = False
                consecutive_gaming = 0

                # Restore health_app priority to NORMAL immediately
                self._set_service_priority("health_app", psutil.NORMAL_PRIORITY_CLASS)

                # Send UDP IPC packet game_mode:off to health_app immediately
                self._send_udp_ipc_message(5098, "game_mode:off")

                # Initialize cooldown period for temp_monitor
                cooldown_end_time = time.time() + 30.0

            elif game_mode_active and is_gaming:
                # Sustaining game mode, keep priority low
                self._set_service_priority("health_app", psutil.IDLE_PRIORITY_CLASS)

            # Check if cooldown has expired
            if cooldown_end_time > 0:
                remaining = cooldown_end_time - time.time()
                if remaining <= 0:
                    logger.info("[GAME MODE] Cooldown expired. Resuming temp_monitor.")
                    cooldown_end_time = 0

                    if temp_monitor_paused:
                        # Send UDP IPC packet game_mode:off to temp_monitor to resume it
                        self._send_udp_ipc_message(5099, "game_mode:off")
                        temp_monitor_paused = False

            time.sleep(3.0)

    def _update_tray_icon(self):
        """Update tray icon based on running process count."""
        running = sum(1 for p in self.processes if p.status == "running")
        if self.tray_icon:
            try:
                self.tray_icon.icon = create_aerohub_icon(running, len(self.processes))
                self.tray_icon.title = (
                    f"AeroHub — {running}/{len(self.processes)} running"
                )
            except Exception:
                pass

    def get_health(self) -> dict:
        return {
            "status": "running" if self._running else "stopped",
            "processes": len(self.processes),
            "running": sum(1 for p in self.processes if p.status == "running"),
        }

    def get_status(self) -> dict:
        return {
            "processes": [
                {
                    "id": proc.id,
                    "name": proc.name,
                    "status": proc.status,
                    "pid": proc.pid,
                    "uptime": proc.uptime_str,
                    "restart_count": proc.restart_count,
                }
                for proc in self.processes
            ]
        }

    def get_metrics(self) -> dict:
        metrics = {
            "process_running_total": sum(1 for p in self.processes if p.status == "running"),
            "process_crashed_total": sum(1 for p in self.processes if p.status == "crashed"),
            "process_circuit_breakers": sum(
                1 for p in self.processes if p.status == "circuit_breaker"
            ),
        }
        return metrics

    def perform_self_update(self) -> dict:
        if self_update():
            return {"status": "updated", "message": "Self-update succeeded."}
        return {"status": "failed", "message": "Self-update failed. See logs."}

    def control_service(self, service_id: str, action: str) -> dict:
        proc = next((p for p in self.processes if p.id == service_id), None)
        if not proc:
            return {"error": "service not found", "service": service_id}
        if action == "start":
            proc.start()
            return {"status": "started", "service": service_id}
        if action == "stop":
            proc.stop()
            return {"status": "stopped", "service": service_id}
        if action == "restart":
            proc.restart()
            return {"status": "restarted", "service": service_id}
        return {"error": "invalid action", "action": action}

    def _cli_status_reporter(self):
        def runner():
            while self._running:
                statuses = [
                    f"{proc.id}: {proc.status} (pid={proc.pid or 'n/a'})"
                    for proc in self.processes
                ]
                logger.info("[AeroHub] %s", " | ".join(statuses))
                time.sleep(5)

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()

    def _start_all(self, icon=None, item=None):
        """Start all enabled processes."""

        def _start():
            for proc in self.processes:
                if proc.enabled and proc.status != "running":
                    proc.start()
                    time.sleep(0.5)
            self._update_tray_icon()

        threading.Thread(target=_start, daemon=True).start()

    def _stop_all(self, icon=None, item=None):
        """Stop all processes."""

        def _stop():
            for proc in self.processes:
                if proc.status == "running":
                    proc.stop()
            self._update_tray_icon()

        threading.Thread(target=_stop, daemon=True).start()

    def _on_show_widget(self, icon=None, item=None):
        """Show/hide the floating dashboard."""
        if self.widget:
            if self.widget._visible:
                self.widget.hide_safe()
            else:
                self.widget.show_safe()

    def _on_quit(self, icon, item):
        """Quit AeroHub and stop all child processes."""
        logger.info("AeroHub shutting down — stopping all processes...")
        self._running = False

        for proc in self.processes:
            if proc.status == "running":
                proc.stop()

        icon.stop()

        # Save config
        save_config(self.config)

        sys.exit(0)

    def _promote_tray_icons(self):
        """Clear stale Python tray icon entries and promote current ones to always-visible."""
        try:
            import winreg

            base_key = r"Control Panel\NotifyIconSettings"

            # Phase 1: Delete all old Python/UTILITIES entries for a clean slate
            to_delete = []
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key) as root:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(root, i)
                        i += 1
                        try:
                            with winreg.OpenKey(
                                root, subkey_name, 0, winreg.KEY_READ
                            ) as sk:
                                exe_path, _ = winreg.QueryValueEx(sk, "ExecutablePath")
                                if exe_path and (
                                    "python" in exe_path.lower()
                                    or "utilities" in exe_path.lower()
                                ):
                                    to_delete.append(subkey_name)
                        except (FileNotFoundError, OSError):
                            pass
                    except OSError:
                        break

            if to_delete:
                for subkey_name in to_delete:
                    try:
                        winreg.DeleteKey(
                            winreg.HKEY_CURRENT_USER, f"{base_key}\\{subkey_name}"
                        )
                    except OSError:
                        pass
                logger.info(
                    f"Cleared {len(to_delete)} stale tray icon registry entries."
                )

            # Phase 2: After child processes create new icons, promote them
            # (runs on a delayed thread so icons have time to register)
            def _delayed_promote():
                import time as _t

                _t.sleep(8)  # Wait for child processes to create their tray icons
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key) as root:
                        i = 0
                        promoted = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(root, i)
                                i += 1
                                with winreg.OpenKey(
                                    root,
                                    subkey_name,
                                    0,
                                    winreg.KEY_READ | winreg.KEY_WRITE,
                                ) as sk:
                                    try:
                                        exe_path, _ = winreg.QueryValueEx(
                                            sk, "ExecutablePath"
                                        )
                                        if exe_path and (
                                            "python" in exe_path.lower()
                                            or "utilities" in exe_path.lower()
                                        ):
                                            winreg.SetValueEx(
                                                sk, "IsPromoted", 0, winreg.REG_DWORD, 1
                                            )
                                            promoted += 1
                                    except (FileNotFoundError, OSError):
                                        pass
                            except OSError:
                                break
                    if promoted > 0:
                        logger.info(
                            f"Promoted {promoted} tray icon(s) to always-visible."
                        )
                except Exception as e:
                    logger.warning(f"Delayed tray promotion failed: {e}")

            threading.Thread(target=_delayed_promote, daemon=True).start()

        except Exception as e:
            logger.warning(f"Tray icon cleanup failed (non-critical): {e}")

    def run(self):
        logger.info("=" * 60)
        logger.info("  AeroHub Core starting...")
        logger.info("=" * 60)
        logger.info(f"Utilities directory: {UTILS_DIR}")
        logger.info(f"Managed processes: {len(self.processes)}")
        logger.info(f"Headless mode: {self.headless}")

        # Clear stale tray icons and schedule promotion of new ones
        self._promote_tray_icons()

        # Save default config if not exists
        if not os.path.exists(CONFIG_PATH):
            save_config(self.config)

        # Start local control API
        try:
            server_address = ("127.0.0.1", self.control_port)
            self.control_server = LocalControlServer(
                server_address, LocalControlHandler, self, self.control_token
            )
            control_thread = threading.Thread(target=self.control_server.serve_forever, daemon=True)
            control_thread.start()
            logger.info(f"Control API listening on http://127.0.0.1:{self.control_port}")
        except Exception as exc:
            logger.warning(f"Could not start control API: {exc}")

        # Auto-start processes
        if self.config.get("auto_start", True):
            auto_thread = threading.Thread(target=self._auto_start_all, daemon=True)
            auto_thread.start()

        # Start health monitor
        health_thread = threading.Thread(target=self._health_monitor, daemon=True)
        health_thread.start()

        # Start Game Mode monitor
        game_mode_thread = threading.Thread(target=self._game_mode_monitor, daemon=True)
        game_mode_thread.start()

        if self.headless or pystray is None:
            logger.info("Running without tray icon; CLI status reporter enabled.")
            self._cli_status_reporter()
            try:
                while self._running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self._on_quit(None, None)
            return

        # Create tray icon
        running = 0
        icon_image = create_aerohub_icon(running, len(self.processes))

        self.tray_icon = pystray.Icon(
            name="AeroHub",
            icon=icon_image,
            title=f"AeroHub — {running}/{len(self.processes)} running",
            menu=pystray.Menu(
                pystray.MenuItem(
                    "🚀 Show Dashboard", self._on_show_widget, default=True
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("▶ Start All", self._start_all),
                pystray.MenuItem("■ Stop All", self._stop_all),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit AeroHub", self._on_quit),
            ),
        )

        # Run tray in background thread
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

        # Create and run floating dashboard widget (tkinter main loop on main thread)
        self.widget = DashboardWidget(
            self.processes,
            self._on_toggle,
            self._on_restart,
            on_start_all=self._start_all,
            on_stop_all=self._stop_all,
            on_exit=lambda: self._on_quit(self.tray_icon, None),
        )
        self.widget.create()

        logger.info("AeroHub dashboard running.")
        self.widget.root.mainloop()


def check_admin_and_elevate(no_uac: bool = False, headless: bool = False):
    import ctypes

    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if is_admin:
        logger.info("✓ Running with Administrator privileges.")
        return

    if no_uac or headless:
        logger.warning(
            "Skipping UAC elevation because --no-uac or headless mode was requested."
        )
        return

    logger.info("Requesting elevation via UAC in non-blocking mode...")
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            f'"{script}" {params}',
            os.path.dirname(script),
            1,
        )
        if int(ret) > 32:
            logger.info("Elevation requested; exiting parent process.")
            sys.exit(0)
        logger.error(f"UAC elevation failed with return value: {ret}")
    except Exception as e:
        logger.error(f"Failed to elevate: {e}")


def self_update():
    if not os.path.isdir(os.path.join(ROOT_DIR, ".git")):
        logger.error("No git repository found. Self-update requires git.")
        return False
    try:
        old_rev = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT_DIR
        ).decode("utf-8").strip()
        subprocess.run(["git", "fetch", "--all"], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "pull", "--ff-only"], cwd=ROOT_DIR, check=True)
        logger.info("Self-update pulled the latest revision.")
        return True
    except Exception as exc:
        logger.error(f"Self-update failed: {exc}")
        try:
            subprocess.run(["git", "reset", "--hard", old_rev], cwd=ROOT_DIR, check=True)
            logger.info("Rolled back to previous revision.")
        except Exception as rollback_exc:
            logger.error(f"Rollback failed: {rollback_exc}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AeroHub Core Launcher")
    parser.add_argument("--service", action="store_true", help="Run in service/headless mode")
    parser.add_argument("--headless", action="store_true", help="Run without GUI/tray")
    parser.add_argument("--no-uac", action="store_true", help="Do not request UAC elevation")
    parser.add_argument("--self-update", action="store_true", help="Update from git and restart")
    args = parser.parse_args()

    try:
        if args.self_update:
            success = self_update()
            if success:
                logger.info("Restarting AeroHub Core after self-update...")
                new_args = [arg for arg in sys.argv[1:] if arg != "--self-update"]
                os.execv(sys.executable, [sys.executable, sys.argv[0]] + new_args)
            sys.exit(0 if success else 1)

        check_admin_and_elevate(args.no_uac, args.headless or args.service)
        app = AeroHubCore(headless=(args.headless or args.service))
        app.run()
    except Exception:
        import traceback

        with open(
            os.path.join(LOGS_DIR, "aerohub_crash.log"), "w", encoding="utf-8"
        ) as f:
            f.write(f"Crash at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            traceback.print_exc(file=f)
        try:
            logger.exception("AeroHub crashed on startup:")
        except Exception:
            pass
        sys.exit(1)
```

---

### File: `aerohub_config.json`
- **Path:** `aerohub_config.json`
- **Estimated Tokens:** 454
- **mtime:** 1781271176.834

```json
{
  "auto_start": true,
  "restart_delay_sec": 5,
  "processes": [
    {
      "id": "clipboard_manager",
      "name": "Clipboard Manager",
      "icon": "\ud83d\udccb",
      "script": "services/clipboard_manager/ClipboardManager/clipboard_manager.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "health_app",
      "name": "Health App",
      "icon": "\ud83d\udc41\ufe0f",
      "script": "services/health_app/health_app.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "media_control",
      "name": "Media Control",
      "icon": "\ud83c\udfb5",
      "script": "services/media_control/media_control.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "battery_monitor",
      "name": "Battery Monitor",
      "icon": "\ud83d\udd0b",
      "script": "toggles/battery_monitor/battery_monitor.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "temp_monitor",
      "name": "Temp Monitor",
      "icon": "\ud83c\udf21\ufe0f",
      "script": "toggles/temp_monitor/temp_monitor.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "touch_toggle",
      "name": "Touch Toggle",
      "icon": "\ud83d\udc46",
      "script": "toggles/touch_toggle/touch_toggle.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "tg_fdm_proxy",
      "name": "Telegram FDM Proxy",
      "icon": "\ud83d\udce1",
      "script": "services/tg_fdm_proxy/TgFdmProxy/tg_fdm_proxy.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "taskbar_scroll_controller",
      "name": "Taskbar Scroll Controller",
      "icon": "\ud83d\udd0a",
      "script": "tools/taskbar_scroll/taskbar_scroll.py",
      "auto_start": true,
      "enabled": true
    }
  ]
}
```

---

### File: `remote_control.py`
- **Path:** `remote_control.py`
- **Estimated Tokens:** 659
- **mtime:** 1780923522.094

```python
import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger("AeroHub.RemoteControl")


class LocalControlHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _unauthorized(self):
        self._send_json({"error": "Unauthorized"}, status=401)

    def _parse_request(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def _allowed(self):
        token = self.server.control_token
        if not token:
            return True
        header = self.headers.get("X-Local-Token") or self.headers.get("Authorization")
        if header and header.strip() == token:
            return True
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if params.get("token", [""])[0] == token:
            return True
        return False

    def do_GET(self):
        if not self._allowed():
            return self._unauthorized()

        path, params = self._parse_request()
        core = self.server.core
        if path == "/health":
            return self._send_json(core.get_health())
        if path == "/status":
            return self._send_json(core.get_status())
        if path == "/metrics":
            return self._send_json(core.get_metrics())
        if path == "/control":
            action = params.get("action", [""])[0]
            service_id = params.get("service", [""])[0]
            if action and service_id:
                result = core.control_service(service_id, action)
                return self._send_json(result)
            return self._send_json({"error": "action and service are required"}, status=400)
        if path == "/self-update":
            result = core.perform_self_update()
            status_code = 200 if result.get("status") == "updated" else 500
            return self._send_json(result, status=status_code)
        return self._send_json({"error": "not found"}, status=404)

    def log_message(self, format, *args):
        logger.debug(format % args)


class LocalControlServer(ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass, core, token=None):
        super().__init__(server_address, RequestHandlerClass)
        self.core = core
        self.control_token = token
```

---

### File: `system_utils.py`
- **Path:** `system_utils.py`
- **Estimated Tokens:** 647
- **mtime:** 1781254032.243

```python
import ctypes
import os


def is_system_awake_and_unlocked():
    """
    Returns True if the workstation is unlocked and active.
    If the system is locked, asleep, or the display is off in a secure way,
    OpenInputDesktop will typically fail.
    """
    if os.name != "nt":
        return True

    try:
        user32 = ctypes.windll.user32
        # 0x0100 = DESKTOP_READOBJECTS
        h_desktop = user32.OpenInputDesktop(0, False, 0x0100)
        if h_desktop:
            user32.CloseDesktop(h_desktop)
            return True
        return False
    except Exception:
        return False


def monitor_parent_process(quit_callback, check_interval_sec=5):
    """
    Spawns a background daemon thread that monitors the parent process.
    If the parent process was AeroHub and it exits/terminates, runs quit_callback.
    """
    import threading
    import time
    import psutil
    import logging

    logger = logging.getLogger("AeroHub.ParentMonitor")
    
    parent_pid = os.getppid()
    parent_is_hub = False
    parent_create_time = None

    try:
        parent_proc = psutil.Process(parent_pid)
        parent_cmd = parent_proc.cmdline()
        parent_name = parent_proc.name().lower()
        if any("aerohub.py" in arg.lower() for arg in parent_cmd) or "pythonw_aerohub.exe" in parent_name:
            parent_is_hub = True
            parent_create_time = parent_proc.create_time()
            logger.info(f"Parent process is AeroHub (PID {parent_pid}, created at {parent_create_time})")
    except Exception as e:
        logger.warning(f"Failed to inspect parent process: {e}")

    if not parent_is_hub:
        logger.info("Parent process is not AeroHub. Running in standalone mode.")
        return

    def _monitor():
        while True:
            try:
                parent_proc = psutil.Process(parent_pid)
                if not parent_proc.is_running() or parent_proc.create_time() != parent_create_time or parent_proc.status() == psutil.STATUS_ZOMBIE:
                    logger.warning("Parent AeroHub process has terminated. Initiating shutdown.")
                    quit_callback()
                    break
            except psutil.NoSuchProcess:
                logger.warning("Parent AeroHub process has terminated (no such process). Initiating shutdown.")
                quit_callback()
                break
            except Exception as e:
                logger.error(f"Error checking parent process: {e}")
            time.sleep(check_interval_sec)

    thread = threading.Thread(target=_monitor, daemon=True)
    thread.start()

```

---

### File: `toast_status.json`
- **Path:** `toast_status.json`
- **Estimated Tokens:** 72
- **mtime:** 1781289562.354

```json
{
  "active_toast_pid": 18744,
  "active_toast_end_time": 1781289569.3540497,
  "break_warning_active": false,
  "break_warning_pid": null,
  "break_warning_end_time": 0.0,
  "break_active": false,
  "break_pid": null,
  "break_end_time": 0.0,
  "last_break_end_time": 1781288126.741003
}
```

---

### File: `toast_utils.py`
- **Path:** `toast_utils.py`
- **Estimated Tokens:** 13,632
- **mtime:** 1781212417.573

```python
# ruff: noqa: E402

import tkinter as tk
import threading

# Categorized emojis for the picker
EMOJI_CATEGORIES = {
    "Smileys": [
        "😀",
        "😃",
        "😄",
        "😁",
        "😆",
        "😅",
        "😂",
        "🤣",
        "😊",
        "😇",
        "🙂",
        "🙃",
        "😉",
        "😌",
        "😍",
        "🥰",
        "😘",
        "😗",
        "😙",
        "😚",
        "😋",
        "😛",
        "😝",
        "😜",
        "🤪",
        "🤨",
        "🧐",
        "🤓",
        "😎",
        "🤩",
        "🥳",
        "😏",
        "😒",
        "😞",
        "😔",
        "😟",
        "😕",
        "🙁",
        "☹️",
        "😣",
        "😖",
        "😫",
        "😩",
        "🥺",
        "😢",
        "😭",
        "😤",
        "😠",
        "😡",
        "🤬",
        "🤯",
        "😳",
        "🥵",
        "🥶",
        "😱",
        "😨",
        "😰",
        "😥",
        "😓",
        "🤗",
        "🤔",
        "🤭",
        "🤫",
        "🤥",
        "😶",
        "😐",
        "😑",
        "😬",
        "🙄",
        "😯",
        "😦",
        "😧",
        "😮",
        "😲",
        "🥱",
        "😴",
        "🤤",
        "😪",
        "😵",
        "🤐",
        "🥴",
        "🤢",
        "🤮",
        "🤧",
        "😷",
        "🤒",
        "🤕",
        "🤑",
        "🤠",
        "😈",
        "👿",
        "👹",
        "👺",
        "🤡",
        "💩",
        "👻",
        "💀",
        "☠️",
        "👽",
        "👾",
        "🤖",
        "🎃",
        "😺",
        "😸",
        "😹",
        "😻",
        "😼",
        "😽",
        "🙀",
        "😿",
        "😾",
    ],
    "Gestures": [
        "👋",
        "🤚",
        "🖐️",
        "✋",
        "🖖",
        "👌",
        "🤏",
        "✌️",
        "🤞",
        "🤟",
        "🤘",
        "🤙",
        "👈",
        "👉",
        "👆",
        "🖕",
        "👇",
        "☝️",
        "👍",
        "👎",
        "✊",
        "👊",
        "🤛",
        "🤜",
        "👏",
        "🙌",
        "👐",
        "🤲",
        "🤝",
        "🙏",
        "✍️",
        "💅",
        "🤳",
        "💪",
        "🦾",
        "🦵",
        "🦿",
        "🦶",
        "👂",
        "🦻",
        "👃",
        "🧠",
        "🦷",
        "🦴",
        "👀",
        "👁️",
        "👅",
        "👄",
        "💋",
        "🩸",
    ],
    "Objects & Tech": [
        "💻",
        "🖥️",
        "🖨️",
        "⌨️",
        "🖱️",
        "🖲️",
        "💽",
        "💾",
        "💿",
        "📀",
        "🧮",
        "🎥",
        "🎞️",
        "📽️",
        "🎬",
        "📺",
        "📷",
        "📸",
        "📹",
        "📼",
        "🔍",
        "🔎",
        "🕯️",
        "💡",
        "🔦",
        "🏮",
        "📔",
        "📕",
        "📖",
        "📗",
        "📘",
        "📙",
        "📚",
        "📓",
        "📒",
        "📃",
        "📜",
        "📄",
        "📰",
        "🗞️",
        "📑",
        "🔖",
        "🏷️",
        "💰",
        "🪙",
        "💴",
        "💵",
        "💶",
        "💷",
        "💸",
        "💳",
        "🧾",
        "✉️",
        "📧",
        "📨",
        "📩",
        "📤",
        "📥",
        "📦",
        "📫",
        "📪",
        "📬",
        "📭",
        "📮",
        "🗳️",
        "✏️",
        "✒️",
        "🖋️",
        "🖊️",
        "🖌️",
        "🖍️",
        "📝",
        "💼",
        "📁",
        "📂",
        "🗂️",
        "📅",
        "📆",
        "🗒️",
        "🗓️",
        "📇",
        "📈",
        "📉",
        "📊",
        "📋",
        "📌",
        "📍",
        "📎",
        "🖇️",
        "📏",
        "📐",
        "✂️",
        "🗃️",
        "🗄️",
        "🗑️",
        "🔒",
        "🔓",
        "🔏",
        "🔐",
        "🔑",
        "🗝️",
        "🔨",
        "🪓",
        "⛏️",
        "⚒️",
        "🛠️",
        "🗡️",
        "⚔️",
        "🔫",
        "🏹",
        "🛡️",
        "🔧",
        "🔩",
        "⚙️",
        "🗜️",
        "⚖️",
        "🦯",
        "🔗",
        "⛓️",
        "🧰",
        "🧲",
        "⚗️",
        "🧪",
        "🧫",
        "🧬",
        "🔬",
        "🔭",
        "📡",
        "💉",
        "🩸",
        "💊",
        "🩹",
        "🩺",
        "🚪",
        "🛏️",
        "🛋️",
        "🪑",
        "🚽",
        "🚿",
        "🛁",
        "🪒",
        "🧴",
        "🧷",
        "🧹",
        "🧺",
        "🧻",
        "🧼",
        "🧽",
        "🧯",
        "🛒",
        "🚬",
        "⚰️",
        "⚱️",
        "🗿",
    ],
    "Symbols": [
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "🤍",
        "🤎",
        "💔",
        "❣️",
        "💕",
        "💞",
        "💓",
        "💗",
        "💖",
        "💘",
        "💝",
        "💟",
        "☮️",
        "✝️",
        "☪️",
        "🕉️",
        "☸️",
        "✡️",
        "🔯",
        "🕎",
        "☯️",
        "☦️",
        "🛐",
        "⛎",
        "♈",
        "♉",
        "♊",
        "♋",
        "♌",
        "♍",
        "♎",
        "♏",
        "♐",
        "♑",
        "♒",
        "♓",
        "🆔",
        "⚛️",
        "⚕️",
        "☢️",
        "☣️",
        "📴",
        "📳",
        "🈶",
        "🈚",
        "🈸",
        "🈺",
        "🈷️",
        "✴️",
        "🆚",
        "🉑",
        "💮",
        "🉐",
        "㊙️",
        "㊗️",
        "🈴",
        "🈵",
        "🈹",
        "🈲",
        "🅰️",
        "🅱️",
        "🆎",
        "🆑",
        "🅾️",
        "🆘",
        "❌",
        "⭕",
        "🛑",
        "⛔",
        "📛",
        "🚫",
        "💯",
        "💢",
        "♨️",
        "🚷",
        "🚯",
        "🚳",
        "🚱",
        "🔞",
        "📵",
        "🚭",
        "❗",
        "❕",
        "❓",
        "❔",
        "‼️",
        "⁉️",
        "🔅",
        "🔆",
        "〽️",
        "⚠️",
        "🚸",
        "🔱",
        "⚜️",
        "🔰",
        "♻️",
        "✅",
        "🈯",
        "💹",
        "❇️",
        "✳️",
        "❎",
        "🌐",
        "💠",
        "Ⓜ️",
        "🌀",
        "💤",
        "🏧",
        "🚾",
        "♿",
        "🅿️",
        "🈳",
        "🈂️",
        "🛂",
        "🛃",
        "🛄",
        "🛅",
        "🚹",
        "🚺",
        "🚼",
        "🚻",
        "🚮",
        "🎦",
        "📶",
        "🈁",
        "🔣",
        "ℹ️",
        "🔤",
        "🔡",
        "🔠",
        "🆖",
        "🆗",
        "🆙",
        "🆒",
        "🆕",
        "🆓",
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "🔟",
        "🔢",
        "#️⃣",
        "*️⃣",
        "⏏️",
        "▶️",
        "⏸️",
        "⏯️",
        "⏹️",
        "⏺️",
        "⏭️",
        "⏮️",
        "⏩",
        "⏪",
        "⏫",
        "⏬",
        "◀️",
        "🔼",
        "🔽",
        "➡️",
        "⬅️",
        "⬆️",
        "⬇️",
        "↗️",
        "↘️",
        "↙️",
        "↖️",
        "↕️",
        "↔️",
        "↪️",
        "↩️",
        "⤴️",
        "⤵️",
        "🔀",
        "🔁",
        "🔂",
        "🔄",
        "🔃",
        "🎵",
        "🎶",
        "➕",
        "➖",
        "➗",
        "✖️",
        "♾️",
        "💲",
        "💱",
        "™️",
        "©️",
        "®️",
        "〰️",
        "➰",
        "➿",
        "🔚",
        "🔙",
        "🔛",
        "🔝",
        "🔜",
        "✔️",
        "☑️",
        "🔘",
        "🔴",
        "🟠",
        "🟡",
        "🟢",
        "🔵",
        "🟣",
        "⚫",
        "⚪",
        "🟤",
        "🔺",
        "🔻",
        "🔸",
        "🔹",
        "🔶",
        "🔷",
        "🔳",
        "🔲",
        "▪️",
        "▫️",
        "◾",
        "◽",
        "◼️",
        "◻️",
        "🟥",
        "🟧",
        "🟨",
        "🟩",
        "🟦",
        "🟪",
        "⬛",
        "⬜",
        "🟫",
        "🔈",
        "🔇",
        "🔉",
        "🔊",
        "🔔",
        "🔕",
        "📣",
        "📢",
        "💬",
        "💭",
        "🗯️",
        "♠️",
        "♣️",
        "♥️",
        "♦️",
        "🃏",
        "🎴",
        "🀄",
        "🕐",
        "🕑",
        "🕒",
        "🕓",
        "🕔",
        "🕕",
        "🕖",
        "🕗",
        "🕘",
        "🕙",
        "🕚",
        "🕛",
        "🕜",
        "🕝",
        "🕞",
        "🕟",
        "🕠",
        "🕡",
        "🕢",
        "🕣",
        "🕤",
        "🕥",
        "🕦",
        "🕧",
    ],
}


class EmojiPickerPanel(tk.Toplevel):
    """A popup window to pick an emoji."""

    def __init__(self, parent, on_select_callback):
        super().__init__(parent)
        self.on_select_callback = on_select_callback

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(
            bg="#1e1e1e",
            padx=2,
            pady=2,
            highlightthickness=1,
            highlightbackground="#3e3e3e",
        )

        # Determine position near cursor
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        self.geometry(f"340x260+{x}+{y}")

        # Title bar
        title_frame = tk.Frame(self, bg="#2d2d2d", height=24)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="Select Emoji",
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.LEFT, padx=8)
        close_btn = tk.Button(
            title_frame,
            text="✕",
            bg="#2d2d2d",
            fg="#ffffff",
            relief=tk.FLAT,
            bd=0,
            command=self.destroy,
            font=("Segoe UI", 9),
        )
        close_btn.pack(side=tk.RIGHT, padx=4)

        # Tabs
        self.tab_frame = tk.Frame(self, bg="#1e1e1e")
        self.tab_frame.pack(fill=tk.X, pady=2)

        # Content frame
        self.content_frame = tk.Frame(self, bg="#1e1e1e")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.canvases = {}
        self.current_tab = None
        self.tab_buttons = {}

        for cat in EMOJI_CATEGORIES.keys():
            btn = tk.Button(
                self.tab_frame,
                text=cat,
                bg="#1e1e1e",
                fg="#a0a0a0",
                relief=tk.FLAT,
                bd=0,
                font=("Segoe UI", 8),
                command=lambda c=cat: self.show_category(c),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tab_buttons[cat] = btn

            # Create a canvas with scrollbar for each category
            f = tk.Frame(self.content_frame, bg="#1e1e1e")
            canvas = tk.Canvas(f, bg="#1e1e1e", highlightthickness=0)
            scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                ),
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Grid of emojis
            col = 0
            row = 0
            for emoji in EMOJI_CATEGORIES[cat]:
                ebtn = tk.Button(
                    scrollable_frame,
                    text=emoji,
                    font=("Segoe UI Emoji", 14),
                    bg="#1e1e1e",
                    fg="#ffffff",
                    relief=tk.FLAT,
                    bd=0,
                    activebackground="#3e3e3e",
                    cursor="hand2",
                    command=lambda e=emoji: self.select_emoji(e),
                )
                ebtn.grid(row=row, column=col, padx=2, pady=2)
                col += 1
                if col > 8:
                    col = 0
                    row += 1

            # Enable mouse wheel scrolling
            def _on_mousewheel(event):
                try:
                    w = event.widget.winfo_containing(event.x_root, event.y_root)
                    while w:
                        if isinstance(w, tk.Canvas):
                            w.yview_scroll(int(-1 * (event.delta / 120)), "units")
                            break
                        w = w.master
                except Exception:
                    pass

            self.bind_all("<MouseWheel>", _on_mousewheel)

            canvas.pack(side="left", fill="both", expand=True)

            self.canvases[cat] = f

        # Show first category
        self.show_category(list(EMOJI_CATEGORIES.keys())[0])

    def show_category(self, cat):
        if self.current_tab:
            self.canvases[self.current_tab].pack_forget()
            self.tab_buttons[self.current_tab].config(fg="#a0a0a0", bg="#1e1e1e")

        self.canvases[cat].pack(fill=tk.BOTH, expand=True)
        self.tab_buttons[cat].config(fg="#ffffff", bg="#3e3e3e")
        self.current_tab = cat

    def select_emoji(self, emoji):
        self.on_select_callback(emoji)
        self.destroy()

    def destroy(self):
        try:
            self.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()


import os
import json
import time
import psutil

# Path to cross-process toast status file in the UTILITIES directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(SCRIPT_DIR, "toast_status.json")

def read_shared_status() -> dict:
    if not os.path.exists(STATUS_FILE):
        return {}
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def write_shared_status(status: dict):
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)
    except Exception:
        pass

def is_process_running(pid: int) -> bool:
    if not pid:
        return False
    try:
        return psutil.pid_exists(pid)
    except Exception:
        return False

def is_any_toast_active() -> bool:
    status = read_shared_status()
    pid = status.get("active_toast_pid")
    end_time = status.get("active_toast_end_time", 0.0)
    
    # If break overlay is active, block toasts
    if status.get("break_active") and is_process_running(status.get("break_pid")):
        return True
        
    # If another process's toast is active, block toasts
    if pid and pid != os.getpid() and is_process_running(pid) and time.time() < end_time:
        return True
        
    return False

def is_in_break_period_shared() -> bool:
    status = read_shared_status()
    now = time.time()
    
    # 1. Break warning active
    if status.get("break_warning_active") and is_process_running(status.get("break_warning_pid")):
        if now < status.get("break_warning_end_time", 0.0):
            return True
            
    # 2. Break active
    if status.get("break_active") and is_process_running(status.get("break_pid")):
        return True
        
    # 3. Within 10 seconds after a break ended
    last_end = status.get("last_break_end_time", 0.0)
    if now - last_end < 10.0:
        return True
        
    return False


class ToastQueue:
    _lock = threading.Lock()
    _queue = []
    _active = None
    _delay_active = False

    @classmethod
    def add(cls, toast):
        with cls._lock:
            cls._queue.append(toast)
        cls.process_queue()

    @classmethod
    def process_queue(cls):
        with cls._lock:
            if cls._active or cls._delay_active:
                return
            if not cls._queue:
                return
            
            # Check if another process has an active toast or break
            if is_any_toast_active():
                next_toast = cls._queue[0]
                if next_toast.parent:
                    try:
                        next_toast.parent.after(500, cls.process_queue)
                        return
                    except Exception:
                        pass
                import threading
                threading.Timer(0.5, cls.process_queue).start()
                return

            cls._active = cls._queue.pop(0)

        try:
            cls._active._create_toast()
        except Exception as e:
            print(f"Error creating queued toast: {e}")
            cls.on_toast_closed(None)

    @classmethod
    def on_toast_closed(cls, parent):
        with cls._lock:
            cls._active = None
            cls._delay_active = True

        def reset_delay():
            with cls._lock:
                cls._delay_active = False
            cls.process_queue()

        if parent:
            try:
                parent.after(1500, reset_delay)
                return
            except Exception:
                pass

        try:
            if BaseToast._root:
                BaseToast._root.after(1500, reset_delay)
                return
        except Exception:
            pass

        threading.Timer(1.5, reset_delay).start()


class BaseToast:
    """
    A highly customizable unified toast notification class.
    Supports 9 positions, 7 animations, shadows, gradients, and behavioral settings.
    """

    _active_toasts = []
    _lock = threading.Lock()
    _root = None

    def __init__(
        self,
        parent,
        title: str,
        message: str,
        settings: dict,
        is_health_tip: bool = False,
        on_click=None,
    ):
        self.parent = parent
        self.title = title
        self.message = message
        self.settings = settings
        self.is_health_tip = is_health_tip
        self.on_click = on_click
        self.closing = False
        self.toast_window = None
        self.hold_time = 0
        self.slot_index = 0
        self.pos = "center"

    def show(self):
        try:
            # Skip if we are in the break period, unless this is a break warning itself
            is_break_warning = "break in" in self.title.lower() or "break in" in self.message.lower() or "eye break" in self.title.lower()
            if not is_break_warning and is_in_break_period_shared():
                print(f"Discarding toast '{self.title}' because we are in a break period.")
                return
            if self.settings.get("is_preview", False):
                self._create_toast()
                return
            ToastQueue.add(self)
        except Exception as e:
            print(f"Error queuing toast: {e}")

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (0, 0, 0)

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def interpolate_color(self, c1, c2, factor):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3))

    def _create_toast(self):
        root = self.parent
        if not root:
            root = tk.Tk()
            root.withdraw()
        BaseToast._root = root

        toast = tk.Toplevel(root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        trans_color = "#010203"
        toast.configure(bg=trans_color)
        toast.attributes("-transparentcolor", trans_color)
        toast.attributes("-alpha", 0.0)

        # Retrieve visual settings
        prefix = "ht_toast_" if self.is_health_tip else "toast_"
        tw = int(self.settings.get(f"{prefix}width", 260))
        th = int(self.settings.get(f"{prefix}height", 60))
        pos = self.settings.get(f"{prefix}pos", "Center").lower()
        if pos == "random":
            import random

            pos = random.choice(
                [
                    "top-left",
                    "top-center",
                    "top-right",
                    "bottom-left",
                    "bottom-center",
                    "bottom-right",
                    "middle-left",
                    "middle-right",
                ]
            )
        bg_col = self.settings.get(f"{prefix}bg_color", "#252525")
        fg_col = self.settings.get(f"{prefix}fg_color", "#ffffff")
        accent_default = "#00f0ff" if prefix in ("toast_", "ht_toast_") else "#7c3aed"
        accent_col = self.settings.get(f"{prefix}accent_color", accent_default)
        font_size = int(self.settings.get(f"{prefix}font_size", 11))
        font_weight = self.settings.get(f"{prefix}font_weight", "bold")
        font_family = self.settings.get(f"{prefix}font_family", "Segoe UI")
        emoji = self.settings.get(f"{prefix}emoji", "👁️")
        radius = int(self.settings.get(f"{prefix}radius", 16))
        padx = int(self.settings.get(f"{prefix}padding_x", 12))
        pady = int(self.settings.get(f"{prefix}padding_y", 10))
        anim_style = self.settings.get(f"{prefix}anim_style", "Slide").lower()
        target_opacity = float(self.settings.get(f"{prefix}opacity", 0.92))
        border_width = int(self.settings.get(f"{prefix}border_width", 0))
        border_color = self.settings.get(f"{prefix}border_color", accent_default)

        # ── Sanitize settings ──
        # Clamp opacity to valid range
        target_opacity = max(0.0, min(1.0, target_opacity))

        # Fallback empty color strings to defaults
        if not bg_col or not bg_col.startswith("#"):
            bg_col = "#252525"
        if not fg_col or not fg_col.startswith("#"):
            fg_col = "#ffffff"
        if not accent_col or not accent_col.startswith("#"):
            accent_col = accent_default
        if not border_color or not border_color.startswith("#"):
            border_color = accent_default
        if not emoji:
            emoji = "👁️" if not self.is_health_tip else "💡"

        # Prevent any color from matching the transparent key color
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if accent_col == trans_color:
            accent_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"

        # Clamp padding so text doesn't render off-canvas
        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

        # New visual features
        _enable_gradient = self.settings.get(f"{prefix}gradient", False)
        enable_shadow = self.settings.get(f"{prefix}shadow", True)
        accent_stripe = self.settings.get(f"{prefix}accent_stripe", False)
        text_align = self.settings.get(f"{prefix}text_align", "left")

        # Behavioral settings
        transition_ms = int(self.settings.get(f"{prefix}transition_time_ms", 320))
        transition_sec = max(0.01, transition_ms / 1000.0)

        if self.is_health_tip:
            duration_sec = float(self.settings.get(f"{prefix}duration_sec", self.settings.get("ht_duration_sec", 5)))
        else:
            duration_sec = float(self.settings.get(
                f"{prefix}duration_sec", self.settings.get(f"{prefix}duration", self.settings.get("pre_warning_sec", 5))
            ))
        auto_dismiss = self.settings.get(f"{prefix}auto_dismiss", True)
        click_action = self.settings.get(f"{prefix}click_action", "dismiss")

        # Register this toast in cross-process shared status
        status = read_shared_status()
        status["active_toast_pid"] = os.getpid()
        status["active_toast_end_time"] = time.time() + (duration_sec if auto_dismiss else 999999) + 2
        write_shared_status(status)

        shadow_offset = 6 if enable_shadow else 0
        canvas_w = tw + shadow_offset * 2
        canvas_h = th + shadow_offset * 2

        # Screen positions (9 points)
        sw = toast.winfo_screenwidth()
        sh = toast.winfo_screenheight()
        padding_edge = 20

        fx, fy = 0, 0
        if "top" in pos or pos in ("left", "center", "right"):
            fy = padding_edge
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "bottom" in pos:
            fy = sh - th - 50  # account for taskbar
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "middle" in pos:
            fy = (sh - th) // 2
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        else:
            # custom offset
            fx = int(self.settings.get(f"{prefix}custom_x", (sw - tw) // 2))
            fy = int(self.settings.get(f"{prefix}custom_y", padding_edge))

        self.pos = pos
        # Adjust for multiple toasts stacking
        with BaseToast._lock:
            # Find the first available slot index for this position to prevent overlap
            occupied_slots = {
                t.slot_index
                for t in BaseToast._active_toasts
                if getattr(t, "pos", None) == self.pos
            }
            self.slot_index = 0
            while self.slot_index in occupied_slots:
                self.slot_index += 1

            y_offset = self.slot_index * (th + 10)
            if "bottom" in self.pos:
                fy -= y_offset
            else:
                fy += y_offset
            BaseToast._active_toasts.append(self)
            self.toast_window = toast

        # Animation start points
        sx, sy = fx, fy
        if anim_style == "slide":
            if "left" in pos:
                sx = -tw - shadow_offset
            elif "right" in pos:
                sx = sw + shadow_offset
            elif "top" in pos or pos == "center":
                sy = -th - shadow_offset
            elif "bottom" in pos:
                sy = sh + shadow_offset
        elif anim_style == "drop":
            sy = -th - 100
        elif anim_style == "bounce":
            if "left" in pos:
                sx = -tw - 50
            elif "right" in pos:
                sx = sw + 50
            else:
                sy = -th - 50

        toast.geometry(f"{canvas_w}x{canvas_h}+{sx}+{sy}")

        canvas = tk.Canvas(
            toast, width=canvas_w, height=canvas_h, bg=trans_color, highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas = canvas

        def create_round_poly(x, y, w, h, r):
            return [
                x + r,
                y,
                w - r,
                y,
                w,
                y,
                w,
                y + r,
                w,
                h - r,
                w,
                h,
                w - r,
                h,
                x + r,
                h,
                x,
                h,
                x,
                h - r,
                x,
                y + r,
                x,
                y,
            ]

        # Shadow
        shadow_id = None
        if enable_shadow:
            shadow_poly = create_round_poly(
                shadow_offset,
                shadow_offset,
                tw + shadow_offset,
                th + shadow_offset,
                radius,
            )
            shadow_id = canvas.create_polygon(shadow_poly, smooth=True, fill="#080808")

        bg_poly = create_round_poly(
            shadow_offset // 2,
            shadow_offset // 2,
            tw + shadow_offset // 2,
            th + shadow_offset // 2,
            radius,
        )

        border_style = self.settings.get(f"{prefix}border_style", "Solid")
        dash_val = ()
        if border_style == "Dashed":
            dash_val = (6, 4)
        elif border_style == "Dotted":
            dash_val = (2, 2)

        bg_id = canvas.create_polygon(
            bg_poly,
            smooth=True,
            fill=bg_col,
            outline=border_color,
            width=border_width,
            dash=dash_val,
        )

        # Accent Stripe
        stripe_id = None
        if accent_stripe:
            stripe_pos = self.settings.get(f"{prefix}stripe_pos", "Left")
            if stripe_pos == "Right":
                stripe_poly = [
                    tw + shadow_offset // 2 - radius - 4, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + radius,
                    tw + shadow_offset // 2, th + shadow_offset // 2 - radius,
                    tw + shadow_offset // 2 - radius - 4, th + shadow_offset // 2,
                ]
            elif stripe_pos == "Top":
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    tw + shadow_offset // 2 - radius, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + 4,
                    shadow_offset // 2, shadow_offset // 2 + 4
                ]
            elif stripe_pos == "Bottom":
                stripe_poly = [
                    shadow_offset // 2 + radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2 - radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2
                ]
            else: # Left
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, th + shadow_offset // 2,
                    shadow_offset // 2 + radius, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2 - radius,
                    shadow_offset // 2, shadow_offset // 2 + radius
                ]
            stripe_id = canvas.create_polygon(stripe_poly, smooth=True, fill=accent_col)

        # Content
        msg_font = (font_family, font_size, font_weight)
        sub_font = (font_family, max(8, font_size - 2))

        # Fallback font for emojis (moved to execute before rendering text)
        if msg_font[0] == "Segoe UI" or msg_font[0] == "Segoe UI Emoji":
            msg_font = (
                "Segoe UI Emoji",
                msg_font[1],
                msg_font[2] if len(msg_font) > 2 else "normal",
            )

        anchor = tk.W
        tx = shadow_offset // 2 + padx + 10
        if text_align == "center":
            anchor = tk.CENTER
            tx = shadow_offset // 2 + tw // 2
        elif text_align == "right":
            anchor = tk.E
            tx = shadow_offset // 2 + tw - padx - 10

        desc_text_id = None
        
        # Add clock time if enabled
        show_clock = self.settings.get(f"{prefix}show_clock", False)
        clock_str = f" - {time.strftime('%I:%M %p')}" if show_clock else ""
        
        if self.is_health_tip:
            text_id = canvas.create_text(
                tx,
                shadow_offset // 2 + th // 2,
                anchor=anchor,
                text=f"{emoji}  {self.message}{clock_str}",
                font=msg_font,
                fill=fg_col,
                width=tw - (padx + 10) * 2,
            )
        else:
            text_id = canvas.create_text(
                tx,
                shadow_offset // 2 + pady,
                anchor=anchor,
                text=f"{emoji}  {self.title}{clock_str}",
                font=msg_font,
                fill=fg_col,
            )
            desc_text_id = canvas.create_text(
                tx,
                shadow_offset // 2 + pady + font_size + 8,
                anchor=anchor,
                text=self.message,
                font=sub_font,
                fill="#8892b0",
                width=tw - (padx + 10) * 2,
            )

        # Progress bar
        show_progress = self.settings.get(f"{prefix}progress_bar", False)
        progress_bar = None
        if show_progress and auto_dismiss and duration_sec > 0:
            bar_y = shadow_offset // 2 + th - 4
            progress_bar = canvas.create_rectangle(
                shadow_offset // 2 + radius,
                bar_y,
                shadow_offset // 2 + tw - radius,
                bar_y + 2,
                fill=accent_col,
                outline="",
            )

        # Interaction
        self._drag_data = {"x": 0, "y": 0, "dragged": False}

        def on_press(event):
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root
            self._drag_data["dragged"] = False

        def on_drag(event):
            dx = event.x_root - self._drag_data["x"]
            dy = event.y_root - self._drag_data["y"]
            if abs(dx) > 3 or abs(dy) > 3:
                self._drag_data["dragged"] = True
            x = toast.winfo_x() + dx
            y = toast.winfo_y() + dy
            toast.geometry(f"+{x}+{y}")
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root

        def on_click_event(event):
            if self._drag_data.get("dragged"):
                return
            self.force_close()  # Always dismiss immediately on click
            if click_action == "snooze":
                if self.on_click:
                    self.on_click("snooze")
            elif click_action == "settings":
                if self.on_click:
                    self.on_click("settings")
            elif click_action != "dismiss":
                if self.on_click:
                    self.on_click("custom")

        toast.bind("<ButtonPress-1>", on_press)
        toast.bind("<B1-Motion>", on_drag)
        toast.bind("<ButtonRelease-1>", on_click_event)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_click_event)

        self.is_hovered = False

        def on_enter(e):
            self.is_hovered = True

        def on_leave(e):
            self.is_hovered = False

        toast.bind("<Enter>", on_enter)
        toast.bind("<Leave>", on_leave)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)

        # Emoji fallback check moved above

        # Adjust height if text is too tall
        original_th = th
        if self.is_health_tip:
            bbox = canvas.bbox(text_id)
            if bbox and (bbox[3] - bbox[1] > th - 20):
                th = bbox[3] - bbox[1] + 20
                canvas_h = th + shadow_offset
                toast.geometry(f"{canvas_w}x{canvas_h}")
                canvas.configure(height=canvas_h)
                canvas.coords(text_id, tx, shadow_offset // 2 + th // 2)
        else:
            bbox_title = canvas.bbox(text_id)
            bbox_desc = canvas.bbox(desc_text_id)
            if bbox_title and bbox_desc:
                title_h = bbox_title[3] - bbox_title[1]
                desc_h = bbox_desc[3] - bbox_desc[1]
                total_needed = pady + title_h + 8 + desc_h + pady
                if total_needed > th:
                    th = total_needed
                    canvas_h = th + shadow_offset
                    toast.geometry(f"{canvas_w}x{canvas_h}")
                    canvas.configure(height=canvas_h)
                    desc_y = bbox_title[3] + 8 + desc_h // 2
                    canvas.coords(desc_text_id, tx, desc_y)

        # Update background and shadow polygons if height adjusted
        if th > original_th:
            new_bg_poly = create_round_poly(
                shadow_offset // 2,
                shadow_offset // 2,
                tw + shadow_offset // 2,
                th + shadow_offset // 2,
                radius,
            )
            canvas.coords(bg_id, *new_bg_poly)
            if shadow_id:
                new_shadow_poly = create_round_poly(
                    shadow_offset,
                    shadow_offset,
                    tw + shadow_offset,
                    th + shadow_offset,
                    radius,
                )
                canvas.coords(shadow_id, *new_shadow_poly)
            if stripe_id:
                new_stripe_poly = [
                    shadow_offset // 2 + radius,
                    shadow_offset // 2,
                    shadow_offset // 2 + radius + 4,
                    shadow_offset // 2,
                    shadow_offset // 2 + radius + 4,
                    th + shadow_offset // 2,
                    shadow_offset // 2 + radius,
                    th + shadow_offset // 2,
                    shadow_offset // 2,
                    th + shadow_offset // 2 - radius,
                    shadow_offset // 2,
                    shadow_offset // 2 + radius,
                ]
                canvas.coords(stripe_id, *new_stripe_poly)
            if progress_bar:
                bar_y = shadow_offset // 2 + th - 4
                canvas.coords(
                    progress_bar,
                    shadow_offset // 2 + radius,
                    bar_y,
                    shadow_offset // 2 + tw - radius,
                    bar_y + 2,
                )

        # Typewriter effect helper
        if anim_style == "typewriter":
            if self.is_health_tip:
                full_text = f"{emoji}  {self.message}"
                canvas.itemconfig(text_id, text="")

                def type_char(idx=0):
                    if self.closing:
                        return
                    if idx <= len(full_text):
                        canvas.itemconfig(text_id, text=full_text[:idx])
                        toast.after(30, lambda: type_char(idx + 1))

                toast.after(200, type_char)
            else:
                full_title = f"{emoji}  {self.title}"
                canvas.itemconfig(text_id, text="")
                full_desc = self.message
                canvas.itemconfig(desc_text_id, text="")

                def type_desc(idx=0):
                    if self.closing:
                        return
                    if idx <= len(full_desc):
                        canvas.itemconfig(desc_text_id, text=full_desc[:idx])
                        toast.after(20, lambda: type_desc(idx + 1))

                def type_title(idx=0):
                    if self.closing:
                        return
                    if idx <= len(full_title):
                        canvas.itemconfig(text_id, text=full_title[:idx])
                        toast.after(30, lambda: type_title(idx + 1))
                    else:
                        toast.after(100, lambda: type_desc(0))

                toast.after(200, type_title)

        # Animations
        self.start_time = time.perf_counter()

        def animate_in():
            if self.closing:
                return
            try:
                elapsed = time.perf_counter() - self.start_time
                p = min(1.0, elapsed / transition_sec)

                if anim_style == "fade" or anim_style == "typewriter":
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
                    toast.attributes("-alpha", p * target_opacity)
                elif anim_style == "slide":
                    ease = 1 - (1 - p) ** 3
                    cx = int(sx + (fx - sx) * ease)
                    cy = int(sy + (fy - sy) * ease)
                    toast.geometry(f"{canvas_w}x{canvas_h}+{cx}+{cy}")
                    toast.attributes("-alpha", target_opacity)
                elif anim_style == "bounce":
                    ease = 1 - (1 - p) ** 3
                    # Add elastic overshoot
                    if p < 0.8:
                        overshoot = 1.1 * (p / 0.8)
                    else:
                        overshoot = 1.1 - 0.1 * ((p - 0.8) / 0.2)
                    cx = int(sx + (fx - sx) * overshoot)
                    cy = int(sy + (fy - sy) * overshoot)
                    toast.geometry(f"{canvas_w}x{canvas_h}+{cx}+{cy}")
                    toast.attributes("-alpha", target_opacity)
                elif anim_style == "scale":
                    ease = p
                    cy = int(fy + 10 * (1 - ease))
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{cy}")
                    toast.attributes("-alpha", p * target_opacity)
                elif anim_style == "glow":
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
                    glow_a = (
                        target_opacity
                        if int(elapsed * 10) % 2 == 0
                        else target_opacity * 0.5
                    )
                    toast.attributes("-alpha", glow_a)
                elif anim_style == "drop":
                    ease = p * p  # accelerate
                    cy = int(sy + (fy - sy) * ease)
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{cy}")
                    toast.attributes("-alpha", p * target_opacity)
                else:
                    # Default fallback
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
                    toast.attributes("-alpha", target_opacity)

                if p < 1.0:
                    toast.after(16, animate_in)
                else:
                    if anim_style == "glow":
                        toast.attributes("-alpha", target_opacity)  # settle
                    if auto_dismiss and duration_sec > 0:
                        update_progress()
            except Exception:
                self.cleanup()

        self.hover_time = 0

        def update_progress():
            if self.closing:
                return
            try:
                if not self.is_hovered or self.hover_time > 15000:
                    self.hold_time += 50
                    if show_progress and progress_bar:
                        p = self.hold_time / (duration_sec * 1000)
                        cur_w = (tw - radius * 2) * (1 - p)
                        if cur_w > 0:
                            canvas.coords(
                                progress_bar,
                                shadow_offset // 2 + radius,
                                bar_y,
                                shadow_offset // 2 + radius + cur_w,
                                bar_y + 2,
                            )

                    if self.hold_time >= duration_sec * 1000:
                        self.out_start_time = time.perf_counter()
                        animate_out()
                        return
                else:
                    self.hover_time += 50
                toast.after(50, update_progress)
            except Exception:
                self.cleanup()

        def animate_out():
            self.closing = True
            try:
                if not hasattr(self, 'out_start_time'):
                    self.out_start_time = time.perf_counter()
                
                elapsed = time.perf_counter() - self.out_start_time
                p = max(0.0, 1.0 - (elapsed / transition_sec))
                
                toast.attributes("-alpha", p * target_opacity)
                if p > 0:
                    toast.after(16, animate_out)
                else:
                    self.cleanup()
            except Exception:
                self.cleanup()

        self.force_close = animate_out

        toast.deiconify()
        animate_in()

        # Play sound if applicable
        play_sound = self.settings.get(f"{prefix}enable_sound", False)
        if play_sound:
            self._play_sound()

    def _play_sound(self):
        try:
            import os
            prefix = "ht_toast_" if self.is_health_tip else "toast_"
            default_snd = "mac_disconnect" if self.is_health_tip else "mac_connect"
            snd_choice = self.settings.get(f"{prefix}sound_effect", default_snd)
            volume = float(self.settings.get(f"{prefix}volume", 80))

            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]

            is_alias = snd_choice in system_aliases
            if not is_alias:
                if not snd_choice.endswith(".wav"):
                    snd_choice += ".wav"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(script_dir, "HealthApp", "resources", "sounds", snd_choice)
                if not os.path.exists(path):
                    path = os.path.join(script_dir, "BatteryMonitor", "sounds", snd_choice)
            else:
                path = None

            # Try playing using Pygame Sound if pygame is active/initialized
            try:
                import pygame
                if pygame.mixer.get_init() and path and os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(volume / 100.0)
                    sound.play()
                    return
            except Exception:
                pass

            # Fallback to winsound
            import winsound
            if is_alias:
                winsound.PlaySound(snd_choice, winsound.SND_ALIAS | winsound.SND_ASYNC)
            elif path and os.path.exists(path):
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def update_settings(self, settings):
        self.settings = settings
        if not self.toast_window or not self.toast_window.winfo_exists():
            return
            
        prefix = "ht_toast_" if self.is_health_tip else "toast_"
        tw = int(self.settings.get(f"{prefix}width", 260))
        th = int(self.settings.get(f"{prefix}height", 60))
        pos = self.settings.get(f"{prefix}pos", "Center").lower()
        if pos == "random":
            pos = "center"
        bg_col = self.settings.get(f"{prefix}bg_color", "#252525")
        fg_col = self.settings.get(f"{prefix}fg_color", "#ffffff")
        accent_default = "#00f0ff" if prefix in ("toast_", "ht_toast_") else "#7c3aed"
        accent_col = self.settings.get(f"{prefix}accent_color", accent_default)
        font_size = int(self.settings.get(f"{prefix}font_size", 11))
        font_weight = self.settings.get(f"{prefix}font_weight", "bold")
        font_family = self.settings.get(f"{prefix}font_family", "Segoe UI")
        emoji = self.settings.get(f"{prefix}emoji", "👁️")
        radius = int(self.settings.get(f"{prefix}radius", 16))
        padx = int(self.settings.get(f"{prefix}padding_x", 12))
        pady = int(self.settings.get(f"{prefix}padding_y", 10))
        _anim_style = self.settings.get(f"{prefix}anim_style", "Slide").lower()
        target_opacity = float(self.settings.get(f"{prefix}opacity", 0.92))
        border_width = int(self.settings.get(f"{prefix}border_width", 0))
        border_color = self.settings.get(f"{prefix}border_color", accent_default)

        target_opacity = max(0.0, min(1.0, target_opacity))
        if not bg_col or not bg_col.startswith("#"):
            bg_col = "#252525"
        if not fg_col or not fg_col.startswith("#"):
            fg_col = "#ffffff"
        if not accent_col or not accent_col.startswith("#"):
            accent_col = accent_default
        if not border_color or not border_color.startswith("#"):
            border_color = accent_default
        if not emoji:
            emoji = "👁️" if not self.is_health_tip else "💡"
            
        trans_color = "#010203"
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if accent_col == trans_color:
            accent_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"

        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

        enable_shadow = self.settings.get(f"{prefix}shadow", True)
        accent_stripe = self.settings.get(f"{prefix}accent_stripe", False)
        text_align = self.settings.get(f"{prefix}text_align", "left")

        shadow_offset = 6 if enable_shadow else 0
        canvas_w = tw + shadow_offset * 2
        canvas_h = th + shadow_offset * 2

        sw = self.toast_window.winfo_screenwidth()
        sh = self.toast_window.winfo_screenheight()
        padding_edge = 20
        fx, fy = 0, 0
        if "top" in pos or pos in ("left", "center", "right"):
            fy = padding_edge
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "bottom" in pos:
            fy = sh - th - 50
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "middle" in pos:
            fy = (sh - th) // 2
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        else:
            fx = int(self.settings.get(f"{prefix}custom_x", (sw - tw) // 2))
            fy = int(self.settings.get(f"{prefix}custom_y", padding_edge))

        self.pos = pos
        y_offset = self.slot_index * (th + 10)
        if "bottom" in self.pos:
            fy -= y_offset
        else:
            fy += y_offset

        try:
            self.toast_window.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
            self.toast_window.attributes("-alpha", target_opacity)
        except tk.TclError:
            pass

        canvas = self.canvas
        canvas.delete("all")
        canvas.configure(width=canvas_w, height=canvas_h)

        def create_round_poly(x, y, w, h, r):
            return [x + r, y, w - r, y, w, y, w, y + r, w, h - r, w, h, w - r, h, x + r, h, x, h, x, h - r, x, y + r, x, y]

        # Shadow
        if enable_shadow:
            shadow_poly = create_round_poly(shadow_offset, shadow_offset, tw + shadow_offset, th + shadow_offset, radius)
            canvas.create_polygon(shadow_poly, smooth=True, fill="#080808")

        # Main background
        bg_poly = create_round_poly(shadow_offset // 2, shadow_offset // 2, tw + shadow_offset // 2, th + shadow_offset // 2, radius)
        
        border_style = self.settings.get(f"{prefix}border_style", "Solid")
        dash_val = ()
        if border_style == "Dashed":
            dash_val = (6, 4)
        elif border_style == "Dotted":
            dash_val = (2, 2)
            
        canvas.create_polygon(bg_poly, smooth=True, fill=bg_col, outline=border_color, width=border_width, dash=dash_val)

        # Accent Stripe
        if accent_stripe:
            stripe_pos = self.settings.get(f"{prefix}stripe_pos", "Left")
            if stripe_pos == "Right":
                stripe_poly = [
                    tw + shadow_offset // 2 - radius - 4, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + radius,
                    tw + shadow_offset // 2, th + shadow_offset // 2 - radius,
                    tw + shadow_offset // 2 - radius - 4, th + shadow_offset // 2,
                ]
            elif stripe_pos == "Top":
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    tw + shadow_offset // 2 - radius, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + 4,
                    shadow_offset // 2, shadow_offset // 2 + 4
                ]
            elif stripe_pos == "Bottom":
                stripe_poly = [
                    shadow_offset // 2 + radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2 - radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2
                ]
            else: # Left
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, th + shadow_offset // 2,
                    shadow_offset // 2 + radius, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2 - radius,
                    shadow_offset // 2, shadow_offset // 2 + radius
                ]
            canvas.create_polygon(stripe_poly, smooth=True, fill=accent_col)

        msg_font = (font_family, font_size, font_weight)
        sub_font = (font_family, max(8, font_size - 2))

        if msg_font[0] == "Segoe UI" or msg_font[0] == "Segoe UI Emoji":
            msg_font = ("Segoe UI Emoji", msg_font[1], msg_font[2] if len(msg_font) > 2 else "normal")

        anchor = tk.W
        tx = shadow_offset // 2 + padx + 10
        if text_align == "center":
            anchor = tk.CENTER
            tx = shadow_offset // 2 + tw // 2
        elif text_align == "right":
            anchor = tk.E
            tx = shadow_offset // 2 + tw - padx - 10

        if self.is_health_tip:
            canvas.create_text(
                tx, shadow_offset // 2 + th // 2, anchor=anchor,
                text=f"{emoji}  {self.message}", font=msg_font, fill=fg_col,
                width=tw - (padx + 10) * 2,
            )
        else:
            canvas.create_text(
                tx, shadow_offset // 2 + pady, anchor=anchor,
                text=f"{emoji}  {self.title}", font=msg_font, fill=fg_col,
            )
            canvas.create_text(
                tx, shadow_offset // 2 + pady + font_size + 8, anchor=anchor,
                text=self.message, font=sub_font, fill="#8892b0",
                width=tw - (padx + 10) * 2,
            )

    def cleanup(self):
        try:
            # Clear active toast from shared status
            status = read_shared_status()
            if status.get("active_toast_pid") == os.getpid():
                status["active_toast_pid"] = None
                status["active_toast_end_time"] = 0.0
                write_shared_status(status)

            with BaseToast._lock:
                if self in BaseToast._active_toasts:
                    BaseToast._active_toasts.remove(self)
            if self.toast_window:
                self.toast_window.destroy()
        except Exception:
            pass
        finally:
            if not self.settings.get("is_preview", False):
                ToastQueue.on_toast_closed(self.parent)
```

---

