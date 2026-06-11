# run_docker.ps1 — build and run docker-compose for local dev
Write-Host "Building and starting docker-compose stack (web:3000)"
docker-compose build --pull
docker-compose up -d
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:3000"
Write-Host "Container started. Run 'docker-compose logs -f' to follow logs."