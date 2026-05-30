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
if not exist "ClipboardManager\exports" mkdir "ClipboardManager\exports"
if not exist "HealthApp\resources\ambient" mkdir "HealthApp\resources\ambient"
if not exist "BatteryMonitor\sounds" mkdir "BatteryMonitor\sounds"
if not exist "MediaControl\assets" mkdir "MediaControl\assets"

echo.
echo  [32m✓ Installation complete![0m
echo.
echo  To start AeroHub, run:
echo    [36mLaunchers\run_aerohub.bat[0m
echo.
echo  Or run individual utilities directly:
echo    python AeroHub_Core\aerohub.py
echo    python ClipboardManager\clipboard_manager.py
echo    python HealthApp\health_app.py
echo    python MediaControl\media_control.py
echo    python BatteryMonitor\battery_monitor.py
echo    python TempMonitor\temp_monitor.py
echo    python TouchToggle\touch_toggle.py
echo    python TgFdmProxy\tg_fdm_proxy.py
echo    python TaskbarScroll\taskbar_scroll.py
echo.
pause
