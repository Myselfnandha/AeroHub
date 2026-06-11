# prod_run.ps1 — start the unified project launcher in production mode
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Starting MovieSongDownloader in production mode..."
Start-Process -NoNewWindow -FilePath powershell -ArgumentList "-File `"$root\run.ps1`" --env prod --port 8555"
