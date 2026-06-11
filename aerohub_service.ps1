# aerohub_service.ps1 — helper to install/uninstall AeroHub as a Windows service using NSSM
param(
    [ValidateSet("install","remove")]
    [string]$action = "install",
    [string]$nssmPath = "nssm"
)
$script = Join-Path $PSScriptRoot "services\aerohub_core\aerohub.py"
if (-not (Test-Path $script)) { Write-Error "services\aerohub_core\aerohub.py not found in workspace."; exit 1 }
$python = (Get-Command python).Source
$serviceName = "AeroHub"
if ($action -eq "install") {
    Write-Host "Installing service $serviceName using NSSM ($nssmPath)"
    & $nssmPath install $serviceName $python $script
    & $nssmPath set $serviceName AppStdout "$(Join-Path $PSScriptRoot 'Logs\aerohub.stdout.log')"
    & $nssmPath set $serviceName AppStderr "$(Join-Path $PSScriptRoot 'Logs\aerohub.stderr.log')"
    & $nssmPath start $serviceName
    Write-Host "$serviceName installed and started."
} else {
    Write-Host "Removing service $serviceName"
    & $nssmPath stop $serviceName
    & $nssmPath remove $serviceName confirm
    Write-Host "$serviceName removed."
}