@echo off
title AeroHub - Install Dependencies
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║        AeroHub Utilities Suite Setup         ║
echo  ╚══════════════════════════════════════════════╝
echo.

echo  [1/2] Installing Python dependencies...
echo.
pip install -r requirements.txt
echo.

echo  [2/2] Creating directory structure...
if not exist "clipboard_manager\exports" mkdir "clipboard_manager\exports"
if not exist "health_app" mkdir "health_app"
if not exist "media_control" mkdir "media_control"
if not exist "battery_monitor" mkdir "battery_monitor"
if not exist "temp_monitor" mkdir "temp_monitor"
if not exist "touch_toggle" mkdir "touch_toggle"
if not exist "aerohub" mkdir "aerohub"

echo.
echo  ✓ Installation complete!
echo.
echo  To start AeroHub, run:
echo    python aerohub\aerohub.py
echo.
echo  Or run individual utilities:
echo    python clipboard_manager\clipboard_manager.py
echo    python health_app\health_app.py
echo    python media_control\media_control.py
echo    python battery_monitor\battery_monitor.py
echo    python temp_monitor\temp_monitor.py
echo    python touch_toggle\touch_toggle.py
echo.
pause
