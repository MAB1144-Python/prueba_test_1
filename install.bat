@echo off
REM Instalador automático para Website Design Evaluator en Windows

echo ==========================================
echo  Website Design Evaluator - Instalador  
echo ==========================================

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo Python detectado correctamente

REM Verificar pip
echo Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no esta disponible
    pause
    exit /b 1
)

REM Crear entorno virtual (opcional)
echo.
set /p VENV="¿Crear entorno virtual? (s/n): "
if /i "%VENV%"=="s" (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Entorno virtual activado
)

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ADVERTENCIA: Algunas dependencias pueden haber fallado
    echo Continua con la instalacion...
)

REM Ejecutar setup
echo.
echo Ejecutando configuracion...
python setup.py

REM Mensaje final
echo.
echo ==========================================
echo        Instalacion completada!
echo ==========================================
echo.
echo PROXIMOS PASOS:
echo 1. Edita el archivo .env con tus credenciales
echo 2. Configura credenciales segun credentials/README.md  
echo 3. Ejecuta: python main.py https://ejemplo.com
echo.
echo EJEMPLOS:
echo   python main.py https://www.google.com
echo   python main.py --batch example_urls.txt
echo   python demo.py  (para ver demostracion)
echo.
echo Para activar el entorno virtual en futuras sesiones:
if exist venv (
    echo   call venv\Scripts\activate.bat
)
echo.
pause