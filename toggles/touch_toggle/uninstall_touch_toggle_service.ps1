param(
    [string]$TaskName = "TouchToggle Service"
)

try {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Uninstalled scheduled task: $TaskName"
    } else {
        Write-Warning "Scheduled task '$TaskName' not found."
    }
} catch {
    Write-Error "Failed to uninstall TouchToggle service: $_"
    exit 1
}
