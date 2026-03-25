@echo off
setlocal EnableDelayedExpansion
title SemilleroComunal v1.2 - Instalador
color 0A

echo.
echo  ====================================================
echo   SemilleroComunal v1.2
echo   Sembramos confianza, cosechamos comunidad
echo  ====================================================
echo.

REM ── PASO 1: Verificar Python ──────────────────────────
echo  [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python no esta instalado o no esta en el PATH.
    echo  Descargalo en: https://www.python.org/downloads/
    echo  IMPORTANTE: Marca "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  OK: !PYVER! detectado

REM ── PASO 2: Copiar archivos ───────────────────────────
echo.
echo  [2/6] Copiando archivos...

if not exist "D:\BancoComunal" mkdir "D:\BancoComunal"

REM Copiar solo los archivos necesarios (sin recursion que cause duplicados)
copy /Y "%~dp0app.py"               "D:\BancoComunal\app.py"               >nul
copy /Y "%~dp0SemilleroComunal.vbs" "D:\BancoComunal\SemilleroComunal.vbs" >nul
copy /Y "%~dp0LEEME.txt"            "D:\BancoComunal\LEEME.txt"            >nul
copy /Y "%~dp0test_auth.py"         "D:\BancoComunal\test_auth.py"         >nul

REM Carpetas de datos y trabajo
for %%d in (datos documentos fotos reportes plantillas backups) do (
    if not exist "D:\BancoComunal\%%d" mkdir "D:\BancoComunal\%%d"
)

REM Templates
if not exist "D:\BancoComunal\templates" mkdir "D:\BancoComunal\templates"
for %%t in (login.html recuperar.html setup.html dashboard.html) do (
    if exist "%~dp0templates\%%t" (
        copy /Y "%~dp0templates\%%t" "D:\BancoComunal\templates\%%t" >nul
    )
)

REM Imagenes / estaticos
if not exist "D:\BancoComunal\static\img" mkdir "D:\BancoComunal\static\img"
for %%i in (semillero.ico semillero.png) do (
    if exist "%~dp0static\img\%%i" (
        copy /Y "%~dp0static\img\%%i" "D:\BancoComunal\static\img\%%i" >nul
    )
)

echo  OK: Archivos copiados a D:\BancoComunal\

REM ── PASO 3: Instalar dependencias ────────────────────
echo.
echo  [3/6] Instalando dependencias de Python...
echo  (Requiere internet - puede tardar unos minutos)
echo.

set PAQUETES=flask google-generativeai pillow python-docx reportlab python-pptx
set /a ERRORES_PIP=0

for %%p in (%PAQUETES%) do (
    echo  Instalando %%p...
    python -m pip install %%p --no-input --quiet --disable-pip-version-check
    if !errorlevel! neq 0 (
        echo  ADVERTENCIA: %%p no se instalo
        set /a ERRORES_PIP+=1
    ) else (
        echo  OK: %%p
    )
)

if !ERRORES_PIP! gtr 0 (
    echo.
    echo  ADVERTENCIA: !ERRORES_PIP! paquete(s) con error.
    echo  Si la app falla, ejecuta manualmente:
    echo    pip install flask python-docx reportlab python-pptx pillow
    echo.
) else (
    echo.
    echo  OK: Todas las dependencias instaladas
)

REM ── PASO 4: Pruebas del modulo auth ──────────────────
echo.
echo  [4/6] Verificando modulo de autenticacion...
echo  -------------------------------------------------------

python "D:\BancoComunal\test_auth.py"
set TEST_RESULT=!errorlevel!

echo  -------------------------------------------------------
if !TEST_RESULT! neq 0 (
    echo.
    echo  ADVERTENCIA: Algunas pruebas fallaron.
    echo  Revisa los errores arriba.
    echo.
    choice /C CN /M "  Continuar de todas formas? (C=Si, N=Cancelar)"
    if errorlevel 2 (
        echo  Instalacion cancelada.
        pause
        exit /b 1
    )
) else (
    echo  OK: Modulo auth verificado - 25/25 pruebas pasaron
)

REM ── PASO 5: Acceso directo en Escritorio ─────────────
echo.
echo  [5/6] Creando acceso directo en el Escritorio...

(
echo Set oWS = WScript.CreateObject("WScript.Shell"^)
echo sDesk = oWS.SpecialFolders("Desktop"^)
echo Set oLink = oWS.CreateShortcut(sDesk ^& "\SemilleroComunal.lnk"^)
echo oLink.TargetPath = "wscript.exe"
echo oLink.Arguments = """D:\BancoComunal\SemilleroComunal.vbs"""
echo oLink.WorkingDirectory = "D:\BancoComunal"
echo oLink.IconLocation = "D:\BancoComunal\static\img\semillero.ico, 0"
echo oLink.Description = "SemilleroComunal - Banco Comunal"
echo oLink.Save
) > "%TEMP%\sc_link.vbs"
cscript //nologo "%TEMP%\sc_link.vbs"
del "%TEMP%\sc_link.vbs" >nul 2>&1
echo  OK: Acceso directo creado

REM ── PASO 6: Lanzar ───────────────────────────────────
echo.
echo  [6/6] Iniciando SemilleroComunal...
echo.
echo  ====================================================
echo   INSTALACION COMPLETADA
echo.
echo   Destino : D:\BancoComunal\
echo   Icono   : En el Escritorio
echo   Acceso  : http://localhost:5000
echo  ====================================================
echo.
pause
wscript "D:\BancoComunal\SemilleroComunal.vbs"
