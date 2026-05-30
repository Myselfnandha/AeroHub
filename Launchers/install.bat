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
if not exist "aerohub" mkdir "aerohub"
if not exist "services\clipboard_manager\exports" mkdir "services\clipboard_manager\exports"
if not exist "services\health_app" mkdir "services\health_app"
if not exist "services\media_control" mkdir "services\media_control"
if not exist "services\tg_fdm_proxy" mkdir "services\tg_fdm_proxy"
if not exist "toggles\battery_monitor" mkdir "toggles\battery_monitor"
if not exist "toggles\temp_monitor" mkdir "toggles\temp_monitor"
if not exist "toggles\touch_toggle" mkdir "toggles\touch_toggle"
if not exist "tools" mkdir "tools"

echo.
echo  ✓ Installation complete!
echo.
echo  To start AeroHub, run:
echo    run_aerohub.bat
echo.
echo  Or run individual utilities directly:
echo    python services\clipboard_manager\clipboard_manager.py
echo    python services\health_app\health_app.py
echo    python services\media_control\media_control.py
echo    python services\tg_fdm_proxy\tg_fdm_proxy.py
echo    python toggles\battery_monitor\battery_monitor.py
echo    python toggles\temp_monitor\temp_monitor.py
echo    python toggles\touch_toggle\touch_toggle.py
echo.
pause
