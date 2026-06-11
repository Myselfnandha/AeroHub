# dev_run.ps1 — start the unified project launcher in development mode
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Starting MovieSongDownloader in development mode..."
Start-Process -NoNewWindow -FilePath powershell -ArgumentList "-File `"$root\run.ps1`" --env dev --port 8555"