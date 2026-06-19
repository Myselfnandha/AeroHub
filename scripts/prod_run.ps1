# prod_run.ps1 — start the unified project launcher in production mode
$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
Start-Process -NoNewWindow -FilePath powershell -ArgumentList "-File `"$script_dir\run.ps1`" --env prod --port 8555"
