@echo off
title AeroHub - Fix Startup Task
echo.
echo  [36m╔══════════════════════════════════════════════╗[0m
echo  [36m║      AeroHub Startup Fix                    ║[0m
echo  [36m╚══════════════════════════════════════════════╝[0m
echo.

:: Check for admin
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo  [32m✓[0m Administrative permissions confirmed.
) else (
    echo  [31m✗[0m Please right-click this file and select "Run as administrator".
    pause
    exit /b
)

:: Derive VBS path from this script's location
set "VBS_PATH=%~dp0run_aerohub.vbs"

echo.
echo  [33m[1/3][0m Removing broken scheduled task...
schtasks /delete /tn "AeroHub_ElevatedStartup" /f >nul 2>&1
echo  [32m✓[0m Old task removed.

echo.
echo  [33m[2/3][0m Creating fixed scheduled task...
echo        Using: %VBS_PATH%
powershell -NoProfile -Command "$arg = [char]34 + '%VBS_PATH%' + [char]34; $action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument $arg; $trigger = New-ScheduledTaskTrigger -AtLogOn; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0; $principal = New-ScheduledTaskPrincipal -UserId '%USERNAME%' -LogonType Interactive -RunLevel Highest; $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal; Register-ScheduledTask -TaskName 'AeroHub_ElevatedStartup' -InputObject $task -Force"

if %errorLevel% == 0 (
    echo.
    echo  [32m✓[0m Task created successfully!
) else (
    echo.
    echo  [31m✗[0m Failed to create task.
    pause
    exit /b
)

echo.
echo  [33m[3/3][0m Verifying...
schtasks /query /tn "AeroHub_ElevatedStartup" /fo LIST | findstr "Task To Run"
echo.
echo  [32m════════════════════════════════════════════════[0m
echo  [32m  ✓ FIXED! AeroHub will start on next login.  [0m
echo  [32m════════════════════════════════════════════════[0m
echo.
pause
exit
