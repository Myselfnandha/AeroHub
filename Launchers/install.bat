@echo off
title AeroHub - Install Dependencies
echo.
echo  [36m╔══════════════════════════════════════════════╗[0m
echo  [36m║        AeroHub Utilities Suite Setup         ║[0m
echo  [36m╚══════════════════════════════════════════════╝[0m
echo.

echo  [33m[1/2][0m Installing Python dependencies...
echo.
pip install -r requirements.txt
echo.

echo  [33m[2/2][0m Creating directory structure...
if not exist "Logs" mkdir "Logs"
if not exist "services\clipboard_manager\exports" mkdir "services\clipboard_manager\exports"
if not exist "services\health_app\resources\ambient" mkdir "services\health_app\resources\ambient"
if not exist "toggles\battery_monitor\sounds" mkdir "toggles\battery_monitor\sounds"
if not exist "services\media_control\assets" mkdir "services\media_control\assets"

echo.
echo  [32m✓ Installation complete![0m
echo.
echo  To start AeroHub, run:
echo    [36mLaunchers\run_aerohub.bat[0m
echo.
echo  Or run individual utilities directly:
echo    python services\aerohub_core\aerohub.py
echo    python services\clipboard_manager\clipboard_manager.py
echo    python services\health_app\health_app.py
echo    python services\media_control\media_control.py
echo    python toggles\battery_monitor\battery_monitor.py
echo    python toggles\temp_monitor\temp_monitor.py
echo    python toggles\touch_toggle\touch_toggle.py
echo    python services\tg_fdm_proxy\TgFdmProxy\tg_fdm_proxy.py
echo    python tools\taskbar_scroll\taskbar_scroll.py
echo.
pause
