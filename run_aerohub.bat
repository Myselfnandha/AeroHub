@echo off
cd /d "%~dp0"
start "" /B pythonw aerohub\aerohub.py --no-elevate
exit
