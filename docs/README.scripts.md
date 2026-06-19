Scripts and Dev Helpers

This project includes useful scripts and CI for local development, production runs, and containerization.

- `dev_run.ps1` — start the Reflex app in development mode and open the browser.
- `prod_run.ps1` — start Reflex in production mode and log to `logs/`.
- `aerohub_service.ps1` — helper to install/uninstall `AeroHub` as a Windows service using `nssm`.
- `run_docker.ps1` — build and run `docker-compose` and open the app in a browser.
- `Dockerfile` / `docker-compose.yml` — containerize the app for consistent environments.
- `.github/workflows/ci.yml` — CI pipeline for linting, compiling, and running tests.
- `.pre-commit-config.yaml` — pre-commit hooks configuration (black, isort, flake8).

Quick usage examples:

PowerShell (dev):

```powershell
.\dev_run.ps1
```

PowerShell (prod):

```powershell
.\prod_run.ps1
```

Docker:

```powershell
.\run_docker.ps1
```

CI is configured to run on pushes and PRs to `main`.
