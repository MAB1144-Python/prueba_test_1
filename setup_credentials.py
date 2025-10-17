#!/usr/bin/env python3
"""
Script para generar credenciales de Google de ejemplo
SOLO PARA DESARROLLO/TESTING LOCAL
"""

import json
import os

def create_example_credentials():
    """Crea un archivo de credenciales de ejemplo"""
    
    # Estructura de credenciales de ejemplo
    credentials = {
        "type": "service_account",
        "project_id": "website-evaluator-demo",
        "private_key_id": "example123456789abcdef",
        "private_key": "-----BEGIN PRIVATE KEY-----\nEXAMPLE_PRIVATE_KEY_CONTENT_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "website-evaluator@website-evaluator-demo.iam.gserviceaccount.com",
        "client_id": "123456789012345678901",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/website-evaluator%40website-evaluator-demo.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    # Crear directorio si no existe
    credentials_dir = "credentials"
    if not os.path.exists(credentials_dir):
        os.makedirs(credentials_dir)
    
    # Guardar archivo de ejemplo
    example_file = os.path.join(credentials_dir, "google-credentials.json")
    with open(example_file, 'w', encoding='utf-8') as f:
        json.dump(credentials, f, indent=2)
    
    print(f"✅ Archivo de ejemplo creado: {example_file}")
    print("\n📋 INSTRUCCIONES:")
    print("1. Ve a https://console.cloud.google.com/")
    print("2. Crea un nuevo proyecto")
    print("3. Habilita Google Drive API y Google Sheets API")
    print("4. Crea un Service Account")
    print("5. Descarga las credenciales reales en formato JSON")
    print("6. Renombra el archivo descargado a 'google-credentials.json'")
    print("7. Colócalo en la carpeta 'credentials/'")
    print("\n⚠️  IMPORTANTE:")
    print("- El archivo de ejemplo NO FUNCIONARÁ para conectar con Google")
    print("- Necesitas credenciales reales de Google Cloud Console")
    print("- NUNCA subas credenciales reales a repositorios públicos")

if __name__ == "__main__":
    create_example_credentials()