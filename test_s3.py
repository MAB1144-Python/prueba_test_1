#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de AWS S3
"""
import boto3
import os
from dotenv import load_dotenv

def test_s3_connection():
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener configuración
    bucket_name = os.getenv('AWS_S3_BUCKET')
    region = os.getenv('AWS_REGION')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    print("🔧 Configuración de AWS S3:")
    print(f"   Bucket: {bucket_name}")
    print(f"   Region: {region}")
    print(f"   Access Key: {access_key[:8]}..." if access_key else "   Access Key: No configurado")
    print(f"   Secret Key: {'*' * 8}..." if secret_key else "   Secret Key: No configurado")
    print()
    
    try:
        # Crear cliente S3
        s3_client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        # Probar conexión listando buckets
        print("🔍 Probando conexión con AWS S3...")
        response = s3_client.list_buckets()
        print("✅ Conexión exitosa con AWS S3")
        print()
        
        print("📦 Buckets disponibles:")
        for bucket in response['Buckets']:
            print(f"   - {bucket['Name']}")
        print()
        
        # Verificar si nuestro bucket existe
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"✅ El bucket '{bucket_name}' existe y es accesible")
        except Exception as e:
            print(f"❌ Error con el bucket '{bucket_name}': {e}")
            # Intentar crear el bucket
            try:
                if region == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                print(f"✅ Bucket '{bucket_name}' creado exitosamente")
            except Exception as create_error:
                print(f"❌ Error creando el bucket: {create_error}")
        
        # Probar subida de archivo
        print("\n🧪 Probando subida de archivo de prueba...")
        test_content = b"Archivo de prueba para el evaluador de sitios web"
        test_key = "test/test_file.txt"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content,
            ContentType='text/plain'
        )
        
        # Generar URL pública
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{test_key}"
        print(f"✅ Archivo de prueba subido exitosamente")
        print(f"📁 URL: {url}")
        
        # Limpiar archivo de prueba
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        print("🧹 Archivo de prueba eliminado")
        
        print("\n🎉 ¡Configuración de S3 completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verificar las credenciales de AWS")
        print("   2. Verificar los permisos del usuario IAM")
        print("   3. Verificar la región configurada")
        return False

if __name__ == "__main__":
    test_s3_connection()