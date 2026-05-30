$events = Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Application Error'} -MaxEvents 5 -ErrorAction SilentlyContinue
if ($events) {
    $events | Where-Object { $_.Message -match 'explorer.exe' } | Select-Object TimeCreated, Message | Format-List
} else {
    Write-Output "No application errors found."
}
