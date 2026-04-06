@echo off
REM ====================================================================
REM SEMILLERO COMUNAL - Iniciador Mejorado
REM ====================================================================

TITLE Semillero Comunal - Iniciando...

REM Cambiar al directorio del script
cd /d "%~dp0"

echo.
echo ========================================================================
echo   SEMILLERO COMUNAL - Sistema de Gestion de Banco Comunal
echo ========================================================================
echo.
echo   Iniciando aplicacion...
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python no esta instalado o no esta en el PATH
    echo.
    echo   Por favor instala Python desde https://www.python.org/downloads/
    echo   Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

REM Verificar que app.py existe
if not exist "app.py" (
    echo   [ERROR] No se encuentra el archivo app.py
    echo   Asegurate de estar en el directorio correcto
    echo.
    pause
    exit /b 1
)

REM Crear directorios necesarios si no existen
if not exist "datos" mkdir datos
if not exist "fotos" mkdir fotos
if not exist "documentos" mkdir documentos
if not exist "reportes" mkdir reportes
if not exist "plantillas" mkdir plantillas
if not exist "backups" mkdir backups

REM Verificar/instalar dependencias
echo   Verificando dependencias...
python -c "import flask, bcrypt, faker" >nul 2>&1
if errorlevel 1 (
    echo.
    echo   [AVISO] Algunas dependencias no estan instaladas
    echo   Instalando dependencias necesarias...
    echo.
    pip install flask bcrypt faker python-docx reportlab python-pptx pillow
    if errorlevel 1 (
        echo.
        echo   [ERROR] No se pudieron instalar las dependencias
        echo   Intenta manualmente: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Iniciar la aplicación
echo.
echo   Iniciando Semillero Comunal...
echo   La aplicacion se abrira automaticamente en tu navegador
echo.
echo   Para detener el servidor, presiona Ctrl+C
echo.
echo ========================================================================
echo.

python app.py

REM Si python sale con error
if errorlevel 1 (
    echo.
    echo   [ERROR] La aplicacion se cerro inesperadamente
    echo   Revisa los logs en datos/app.log para mas informacion
    echo.
    pause
)
