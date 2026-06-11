@echo off
title AeroHub - Re-register Startup Task
echo.
echo  [36m  AeroHub Startup Task Fix[0m
echo.

:: Check for admin
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo  [32m✓[0m Admin confirmed.
) else (
    echo  [31m✗[0m Need admin. Re-launching elevated...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

:: Derive VBS path from this script's location
set "VBS_PATH=%~dp0run_aerohub.vbs"

echo.
echo  [33m[1/2][0m Removing old task...
schtasks /delete /tn "AeroHub_ElevatedStartup" /f >nul 2>&1
echo  [32m✓[0m Done.

echo.
echo  [33m[2/2][0m Creating task with path: %VBS_PATH%
powershell -NoProfile -Command "$arg = [char]34 + '%VBS_PATH%' + [char]34; $action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument $arg; $trigger = New-ScheduledTaskTrigger -AtLogOn; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0; $principal = New-ScheduledTaskPrincipal -UserId '%USERNAME%' -LogonType Interactive -RunLevel Highest; $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal; Register-ScheduledTask -TaskName 'AeroHub_ElevatedStartup' -InputObject $task -Force"

if %errorLevel% == 0 (
    echo.
    echo  [32m✓ Task registered! AeroHub will auto-start on next login.[0m
    echo.
    echo  Starting AeroHub now...
    schtasks /run /tn "AeroHub_ElevatedStartup"
    echo  [32m✓ AeroHub launched.[0m
) else (
    echo.
    echo  [31m✗ Failed to register task.[0m
)
echo.
pause
