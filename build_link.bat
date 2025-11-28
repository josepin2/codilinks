@echo off
setlocal

REM Ir al directorio donde está este script
cd /d "%~dp0"

REM Verificar que el archivo fuente existe
if not exist "link.py" (
    echo [ERROR] No se encontro link.py en "%CD%".
    echo Coloca este .bat en la carpeta del proyecto donde esta link.py.
    exit /b 1
)

REM Ruta de PyInstaller dentro del entorno virtual (si existe)
set "PYI=%CD%\venv\Scripts\pyinstaller.exe"

REM Opcional: usar icono si existe icon.ico en el directorio
set "ICON="
if exist "icon.ico" (
    set "ICON=--icon icon.ico"
)

REM Limpiar compilaciones anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo Compilando link.py a ejecutable standalone (offline) sin consola...

REM Ejecutar PyInstaller (preferentemente desde venv)
if exist "%PYI%" (
    "%PYI%" --onefile --noconfirm --clean --noconsole -n Link %ICON% "link.py"
else (
    pyinstaller --onefile --noconfirm --clean --noconsole -n Link %ICON% "link.py"
)

REM Comprobar resultado
if exist "dist\Link.exe" (
    echo.
    echo [OK] Ejecutable generado: "%CD%\dist\Link.exe"
    echo Abriendo la carpeta dist...
    explorer "dist"
    exit /b 0
)

echo.
echo [ERROR] No se genero el ejecutable. Revisa los mensajes anteriores.
echo Sugerencias:
echo  - Verifica que todas las dependencias esten instaladas en el entorno.
echo  - Prueba ejecutar: venv\Scripts\pip.exe install -r requirements.txt
echo  - Si necesitas ver la consola, quita la opcion --noconsole del comando.
exit /b 1