param(
    [string]$TaskName = "AeroHub Core",
    [string]$PythonExecutable = "python"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $root "..\services\aerohub_core\aerohub.py"
$action = New-ScheduledTaskAction -Execute $PythonExecutable -Argument "`"$scriptPath`" --service"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    Write-Host "Installed scheduled task: $TaskName"
} catch {
    Write-Error "Failed to install service task: $_"
    exit 1
}
