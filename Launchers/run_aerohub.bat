@echo off
cd /d "%~dp0\.."
start "" /B pythonw services\aerohub_core\aerohub.py
exit
