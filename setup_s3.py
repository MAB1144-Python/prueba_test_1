#!/usr/bin/env python3
"""
Script de configuración para AWS S3
Guía para configurar las credenciales y el bucket de S3
"""
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_aws_credentials():
    """Verifica si las credenciales de AWS están configuradas"""
    try:
        # Intentar crear un cliente S3
        s3_client = boto3.client('s3')
        # Intentar listar buckets para verificar credenciales
        s3_client.list_buckets()
        logger.info("✅ Credenciales de AWS configuradas correctamente")
        return True
    except NoCredentialsError:
        logger.error("❌ No se encontraron credenciales de AWS")
        return False
    except ClientError as e:
        logger.error(f"❌ Error con las credenciales de AWS: {e}")
        return False

def create_bucket_if_not_exists(bucket_name, region='us-east-1'):
    """Crea un bucket S3 si no existe"""
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # Verificar si el bucket existe
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"✅ El bucket '{bucket_name}' ya existe")
            return True
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                # El bucket no existe, crearlo
                try:
                    if region == 'us-east-1':
                        s3_client.create_bucket(Bucket=bucket_name)
                    else:
                        s3_client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': region}
                        )
                    logger.info(f"✅ Bucket '{bucket_name}' creado exitosamente")
                    return True
                except ClientError as create_error:
                    logger.error(f"❌ Error creando el bucket: {create_error}")
                    return False
            else:
                logger.error(f"❌ Error verificando el bucket: {e}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error general: {e}")
        return False

def setup_bucket_policy(bucket_name):
    """Configura la política del bucket para permitir acceso público a archivos específicos"""
    try:
        s3_client = boto3.client('s3')
        
        # Política básica que permite acceso público de lectura
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/public/*"
                }
            ]
        }
        
        import json
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        logger.info(f"✅ Política del bucket '{bucket_name}' configurada")
        return True
        
    except ClientError as e:
        logger.error(f"❌ Error configurando la política del bucket: {e}")
        return False

def test_s3_operations(bucket_name):
    """Prueba las operaciones básicas de S3"""
    try:
        s3_client = boto3.client('s3')
        
        # Crear un archivo de prueba
        test_content = b"Archivo de prueba para el evaluador de sitios web"
        test_key = "test/test_file.txt"
        
        # Subir archivo
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content,
            ContentType='text/plain'
        )
        logger.info(f"✅ Archivo de prueba subido a s3://{bucket_name}/{test_key}")
        
        # Generar URL pública
        url = f"https://{bucket_name}.s3.amazonaws.com/{test_key}"
        logger.info(f"📁 URL del archivo: {url}")
        
        # Limpiar archivo de prueba
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        logger.info("🧹 Archivo de prueba eliminado")
        
        return True
        
    except ClientError as e:
        logger.error(f"❌ Error en las pruebas de S3: {e}")
        return False

def update_env_file():
    """Actualiza el archivo .env con las variables de S3"""
    env_path = '.env'
    
    # Leer archivo .env existente si existe
    env_vars = {}
    if os.path.exists(env_path):
        load_dotenv(env_path)
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    # Solicitar configuración de S3
    print("\n🔧 Configuración de AWS S3")
    print("=" * 50)
    
    bucket_name = input(f"Nombre del bucket S3 [{env_vars.get('AWS_S3_BUCKET', 'website-evaluator-bucket')}]: ").strip()
    if not bucket_name:
        bucket_name = env_vars.get('AWS_S3_BUCKET', 'website-evaluator-bucket')
    
    region = input(f"Región de AWS [{env_vars.get('AWS_REGION', 'us-east-1')}]: ").strip()
    if not region:
        region = env_vars.get('AWS_REGION', 'us-east-1')
    
    # Actualizar variables
    env_vars['AWS_S3_BUCKET'] = bucket_name
    env_vars['AWS_REGION'] = region
    
    # Guardar archivo .env
    with open(env_path, 'w') as f:
        f.write("# Configuración del Evaluador de Sitios Web\n\n")
        f.write("# OpenAI API\n")
        f.write(f"OPENAI_API_KEY={env_vars.get('OPENAI_API_KEY', 'tu_api_key_aqui')}\n\n")
        f.write("# AWS S3 Configuration\n")
        f.write(f"AWS_S3_BUCKET={bucket_name}\n")
        f.write(f"AWS_REGION={region}\n\n")
        f.write("# AWS Credentials (opcional si usas AWS CLI configurado)\n")
        f.write(f"# AWS_ACCESS_KEY_ID=tu_access_key_aqui\n")
        f.write(f"# AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui\n")
    
    logger.info(f"✅ Archivo .env actualizado con configuración de S3")
    return bucket_name, region

def main():
    """Función principal de configuración"""
    print("🚀 Configurador de AWS S3 para el Evaluador de Sitios Web")
    print("=" * 60)
    
    # Paso 1: Configurar variables de entorno
    bucket_name, region = update_env_file()
    
    # Recargar variables de entorno
    load_dotenv()
    
    print(f"\n📋 Configuración:")
    print(f"   Bucket: {bucket_name}")
    print(f"   Región: {region}")
    
    # Paso 2: Verificar credenciales
    print(f"\n🔐 Verificando credenciales de AWS...")
    if not check_aws_credentials():
        print("\n❌ Error: No se pudieron verificar las credenciales de AWS")
        print("\n💡 Soluciones:")
        print("   1. Configurar AWS CLI: aws configure")
        print("   2. Configurar variables de entorno:")
        print("      - AWS_ACCESS_KEY_ID")
        print("      - AWS_SECRET_ACCESS_KEY")
        print("   3. Usar perfil de IAM si estás en EC2")
        return False
    
    # Paso 3: Crear bucket
    print(f"\n📦 Creando/verificando bucket S3...")
    if not create_bucket_if_not_exists(bucket_name, region):
        print(f"❌ Error: No se pudo crear/verificar el bucket '{bucket_name}'")
        return False
    
    # Paso 4: Configurar política del bucket
    print(f"\n🔒 Configurando política del bucket...")
    if not setup_bucket_policy(bucket_name):
        print("⚠️  Advertencia: No se pudo configurar la política del bucket")
        print("   Los archivos públicos podrían no ser accesibles")
    
    # Paso 5: Probar operaciones
    print(f"\n🧪 Probando operaciones de S3...")
    if not test_s3_operations(bucket_name):
        print("❌ Error: Las pruebas de S3 fallaron")
        return False
    
    print(f"\n✅ ¡Configuración de S3 completada exitosamente!")
    print(f"\n📝 Próximos pasos:")
    print(f"   1. Instalar dependencias: pip install -r requirements.txt")
    print(f"   2. Ejecutar el evaluador: python main.py")
    print(f"\n📁 Los archivos se guardarán en: s3://{bucket_name}/")
    return True

if __name__ == "__main__":
    main()