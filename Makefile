# Makefile — common developer tasks
.PHONY: lint test precommit run-dev run-prod build docker-build service-install service-uninstall

lint:
	flake8 --max-line-length=120 --exclude=.agent,scratch

precommit:
	python -m pip install pre-commit
	pre-commit run --all-files

test:
	python -m py_compile $(shell git ls-files '*.py') && pytest -q

run-dev:
	powershell -File dev_run.ps1

run-prod:
	powershell -File prod_run.ps1

build:
	powershell -File services\movie_song_downloader\build_prod.ps1

docker-build:
	docker build -t moviesongdownloader:latest .

service-install:
	powershell -File Launchers\install_aerohub_service.ps1

service-uninstall:
	powershell -File Launchers\uninstall_aerohub_service.ps1

service-install-touch:
	powershell -File toggles\touch_toggle\install_touch_toggle_service.ps1

service-uninstall-touch:
	powershell -File toggles\touch_toggle\uninstall_touch_toggle_service.ps1
