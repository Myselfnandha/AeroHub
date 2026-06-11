param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev","prod")]
    [string]$env = "dev",
    [string]$port = "8555"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = $port
Write-Host "Starting application in $env mode on port $port"
if ($env -eq "dev") {
    Write-Host "Launching development server..."
    Start-Process -NoNewWindow -FilePath python -ArgumentList "services/movie_song_downloader/main.py"
    Start-Sleep -Seconds 4
    Start-Process "http://127.0.0.1:$port"
} else {
    Write-Host "Launching production server..."
    Start-Process -NoNewWindow -FilePath python -ArgumentList "services/movie_song_downloader/main.py --env prod"
    Write-Host "Application started."
}
