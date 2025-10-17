#!/usr/bin/env python3
"""
Demo Script para Website Design Evaluator
Demuestra las capacidades de la herramienta
"""

import sys
import os
import time
from datetime import datetime

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def demo_single_evaluation():
    """Demostración de evaluación individual"""
    print("🎯 DEMO: Evaluación de sitio web individual")
    print("="*50)
    
    try:
        from src.website_evaluator import WebsiteEvaluator
        
        # URL de ejemplo
        demo_url = "https://www.apple.com"
        
        print(f"📍 Evaluando: {demo_url}")
        print("⏳ Iniciando evaluación...")
        
        # Crear evaluador (modo demo sin servicios externos)
        evaluator = WebsiteEvaluator()
        
        # Realizar evaluación
        result = evaluator.evaluate_website(
            demo_url,
            save_to_cloud=False,  # Sin nube para demo
            save_to_sheets=False  # Sin sheets para demo
        )
        
        # Mostrar resultados
        print("\n✅ Evaluación completada!")
        print(f"📊 Puntuación final: {result['final_score']}/100")
        
        analysis = result.get('analysis_results', {})
        for category, data in analysis.items():
            score = data.get('score', 0)
            print(f"  {category.replace('_', ' ').title()}: {score}/100")
        
        print(f"\n📁 Archivos generados:")
        if result.get('screenshot_path'):
            print(f"  📸 Screenshot: {result['screenshot_path']}")
        if result.get('report_path'):
            print(f"  📄 Reporte PDF: {result['report_path']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en demo: {str(e)}")
        return False

def demo_screenshot_only():
    """Demostración solo de captura de screenshot"""
    print("\n📸 DEMO: Captura de screenshot")
    print("="*30)
    
    try:
        from src.screenshot_capture import ScreenshotCapture
        
        capturer = ScreenshotCapture()
        
        demo_urls = [
            "https://www.github.com",
            "https://www.stackoverflow.com"
        ]
        
        for url in demo_urls:
            print(f"📷 Capturando: {url}")
            screenshot_path = capturer.capture_website(url, wait_time=2)
            print(f"  ✅ Guardado en: {screenshot_path}")
        
        capturer.close_driver()
        return True
        
    except Exception as e:
        print(f"❌ Error en captura: {str(e)}")
        return False

def demo_design_analysis():
    """Demostración de análisis de diseño"""
    print("\n🔍 DEMO: Análisis de diseño")
    print("="*30)
    
    try:
        # Buscar screenshot existente
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            print("⚠️  No hay screenshots para analizar")
            return False
        
        screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
        
        if not screenshots:
            print("⚠️  No hay screenshots disponibles")
            return False
        
        # Tomar el primer screenshot
        screenshot_path = os.path.join(screenshots_dir, screenshots[0])
        print(f"🖼️  Analizando: {screenshot_path}")
        
        from src.design_analyzer import DesignAnalyzer
        
        # Cargar configuración
        import json
        with open('config/scoring_config.json', 'r') as f:
            config = json.load(f)
        
        analyzer = DesignAnalyzer(config)
        
        # Realizar análisis (sin OpenAI para demo)
        print("🧠 Ejecutando análisis técnico...")
        
        # Análisis técnico básico
        from PIL import Image
        import cv2
        import numpy as np
        
        # Cargar imagen
        pil_image = Image.open(screenshot_path)
        cv_image = cv2.imread(screenshot_path)
        
        # Análisis de color básico
        colors = analyzer._analyze_colors(pil_image)
        print(f"  🎨 Colores dominantes detectados: {len(colors.get('dominant_colors', []))}")
        print(f"  📊 Nivel de contraste: {colors.get('contrast_level', 0):.2f}")
        
        # Análisis de layout básico  
        layout = analyzer._analyze_layout(cv_image)
        print(f"  📐 Densidad de contenido: {layout.get('content_density', 0):.2f}")
        print(f"  ⚖️  Balance horizontal: {layout.get('horizontal_balance', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en análisis: {str(e)}")
        return False

