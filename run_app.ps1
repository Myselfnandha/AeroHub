$env:FLET_WEB_PORT="8555"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Movie Song Downloader - Reflex Launcher (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "1. Run in Production Mode (Recommended - Prevents Windows socket reload bugs)"
Write-Host "2. Run in Development Mode (With Auto-Reload)"
Write-Host "========================================================"
$mode = Read-Host "Choose run mode (1 or 2, default is 1)"

if ($mode -eq "2") {
    Write-Host "Starting in Development Mode..." -ForegroundColor Yellow
    python services/movie_song_downloader/main.py
} else {
    Write-Host "Starting in Production Mode..." -ForegroundColor Green
    python services/movie_song_downloader/main.py --env prod
}
