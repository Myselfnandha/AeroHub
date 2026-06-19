@echo off
set FLET_WEB_PORT=8555
set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%..
echo ========================================================
echo Movie Song Downloader - Reflex Launcher
echo ========================================================
echo 1. Run in Production Mode (Recommended - Prevents Windows socket reload bugs)
echo 2. Run in Development Mode (With Auto-Reload)
echo ========================================================
set /p mode="Choose run mode (1 or 2, default is 1): "

if "%mode%"=="2" (
    echo Starting in Development Mode...
    python "%REPO_ROOT%\services\movie_song_downloader\main.py"
) else (
    echo Starting in Production Mode...
    python "%REPO_ROOT%\services\movie_song_downloader\main.py" --env prod
)
pause
