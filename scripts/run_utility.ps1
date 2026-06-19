param(
    [Parameter(Mandatory=$true)]
    [string]$name,
    [string]$env = "dev",
    [switch]$noGui,
    [int]$port = 8555
)

$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $script_dir
$utilities = @{
    "BatteryMonitor" = "toggles\battery_monitor\battery_monitor.py"
    "TempMonitor" = "toggles\temp_monitor\temp_monitor.py"
    "TouchToggle" = "toggles\touch_toggle\touch_toggle.py"
    "MediaControl" = "services\media_control\media_control.py"
    "ClipboardManager" = "services\clipboard_manager\clipboard_manager.py"
    "HealthApp" = "services\health_app\health_app.py"
    "TaskbarScroll" = "tools\taskbar_scroll\taskbar_scroll.py"
    "TgFdmProxy" = "services\tg_fdm_proxy\TgFdmProxy\tg_fdm_proxy.py"
}

if (-not $utilities.ContainsKey($name)) {
    Write-Error "Unknown utility: $name"
    exit 1
}

$scriptPath = Join-Path $repo $utilities[$name]
if (-not (Test-Path $scriptPath)) {
    Write-Error "Utility script not found: $scriptPath"
    exit 1
}

$env:FLET_WEB_PORT = $port
$env:LOG_DIR = Join-Path $repo "Logs"
$env:ENV = $env

$arguments = @($scriptPath)
if ($name -eq "movie_song_downloader") {
    if ($env -eq "prod") { $arguments += "--env"; $arguments += "prod" }
}

if ($noGui.IsPresent) {
    Write-Host "Starting $name in headless mode..."
} else {
    Write-Host "Starting $name with unified environment."
}

Start-Process -FilePath python -ArgumentList $arguments -NoNewWindow
