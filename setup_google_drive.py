#!/usr/bin/env python3
"""
Script para configurar Google Drive compartido
"""

def setup_google_drive_instructions():
    """Muestra instrucciones para configurar Google Drive"""
    
    print("🔧 CONFIGURACIÓN DE GOOGLE DRIVE")
    print("=" * 50)
    
    print("\n📋 PASOS A SEGUIR (DRIVE COMPARTIDO):")
    print("1. Abre Google Drive: https://drive.google.com")
    print("2. En el panel izquierdo, haz clic en 'Drives compartidos'")
    print("3. Haz clic en '+ Nuevo' (arriba a la izquierda)")
    print("4. Selecciona 'Drive compartido'")
    print("5. Nombre: 'Website Evaluator'")
    print("6. Haz clic en 'Crear'")
    print("7. Dentro del Drive compartido, haz clic en el icono de personas")
    print("8. Agrega este email:")
    print("   📧 website-evaluator-service@website-evaluator-475304.iam.gserviceaccount.com")
    print("9. Permisos: 'Administrador de contenido' o 'Editor'")
    print("10. Haz clic en 'Enviar'")
    
    print("\n⏰ TIEMPO DE ESPERA:")
    print("Después de compartir, espera 1-2 minutos para que se propague")
    
    print("\n🧪 PRUEBA:")
    print("Una vez configurado, ejecuta:")
    print("   python main.py https://www.google.com")
    print("   (sin --no-cloud para probar Google Drive)")
    
    print("\n❌ SI NO QUIERES USAR GOOGLE DRIVE:")
    print("Siempre puedes ejecutar sin servicios en la nube:")
    print("   python main.py https://www.google.com --no-cloud --no-sheets")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    setup_google_drive_instructions()