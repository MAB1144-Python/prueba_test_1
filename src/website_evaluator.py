"""
Website Design Evaluator - Módulo principal
Evalúa el diseño de sitios web usando IA y genera reportes detallados
"""

import os
import json
import time
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import openai
from dotenv import load_dotenv

from .screenshot_capture import ScreenshotCapture
from .cloud_storage import CloudStorageManager
from .design_analyzer import DesignAnalyzer
from .report_generator import ReportGenerator
from .google_sheets_integration import GoogleSheetsIntegration

# Cargar variables de entorno
load_dotenv()

class WebsiteEvaluator:
    """
    Clase principal para evaluar el diseño de sitios web
    """
    
    def __init__(self, config_path: str = "config/scoring_config.json"):
        """
        Inicializa el evaluador de sitios web
        
        Args:
            config_path: Ruta al archivo de configuración de puntuación
        """
        self.config = self._load_config(config_path)
        self.screenshot_capture = ScreenshotCapture()
        self.cloud_storage = CloudStorageManager()
        self.design_analyzer = DesignAnalyzer(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.sheets_integration = GoogleSheetsIntegration()
        
        # Configurar OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carga la configuración de puntuación"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file: {config_path}")
    
    def validate_url(self, url: str) -> bool:
        """
        Valida si la URL es correcta
        
        Args:
            url: URL a validar
            
        Returns:
            True si es válida, False en caso contrario
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def evaluate_website(self, url: str, save_to_cloud: bool = True, 
                        save_to_sheets: bool = True) -> Dict:
        """
        Evalúa un sitio web completo
        
        Args:
            url: URL del sitio web a evaluar
            save_to_cloud: Si guardar capturas en la nube
            save_to_sheets: Si guardar resultados en Google Sheets
            
        Returns:
            Diccionario con los resultados de la evaluación
        """
        if not self.validate_url(url):
            raise ValueError(f"URL inválida: {url}")
        
        print(f"Iniciando evaluación de: {url}")
        start_time = time.time()
        
        # 1. Capturar screenshot
        print("Capturando screenshot...")
        screenshot_path = self.screenshot_capture.capture_website(url)
        
        # 2. Subir a la nube si se requiere
        cloud_url = None
        if save_to_cloud:
            print("Subiendo screenshot a la nube...")
            cloud_url = self.cloud_storage.upload_screenshot(screenshot_path)
        
        # 3. Analizar diseño
        print("Analizando diseño con IA...")
        analysis_results = self.design_analyzer.analyze_design(screenshot_path, url)
        
        # 4. Calcular puntuación final
        final_score = self._calculate_final_score(analysis_results)
        
        # 5. Generar reporte
        evaluation_data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'screenshot_path': screenshot_path,
            'cloud_url': cloud_url,
            'analysis_results': analysis_results,
            'final_score': final_score,
            'evaluation_time': time.time() - start_time
        }
        
        print("Generando reporte PDF...")
        report_path = self.report_generator.generate_report(evaluation_data)
        evaluation_data['report_path'] = report_path
        
        # 6. Guardar en Google Sheets si se requiere
        if save_to_sheets:
            print("Guardando resultados en Google Sheets...")
            self.sheets_integration.log_evaluation(evaluation_data)
        
        print(f"Evaluación completada. Puntuación final: {final_score}/100")
        return evaluation_data
    
    def _calculate_final_score(self, analysis_results: Dict) -> float:
        """
        Calcula la puntuación final basada en los pesos configurados
        
        Args:
            analysis_results: Resultados del análisis de diseño
            
        Returns:
            Puntuación final (0-100)
        """
        total_score = 0.0
        weights = self.config['scoring_weights']
        
        for category, category_data in weights.items():
            if category in analysis_results:
                category_score = analysis_results[category]['score']
                weight = category_data['weight']
                total_score += category_score * weight
        
        return round(total_score, 2)
    
    def batch_evaluate(self, urls: List[str], save_to_cloud: bool = True, 
                      save_to_sheets: bool = True) -> List[Dict]:
        """
        Evalúa múltiples sitios web en lote
        
        Args:
            urls: Lista de URLs a evaluar
            save_to_cloud: Si guardar capturas en la nube
            save_to_sheets: Si guardar resultados en Google Sheets
            
        Returns:
            Lista con los resultados de todas las evaluaciones
        """
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\nEvaluando sitio {i}/{len(urls)}: {url}")
            try:
                result = self.evaluate_website(url, save_to_cloud, save_to_sheets)
                results.append(result)
            except Exception as e:
                print(f"Error evaluando {url}: {str(e)}")
                results.append({
                    'url': url,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return results
    
    def get_score_category(self, score: float) -> str:
        """
        Obtiene la categoría de puntuación basada en el score
        
        Args:
            score: Puntuación (0-100)
            
        Returns:
            Categoría de la puntuación
        """
        # Validar entrada
        if score is None:
            print(f"⚠️ Score es None, usando valor por defecto")
            score = 50
        
        # Asegurar que el score esté en el rango válido
        if not isinstance(score, (int, float)):
            print(f"⚠️ Score no es numérico: {score}, usando valor por defecto")
            score = 50
        
        score = max(0, min(100, float(score)))  # Clamp entre 0 y 100
        
        ranges = self.config['score_ranges']
        
        for category, range_data in ranges.items():
            if range_data['min'] <= score <= range_data['max']:
                return category
        
        # Fallback - esto no debería suceder con el clamping
        print(f"⚠️ Score {score} no coincide con ningún rango, usando 'fair'")
        return 'fair'