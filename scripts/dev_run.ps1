# dev_run.ps1 — start the unified project launcher in development mode
$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
Start-Process -NoNewWindow -FilePath powershell -ArgumentList "-File `"$script_dir\run.ps1`" --env dev --port 8555"
