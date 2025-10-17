#!/usr/bin/env python3
"""
Script para verificar las credenciales de Google Drive
"""

import os
import json

def check_credentials():
    """Verifica que las credenciales estén configuradas correctamente"""
    
    print("🔍 Verificando configuración de credenciales...")
    
    # Verificar archivo .env
    env_path = '.env'
    print(f"\n📁 Verificando archivo .env: {env_path}")
    if os.path.exists(env_path):
        print("✅ Archivo .env encontrado")
        with open(env_path, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                print("✅ OPENAI_API_KEY configurado")
            if 'GOOGLE_APPLICATION_CREDENTIALS' in content:
                print("✅ GOOGLE_APPLICATION_CREDENTIALS configurado")
    else:
        print("❌ Archivo .env no encontrado")
    
    # Verificar credenciales de Google
    google_creds_path = 'credentials/google-credentials.json'
    print(f"\n📁 Verificando credenciales de Google: {google_creds_path}")
    if os.path.exists(google_creds_path):
        print("✅ Archivo de credenciales de Google encontrado")
        try:
            with open(google_creds_path, 'r') as f:
                creds = json.load(f)
                if 'type' in creds and creds['type'] == 'service_account':
                    print("✅ Credenciales de Service Account válidas")
                    print(f"   - Project ID: {creds.get('project_id', 'No encontrado')}")
                    print(f"   - Client Email: {creds.get('client_email', 'No encontrado')}")
                else:
                    print("❌ Formato de credenciales incorrecto")
                    print("   Debe ser un archivo de Service Account, no OAuth")
        except Exception as e:
            print(f"❌ Error leyendo credenciales: {e}")
    else:
        print("❌ Archivo de credenciales de Google no encontrado")
        print("   Debes colocar tu archivo de credenciales en:")
        print("   credentials/google-credentials.json")
    
    # Verificar directorio credentials
    creds_dir = 'credentials'
    print(f"\n📁 Contenido del directorio {creds_dir}:")
    if os.path.exists(creds_dir):
        files = os.listdir(creds_dir)
        for file in files:
            file_path = os.path.join(creds_dir, file)
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
            print(f"   - {file} ({size} bytes)")
    else:
        print("❌ Directorio credentials no existe")
    
    print("\n" + "="*50)
    print("📋 RESUMEN:")
    print("="*50)
    
    if os.path.exists(google_creds_path):
        try:
            with open(google_creds_path, 'r') as f:
                creds = json.load(f)
                if creds.get('type') == 'service_account':
                    print("✅ Google Drive debería funcionar correctamente")
                else:
                    print("❌ Necesitas credenciales de Service Account")
        except:
            print("❌ Archivo de credenciales corrupto")
    else:
        print("❌ Falta archivo de credenciales de Google")
        print("   1. Ve a https://console.cloud.google.com/")
        print("   2. Crea un Service Account")
        print("   3. Descarga el archivo JSON")
        print("   4. Guárdalo como credentials/google-credentials.json")

if __name__ == "__main__":
    check_credentials()