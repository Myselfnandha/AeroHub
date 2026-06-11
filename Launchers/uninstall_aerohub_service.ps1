param(
    [string]$TaskName = "AeroHub Core"
)

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed scheduled task: $TaskName"
} catch {
    Write-Warning "Could not remove task. It may not exist: $_"
}
