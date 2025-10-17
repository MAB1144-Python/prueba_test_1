"""
Cloud Storage Manager
Maneja el almacenamiento de archivos en Amazon S3
"""

import os
import boto3
import uuid
from datetime import datetime
from typing import Optional
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logger = logging.getLogger(__name__)

class CloudStorageManager:
    """
    Maneja el almacenamiento de archivos en Amazon S3
    """
    
    def __init__(self):
        """Inicializa el administrador de almacenamiento en la nube"""
        self.s3_client = None
        self.bucket_name = None
        self._setup_s3()
    
    def _setup_s3(self):
        """Configura Amazon S3"""
        try:
            # Obtener configuración de variables de entorno
            aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            self.bucket_name = os.getenv('AWS_S3_BUCKET')
            
            if not aws_access_key or not aws_secret_key:
                logger.warning("⚠️ Credenciales de AWS no encontradas en variables de entorno")
                return False
            
            if not self.bucket_name:
                logger.warning("⚠️ Nombre del bucket S3 no especificado")
                return False
            
            # Crear cliente S3
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            
            # Verificar conexión
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info("✅ Amazon S3 configurado correctamente")
            return True
            
        except NoCredentialsError:
            logger.error("❌ Credenciales de AWS no válidas")
            return False
        except ClientError as e:
            logger.error(f"❌ Error de S3: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error configurando S3: {e}")
            return False
    
    def upload_to_s3(self, file_path: str, folder: str = "screenshots") -> Optional[str]:
        """
        Sube un archivo a Amazon S3
        
        Args:
            file_path: Ruta local del archivo
            folder: Carpeta dentro del bucket (por defecto 'screenshots')
            
        Returns:
            URL del archivo subido o None si falla
        """
        if not self.s3_client or not self.bucket_name:
            logger.error("❌ S3 no está configurado correctamente")
            return None
            
        if not os.path.exists(file_path):
            logger.error(f"❌ Archivo no encontrado: {file_path}")
            return None
        
        try:
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = os.path.basename(file_path)
            name_parts = os.path.splitext(file_name)
            unique_name = f"{name_parts[0]}_{timestamp}{name_parts[1]}"
            
            # Construir la clave S3
            s3_key = f"{folder}/{unique_name}"
            
            # Determinar tipo de contenido
            content_type = 'image/png'
            if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file_path.lower().endswith('.pdf'):
                content_type = 'application/pdf'
            
            # Subir archivo
            with open(file_path, 'rb') as file_data:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=file_data,
                    ContentType=content_type,
                    Metadata={
                        'uploaded-by': 'website-evaluator',
                        'upload-time': datetime.now().isoformat()
                    }
                )
            
            # Generar URL presignada (válida por 24 horas)
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=86400  # 24 horas
            )
            
            logger.info(f"✅ Archivo subido a S3: {s3_key}")
            return url
            
        except ClientError as e:
            logger.error(f"❌ Error subiendo archivo a S3: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            return None
    
    def upload_screenshot(self, file_path: str) -> Optional[str]:
        """
        Sube un screenshot a Amazon S3
        
        Args:
            file_path: Ruta del archivo screenshot
            
        Returns:
            URL del screenshot subido
        """
        logger.info("📤 Subiendo screenshot a Amazon S3...")
        
        if not os.path.exists(file_path):
            logger.error(f"❌ Screenshot no encontrado: {file_path}")
            return None
        
        # Intentar subir a S3
        s3_url = self.upload_to_s3(file_path, "screenshots")
        
        if s3_url:
            logger.info(f"✅ Screenshot subido exitosamente: {s3_url}")
            return s3_url
        else:
            logger.error("❌ No se pudo subir el screenshot a S3")
            return None
    
    def upload_report(self, file_path: str) -> Optional[str]:
        """
        Sube un reporte PDF a Amazon S3
        
        Args:
            file_path: Ruta del archivo PDF
            
        Returns:
            URL del reporte subido
        """
        logger.info("📤 Subiendo reporte a Amazon S3...")
        
        if not os.path.exists(file_path):
            logger.error(f"❌ Reporte no encontrado: {file_path}")
            return None
        
        # Intentar subir a S3
        s3_url = self.upload_to_s3(file_path, "reports")
        
        if s3_url:
            logger.info(f"✅ Reporte subido exitosamente: {s3_url}")
            return s3_url
        else:
            logger.error("❌ No se pudo subir el reporte a S3")
            return None
    
    def get_available_services(self) -> dict:
        """
        Verifica qué servicios están disponibles
        
        Returns:
            Diccionario con el estado de cada servicio
        """
        return {
            's3': self.s3_client is not None and self.bucket_name is not None
        }