param(
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = "$port"
Write-Host "Starting movie_song_downloader in DEVELOPMENT mode with hot reload"
Start-Process -NoNewWindow -FilePath python -ArgumentList "movie_song_downloader/main.py"
Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:$port"
