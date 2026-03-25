
Set oShell = CreateObject("WScript.Shell")
Set oFSO = CreateObject("Scripting.FileSystemObject")

appPath = "D:\BancoComunal\app.py"
If Not oFSO.FileExists(appPath) Then
    MsgBox "No se encontró SemilleroComunal en D:\BancoComunal\" & Chr(10) & "Por favor ejecuta INSTALAR.bat primero.", 16, "SemilleroComunal"
    WScript.Quit
End If

' Run Python app silently (no command window)
oShell.Run "python D:\BancoComunal\app.py", 0, False

' Wait a moment for server to start
WScript.Sleep 2000

' Open browser
oShell.Run "http://localhost:5000", 1, False
