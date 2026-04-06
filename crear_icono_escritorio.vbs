Option Explicit

' ========================================================================
' SEMILLERO COMUNAL - Creador de Acceso Directo en Escritorio
' ========================================================================
' Este script crea un acceso directo en el escritorio del usuario
' que inicia directamente la aplicación Semillero Comunal
' ========================================================================

Dim objShell, objFSO, strDesktop, objShortcut, strScriptPath, strBatchPath

' Crear objetos
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obtener ruta del escritorio
strDesktop = objShell.SpecialFolders("Desktop")

' Obtener ruta del script actual
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Ruta al archivo .bat
strBatchPath = objFSO.BuildPath(strScriptPath, "INICIAR_SEMILLERO.bat")

' Verificar que el archivo .bat existe
If Not objFSO.FileExists(strBatchPath) Then
    MsgBox "No se encuentra el archivo INICIAR_SEMILLERO.bat" & vbCrLf & _
           "Ruta esperada: " & strBatchPath, vbCritical, "Error - Semillero Comunal"
    WScript.Quit 1
End If

' Crear el acceso directo
Set objShortcut = objShell.CreateShortcut(strDesktop & "\Semillero Comunal.lnk")

With objShortcut
    .TargetPath = strBatchPath
    .WorkingDirectory = strScriptPath
    .Description = "Sistema de Gestión de Banco Comunal"
    .WindowStyle = 1  ' Normal window
    
    ' Intentar usar el icono si existe
    Dim strIconPath
    strIconPath = objFSO.BuildPath(strScriptPath, "static\img\logo.ico")
    If objFSO.FileExists(strIconPath) Then
        .IconLocation = strIconPath & ",0"
    Else
        ' Usar icono del sistema si no existe el personalizado
        .IconLocation = "%SystemRoot%\System32\shell32.dll,165"
    End If
    
    .Save
End With

' Mensaje de éxito
MsgBox "¡Acceso directo creado exitosamente!" & vbCrLf & vbCrLf & _
       "Se ha creado el icono 'Semillero Comunal' en tu escritorio." & vbCrLf & _
       "Haz doble clic en él para iniciar la aplicación.", _
       vbInformation, "Semillero Comunal"

' Limpiar objetos
Set objShortcut = Nothing
Set objFSO = Nothing
Set objShell = Nothing

WScript.Quit 0
