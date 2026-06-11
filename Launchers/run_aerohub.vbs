Set FSO = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

' Derive paths from this script's location
LaunchersDir = FSO.GetParentFolderName(WScript.ScriptFullName)
UtilitiesDir = FSO.GetParentFolderName(LaunchersDir)

' Find pythonw.exe — prefer the one next to current python
PythonwExe = ""
' Try common locations
Dim candidates
candidates = Array( _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python313\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python311\pythonw.exe" _
)

For Each p In candidates
    If FSO.FileExists(p) Then
        PythonwExe = p
        Exit For
    End If
Next

' Fallback: just use pythonw from PATH
If PythonwExe = "" Then PythonwExe = "pythonw.exe"

AeroHubScript = UtilitiesDir & "\services\aerohub_core\aerohub.py"

WshShell.CurrentDirectory = UtilitiesDir
WshShell.Run """" & PythonwExe & """ """ & AeroHubScript & """", 0, False
