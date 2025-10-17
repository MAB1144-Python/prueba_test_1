#!/usr/bin/env python3
"""
Setup Script para Website Design Evaluator
Instala dependencias y configura el entorno
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el progreso"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def install_chrome_driver():
    """Instala ChromeDriver si no está disponible"""
    print("🔍 Verificando ChromeDriver...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        ChromeDriverManager().install()
        print("✅ ChromeDriver configurado correctamente")
        return True
    except Exception as e:
        print(f"⚠️  Advertencia: Error configurando ChromeDriver: {e}")
        print("   Nota: Se intentará configurar automáticamente al ejecutar")
        return True

def create_directories():
    """Crea directorios necesarios"""
    directories = [
        'screenshots',
        'reports', 
        'credentials',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Directorio creado/verificado: {directory}")
    
    return True

def setup_environment():
    """Configura el archivo de entorno"""
    env_file = ".env"
    env_example = ".env.example"
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print(f"📝 Archivo .env creado desde {env_example}")
        print("   ⚠️  IMPORTANTE: Edita .env con tus credenciales reales")
        return True
    elif os.path.exists(env_file):
        print("✅ Archivo .env ya existe")
        return True
    else:
        print("⚠️  Advertencia: No se encontró .env.example")
        return False

def create_credentials_readme():
    """Crea README para credenciales"""
    credentials_readme = """# Configuración de Credenciales

## Google Drive y Sheets
1. Ve a Google Cloud Console (https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs de Google Drive y Google Sheets
4. Crea credenciales de cuenta de servicio
5. Descarga el archivo JSON y guárdalo como:
   - `google_drive_credentials.json` para Google Drive
   - `google_sheets_credentials.json` para Google Sheets

## AWS S3
1. Ve a AWS IAM Console
2. Crea un usuario con acceso programático
3. Asigna política AmazonS3FullAccess
4. Anota Access Key ID y Secret Access Key
5. Configura las variables en .env

## Dropbox
1. Ve a Dropbox App Console (https://www.dropbox.com/developers/apps)
2. Crea una nueva aplicación
3. Genera un Access Token
4. Configura el token en .env

## OpenAI
1. Ve a OpenAI Platform (https://platform.openai.com/)
2. Crea una API Key
3. Configura la key en .env

⚠️ IMPORTANTE: Nunca compartas estos archivos de credenciales públicamente
"""
    
    credentials_path = Path("credentials/README.md")
    with open(credentials_path, 'w', encoding='utf-8') as f:
        f.write(credentials_readme)
    
    print("📖 README de credenciales creado en credentials/README.md")
    return True

def main():
    """Función principal de setup"""
    print("🚀 Configurando Website Design Evaluator...")
    print("="*50)
    
    # Verificar Python
    if not check_python_version():
        return 1
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias...")
    if not run_command("pip install -r requirements.txt", "Instalación de dependencias"):
        print("⚠️  Algunas dependencias pueden haber fallado. Continúa con la configuración...")
    
    # Crear directorios
    print("\n📁 Creando estructura de directorios...")
    create_directories()
    
    # Configurar entorno
    print("\n⚙️  Configurando entorno...")
    setup_environment()
    
    # Instalar ChromeDriver
    print("\n🌐 Configurando ChromeDriver...")
    install_chrome_driver()
    
    # Crear README de credenciales
    print("\n📋 Creando documentación...")
    create_credentials_readme()
    
    print("\n" + "="*50)
    print("✅ Configuración completada!")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Edita el archivo .env con tus credenciales")
    print("2. Configura las credenciales según credentials/README.md")
    print("3. Ejecuta: python main.py https://ejemplo.com")
    print("\n💡 EJEMPLOS DE USO:")
    print("   python main.py https://www.google.com")
    print("   python main.py --batch example_urls.txt")
    print("   python main.py https://ejemplo.com --no-cloud --no-sheets")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())