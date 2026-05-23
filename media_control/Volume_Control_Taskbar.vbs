Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'Volume_Control_Taskbar.exe'")

If colProcesses.Count = 0 Then
    Set WshShell = CreateObject("WScript.Shell")
    Set fso = CreateObject("Scripting.FileSystemObject")
    scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
    parent1 = fso.GetParentFolderName(scriptDir)
    parent2 = fso.GetParentFolderName(parent1)
    exePath = fso.BuildPath(fso.BuildPath(parent2, "legacy"), "Volume_Control_Taskbar.exe")
    WshShell.Run """" & exePath & """", 0, False
End If
