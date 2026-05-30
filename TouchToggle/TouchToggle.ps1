#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

$logPath = "c:\Users\NANDHA A\Desktop\UTILITIES\Logs\touch_toggle_run.log"
"--- Run at $(Get-Date) ---" | Out-File $logPath -Append

try {
    $device = Get-PnpDevice -Class 'HIDClass' | Where-Object { $_.FriendlyName -match 'touch screen' } | Select-Object -First 1
    if (-not $device) {
        "  [ERROR] No HID-compliant touch screen device found!" | Out-File $logPath -Append
        exit 1
    }

    $instanceId = $device.InstanceId
    $currentStatus = $device.Status

    "Device: $($device.FriendlyName)" | Out-File $logPath -Append
    "ID: $instanceId" | Out-File $logPath -Append
    "Status: $currentStatus" | Out-File $logPath -Append

    if ($currentStatus -eq 'OK') {
        "Attempting to disable..." | Out-File $logPath -Append
        Disable-PnpDevice -InstanceId "$instanceId" -Confirm:$false
        "Disabled successfully." | Out-File $logPath -Append
    } else {
        "Attempting to enable..." | Out-File $logPath -Append
        Enable-PnpDevice -InstanceId "$instanceId" -Confirm:$false
        "Enabled successfully." | Out-File $logPath -Append
    }
} catch {
    "ERROR: $_" | Out-File $logPath -Append
    "ScriptStackTrace: $($_.ScriptStackTrace)" | Out-File $logPath -Append
    exit 1
}

