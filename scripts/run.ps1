param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev","prod")]
    [string]$env = "dev",
    [string]$port = "8555"
)

$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $script_dir
$env:FLET_WEB_PORT = $port
Write-Host "Starting application in $env mode on port $port"
$main_script = Join-Path $repo "services/movie_song_downloader/main.py"
if ($env -eq "dev") {
    Write-Host "Launching development server..."
    Start-Process -NoNewWindow -FilePath python -ArgumentList "$main_script"
    Start-Sleep -Seconds 4
    Start-Process "http://127.0.0.1:$port"
} else {
    Write-Host "Launching production server..."
    Start-Process -NoNewWindow -FilePath python -ArgumentList "$main_script --env prod"
    Write-Host "Application started."
}
