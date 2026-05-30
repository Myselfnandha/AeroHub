@echo off
title AeroHub Silent Elevated Startup Setup
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo Administrative permissions confirmed.
) else (
    echo Please right-click this file and select "Run as administrator".
    pause
    exit /b
)

set TASKNAME=AeroHub_ElevatedStartup
set VBS_PATH=C:\Users\NANDHA A\Desktop\UTILITIES\run_aerohub.vbs

echo Removing old scheduled task if exists...
schtasks /delete /tn "%TASKNAME%" /f >nul 2>&1

echo Creating new elevated logon scheduled task...
:: Create the task in powershell to ensure battery restrictions are disabled
powershell -NoProfile -Command "$arg = [char]34 + '%VBS_PATH%' + [char]34; $action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument $arg; $trigger = New-ScheduledTaskTrigger -AtLogOn; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0; $principal = New-ScheduledTaskPrincipal -UserId '%USERNAME%' -LogonType Interactive -RunLevel Highest; $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal; Register-ScheduledTask -TaskName '%TASKNAME%' -InputObject $task -Force"

if %errorLevel% == 0 (
    echo.
    echo ========================================================
    echo SUCCESS: AeroHub is now set to start silently as Admin!
    echo ========================================================
    echo Starting AeroHub now...
    schtasks /run /tn "%TASKNAME%"
    echo.
    echo You can close this window now. Touch toggle will now work silently!
) else (
    echo.
    echo FAILED to create scheduled task.
)
pause
exit
