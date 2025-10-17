#!/usr/bin/env python3
"""
Script para obtener el ID de una carpeta compartida de Google Drive
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_folder_id():
    """Obtiene el ID de la carpeta compartida"""
    try:
        # Configurar credenciales
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds_path = 'credentials/google-credentials.json'
        
        if not os.path.exists(creds_path):
            print("❌ Credenciales no encontradas")
            return
        
        credentials = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES
        )
        
        service = build('drive', 'v3', credentials=credentials)
        
        # Buscar carpetas compartidas
        print("🔍 Buscando carpetas compartidas...")
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and sharedWithMe=true",
            spaces='drive',
            fields='files(id, name, owners, parents)'
        ).execute()
        
        folders = results.get('files', [])
        
        if not folders:
            print("❌ No se encontraron carpetas compartidas")
            print("\n📋 INSTRUCCIONES:")
            print("1. Ve a Google Drive")
            print("2. Crea una carpeta llamada 'Website Screenshots'")
            print("3. Compártela con:")
            print("   website-evaluator-service@website-evaluator-475304.iam.gserviceaccount.com")
            print("4. Dale permisos de 'Editor'")
        else:
            print("✅ Carpetas compartidas encontradas:")
            for folder in folders:
                print(f"   - Nombre: {folder['name']}")
                print(f"     ID: {folder['id']}")
                print(f"     Propietarios: {[owner.get('displayName', 'N/A') for owner in folder.get('owners', [])]}")
                print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_folder_id()