def demo_report_generation():
    """Demostración de generación de reportes"""
    print("\n📄 DEMO: Generación de reportes")
    print("="*35)
    
    try:
        from src.report_generator import ReportGenerator
        import json
        
        # Cargar configuración
        with open('config/scoring_config.json', 'r') as f:
            config = json.load(f)
        
        generator = ReportGenerator(config)
        
        # Datos de ejemplo para el reporte
        demo_data = {
            'url': 'https://demo.example.com',
            'timestamp': datetime.now().isoformat(),
            'screenshot_path': None,
            'cloud_url': None,
            'final_score': 85.5,
            'evaluation_time': 45.2,
            'analysis_results': {
                'typography': {
                    'score': 88,
                    'analysis': 'Excelente legibilidad y jerarquía tipográfica clara.',
                    'recommendations': ['Aumentar contraste en textos secundarios', 'Unificar tamaños de fuente']
                },
                'color': {
                    'score': 92,
                    'analysis': 'Esquema de colores coherente y accesible.',
                    'recommendations': ['Explorar paleta más moderna']
                },
                'layout': {
                    'score': 80,
                    'analysis': 'Buen uso del espacio en blanco y estructura clara.',
                    'recommendations': ['Mejorar alineación en móvil', 'Optimizar grid layout']
                },
                'usability': {
                    'score': 85,
                    'analysis': 'Navegación intuitiva y buena experiencia de usuario.',
                    'recommendations': ['Acelerar tiempo de carga', 'Añadir breadcrumbs']
                },
                'modern_design': {
                    'score': 78,
                    'analysis': 'Diseño actualizado pero con oportunidades de modernización.',
                    'recommendations': ['Incorporar microinteracciones', 'Actualizar iconografía']
                }
            }
        }
        
        print("📝 Generando reporte de ejemplo...")
        report_path = generator.generate_report(demo_data)
        print(f"✅ Reporte generado: {report_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando reporte: {str(e)}")
        return False

def main():
    """Función principal de demo"""
    print("🎬 WEBSITE DESIGN EVALUATOR - DEMOSTRACIÓN")
    print("="*60)
    print("Esta demo muestra las capacidades de la herramienta")
    print("Nota: Algunas funciones requieren configuración completa\n")
    
    demos = [
        ("Captura de Screenshots", demo_screenshot_only),
        ("Análisis de Diseño", demo_design_analysis), 
        ("Generación de Reportes", demo_report_generation),
        ("Evaluación Completa", demo_single_evaluation)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20}")
        print(f"🎯 {demo_name}")
        print('='*20)
        
        try:
            success = demo_func()
            results.append((demo_name, success))
            
            if success:
                print(f"✅ {demo_name} completada")
            else:
                print(f"⚠️  {demo_name} con advertencias")
                
        except KeyboardInterrupt:
            print("\n⏹️  Demo cancelada por el usuario")
            break
        except Exception as e:
            print(f"❌ Error en {demo_name}: {str(e)}")
            results.append((demo_name, False))
        
        # Pausa entre demos
        if demo_func != demos[-1][1]:  # Si no es la última demo
            print("\n⏳ Presiona Enter para continuar...")
            input()
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE LA DEMOSTRACIÓN")
    print('='*60)
    
    for demo_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {demo_name}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n🎯 Demos exitosas: {successful}/{total}")
    
    if successful == total:
        print("🏆 ¡Todas las demos completadas exitosamente!")
    elif successful > 0:
        print("⚠️  Algunas funciones requieren configuración adicional")
    else:
        print("❌ Revisa la instalación y configuración")
    
    print("\n💡 Para usar la herramienta completa:")
    print("   1. Ejecuta: python setup.py")
    print("   2. Configura credenciales en .env")
    print("   3. Ejecuta: python main.py https://ejemplo.com")

if __name__ == "__main__":
    main()