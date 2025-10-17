#!/bin/bash
# Instalador automático para Website Design Evaluator en Linux/Mac

echo "=========================================="
echo " Website Design Evaluator - Instalador"  
echo "=========================================="

# Verificar Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python no está instalado"
        echo "Instala Python 3.8+ desde https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python detectado: $($PYTHON_CMD --version)"

# Verificar pip
echo "Verificando pip..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "ERROR: pip no está disponible"
    exit 1
fi

# Crear entorno virtual (opcional)
echo
read -p "¿Crear entorno virtual? (s/n): " venv_choice
if [[ $venv_choice == "s" || $venv_choice == "S" ]]; then
    echo "Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    echo "Entorno virtual activado"
    PYTHON_CMD="python"  # Usar python del venv
fi

# Instalar dependencias
echo
echo "Instalando dependencias..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ADVERTENCIA: Algunas dependencias pueden haber fallado"
    echo "Continúa con la instalación..."
fi

# Ejecutar setup
echo
echo "Ejecutando configuración..."
$PYTHON_CMD setup.py

# Mensaje final
echo
echo "=========================================="
echo "        Instalación completada!"
echo "=========================================="
echo
echo "PRÓXIMOS PASOS:"
echo "1. Edita el archivo .env con tus credenciales"
echo "2. Configura credenciales según credentials/README.md"  
echo "3. Ejecuta: $PYTHON_CMD main.py https://ejemplo.com"
echo
echo "EJEMPLOS:"
echo "  $PYTHON_CMD main.py https://www.google.com"
echo "  $PYTHON_CMD main.py --batch example_urls.txt"
echo "  $PYTHON_CMD demo.py  (para ver demostración)"
echo

if [ -d "venv" ]; then
    echo "Para activar el entorno virtual en futuras sesiones:"
    echo "  source venv/bin/activate"
fi

echo