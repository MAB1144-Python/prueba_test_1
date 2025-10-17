#!/usr/bin/env python3
"""
Script de diagnóstico para Google Drive
Muestra todas las carpetas que puede ver el Service Account
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def diagnose_google_drive():
    """Diagnostica el acceso a Google Drive"""
    try:
        print("🔍 DIAGNÓSTICO DE GOOGLE DRIVE")
        print("=" * 50)
        
        # Configurar credenciales
        SCOPES = [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
        creds_path = 'credentials/google-credentials.json'
        
        if not os.path.exists(creds_path):
            print("❌ Credenciales no encontradas")
            return
        
        credentials = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES
        )
        
        service = build('drive', 'v3', credentials=credentials)
        
        print(f"✅ Conectado a Google Drive")
        print(f"📧 Service Account: {credentials.service_account_email}")
        
        # Listar todas las carpetas compartidas
        print(f"\n📁 CARPETAS COMPARTIDAS CON EL SERVICE ACCOUNT:")
        print("-" * 50)
        
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and sharedWithMe=true",
            spaces='drive',
            fields='files(id, name, owners, capabilities, permissions)'
        ).execute()
        
        shared_folders = results.get('files', [])
        
        if not shared_folders:
            print("❌ No se encontraron carpetas compartidas")
        else:
            for folder in shared_folders:
                print(f"📂 {folder['name']}")
                print(f"   ID: {folder['id']}")
                
                # Mostrar capacidades
                capabilities = folder.get('capabilities', {})
                can_add = capabilities.get('canAddChildren', False)
                can_edit = capabilities.get('canEdit', False)
                print(f"   Puede añadir archivos: {'✅' if can_add else '❌'}")
                print(f"   Puede editar: {'✅' if can_edit else '❌'}")
                
                # Mostrar propietarios
                owners = folder.get('owners', [])
                if owners:
                    print(f"   Propietario: {owners[0].get('displayName', 'N/A')}")
                
                print()
        
        # También buscar carpetas llamadas "Website Screenshots"
        print(f"\n🔍 BUSCANDO CARPETAS 'Website Screenshots':")
        print("-" * 50)
        
        results = service.files().list(
            q="name='Website Screenshots' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name, capabilities, sharedWithMe)'
        ).execute()
        
        target_folders = results.get('files', [])
        
        if not target_folders:
            print("❌ No se encontraron carpetas 'Website Screenshots'")
            print("\n💡 SOLUCIÓN:")
            print("1. Ve a https://drive.google.com")
            print("2. Crea una carpeta llamada 'Website Screenshots'")
            print("3. Haz clic derecho > Compartir")
            print("4. Agrega: website-evaluator-service@website-evaluator-475304.iam.gserviceaccount.com")
            print("5. Dale permisos de 'Editor'")
        else:
            for folder in target_folders:
                print(f"📂 {folder['name']}")
                print(f"   ID: {folder['id']}")
                
                capabilities = folder.get('capabilities', {})
                can_add = capabilities.get('canAddChildren', False)
                shared = folder.get('sharedWithMe', False)
                
                print(f"   Compartida conmigo: {'✅' if shared else '❌'}")
                print(f"   Puede añadir archivos: {'✅' if can_add else '❌'}")
                
                if can_add:
                    print("   🎉 ¡Esta carpeta debería funcionar!")
                else:
                    print("   ⚠️  Esta carpeta no tiene permisos suficientes")
                print()
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")

if __name__ == "__main__":
    diagnose_google_drive()