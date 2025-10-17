"""
Tests básicos para Website Design Evaluator
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch

# Añadir src al path para las pruebas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestWebsiteEvaluator(unittest.TestCase):
    """Tests para la clase principal WebsiteEvaluator"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.test_config = {
            'scoring_weights': {
                'typography': {'weight': 0.25},
                'color': {'weight': 0.20},
                'layout': {'weight': 0.25},
                'usability': {'weight': 0.20},
                'modern_design': {'weight': 0.10}
            },
            'score_ranges': {
                'excellent': {'min': 90, 'max': 100, 'color': '#4CAF50'},
                'poor': {'min': 0, 'max': 59, 'color': '#F44336'}
            }
        }
    
    def test_validate_url(self):
        """Test validación de URLs"""
        from website_evaluator import WebsiteEvaluator
        
        evaluator = WebsiteEvaluator.__new__(WebsiteEvaluator)  # Sin __init__
        
        # URLs válidas
        valid_urls = [
            'https://www.google.com',
            'http://example.com',
            'https://subdomain.example.co.uk'
        ]
        
        for url in valid_urls:
            self.assertTrue(evaluator.validate_url(url), f"URL válida falló: {url}")
        
        # URLs inválidas
        invalid_urls = [
            'not-a-url',
            'ftp://example.com',
            '',
            'https://',
            'www.google.com'  # Sin protocolo
        ]
        
        for url in invalid_urls:
            self.assertFalse(evaluator.validate_url(url), f"URL inválida pasó: {url}")
    
    def test_calculate_final_score(self):
        """Test cálculo de puntuación final"""
        from website_evaluator import WebsiteEvaluator
        
        with patch.object(WebsiteEvaluator, '_load_config', return_value=self.test_config):
            evaluator = WebsiteEvaluator.__new__(WebsiteEvaluator)
            evaluator.config = self.test_config
            
            # Datos de prueba
            analysis_results = {
                'typography': {'score': 80},
                'color': {'score': 90},
                'layout': {'score': 70},
                'usability': {'score': 85},
                'modern_design': {'score': 75}
            }
            
            score = evaluator._calculate_final_score(analysis_results)
            
            # Calcular score esperado manualmente
            expected = (80 * 0.25) + (90 * 0.20) + (70 * 0.25) + (85 * 0.20) + (75 * 0.10)
            expected = round(expected, 2)
            
            self.assertEqual(score, expected, "Cálculo de puntuación final incorrecto")
    
    def test_get_score_category(self):
        """Test categorización de puntuaciones"""
        from website_evaluator import WebsiteEvaluator
        
        with patch.object(WebsiteEvaluator, '_load_config', return_value=self.test_config):
            evaluator = WebsiteEvaluator.__new__(WebsiteEvaluator)
            evaluator.config = self.test_config
            
            # Test casos límite
            self.assertEqual(evaluator.get_score_category(95), 'excellent')
            self.assertEqual(evaluator.get_score_category(90), 'excellent')
            self.assertEqual(evaluator.get_score_category(59), 'poor')
            self.assertEqual(evaluator.get_score_category(0), 'poor')


class TestScreenshotCapture(unittest.TestCase):
    """Tests para captura de screenshots"""
    
    def test_ensure_directory_exists(self):
        """Test creación de directorios"""
        from screenshot_capture import ScreenshotCapture
        
        test_dir = "test_screenshots"
        
        # Limpiar si existe
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        
        # Crear capturador
        capturer = ScreenshotCapture(test_dir)
        
        # Verificar que el directorio se creó
        self.assertTrue(os.path.exists(test_dir), "Directorio no fue creado")
        
        # Limpiar
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


class TestDesignAnalyzer(unittest.TestCase):
    """Tests para análisis de diseño"""
    
    def test_find_sections(self):
        """Test detección de secciones"""
        from design_analyzer import DesignAnalyzer
        
        analyzer = DesignAnalyzer({})
        
        # Crear perfil vertical de prueba
        import numpy as np
        
        # Simular perfil con 3 secciones separadas por espacios
        profile = np.array([5, 5, 5, 50, 50, 5, 5, 30, 30, 30, 5, 5])
        
        sections = analyzer._find_sections(profile, threshold=10)
        
        # Deberíamos encontrar 2 secciones principales
        self.assertGreaterEqual(len(sections), 2, "No se detectaron suficientes secciones")


class TestReportGenerator(unittest.TestCase):
    """Tests para generación de reportes"""
    
    def test_get_score_category(self):
        """Test categorización en reporte"""
        from report_generator import ReportGenerator
        
        generator = ReportGenerator(self.test_config)
        
        # Test categorías
        self.assertEqual(generator._get_score_category(95), 'excellent')
        self.assertEqual(generator._get_score_category(50), 'poor')


class TestGoogleSheetsIntegration(unittest.TestCase):
    """Tests para integración con Google Sheets"""
    
    def test_prepare_row_data(self):
        """Test preparación de datos para fila"""
        from google_sheets_integration import GoogleSheetsIntegration
        
        integration = GoogleSheetsIntegration.__new__(GoogleSheetsIntegration)
        
        # Datos de prueba
        evaluation_data = {
            'url': 'https://example.com',
            'timestamp': '2024-01-01T12:00:00',
            'final_score': 85.5,
            'analysis_results': {
                'typography': {'score': 90, 'analysis': 'Buen análisis'},
                'color': {'score': 80, 'analysis': 'Análisis de color'}
            },
            'cloud_url': 'https://cloud.example.com/file',
            'evaluation_time': 45.2
        }
        
        row_data = integration._prepare_row_data(evaluation_data)
        
        # Verificar que se generaron datos
        self.assertIsInstance(row_data, list, "Datos de fila deben ser una lista")
        self.assertGreater(len(row_data), 10, "Datos de fila muy cortos")
        
        # Verificar algunos campos específicos
        self.assertEqual(row_data[1], 'https://example.com', "URL incorrecta")
        self.assertEqual(row_data[3], 85.5, "Puntuación incorrecta")


def run_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 Ejecutando pruebas para Website Design Evaluator...")
    print("="*60)
    
    # Configurar el test runner
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Cargar tests
    test_classes = [
        TestWebsiteEvaluator,
        TestScreenshotCapture,
        TestDesignAnalyzer, 
        TestReportGenerator,
        TestGoogleSheetsIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ FALLOS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print(f"\n⚠️  ERRORES:")
        for test, traceback in result.errors:
            print(f"  - {test}: Error de ejecución")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🏆 ¡Todas las pruebas pasaron exitosamente!")
    elif success_rate >= 80:
        print("✅ La mayoría de pruebas pasaron correctamente")
    else:
        print("⚠️  Revisa los errores antes de usar en producción")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)