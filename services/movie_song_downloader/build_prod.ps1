param(
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = "$port"
$logdir = Join-Path $root "logs"
if (-not (Test-Path $logdir)) { New-Item -ItemType Directory -Path $logdir | Out-Null }
$timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$logfile = Join-Path $logdir "build_prod_$timestamp.log"

Write-Host "Building movie_song_downloader production bundle..."
Write-Host "Logs: $logfile"

try {
    python -m pip install --upgrade pip | Out-Null
    python -m pip install -r requirements.txt | Out-Null
    python movie_song_downloader/main.py --env prod 2>&1 | Tee-Object -FilePath $logfile
    Write-Host "Production run successful. Packaging artifacts..."
    $archive = Join-Path $logdir "movie_song_downloader-production-$timestamp.zip"
    Compress-Archive -Path "$root\movie_song_downloader\*" -DestinationPath $archive -Force
    Write-Host "Packaged production artifact: $archive"
} catch {
    Write-Error "Build failed: $_"
    exit 1
}
