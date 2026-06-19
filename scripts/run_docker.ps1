# run_docker.ps1 — build and run docker-compose for local dev
$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $script_dir
Set-Location $repo
Write-Host "Building and starting docker-compose stack (web:3000)"
docker-compose -f config/docker-compose.yml build --pull
docker-compose -f config/docker-compose.yml up -d
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:3000"
Write-Host "Container started. Run 'docker-compose -f config/docker-compose.yml logs -f' to follow logs."
