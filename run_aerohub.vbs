Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\NANDHA A\Desktop\UTILITIES"
WshShell.Run """C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\pythonw.exe"" ""C:\Users\NANDHA A\Desktop\UTILITIES\aerohub\aerohub.py"" --no-elevate", 0, False
