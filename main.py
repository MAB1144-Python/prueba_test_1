#!/usr/bin/env python3
"""
Website Design Evaluator - Script Principal
Punto de entrada para evaluar sitios web desde la línea de comandos
"""

import sys
import os
import argparse
from typing import List
from urllib.parse import urlparse

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.website_evaluator import WebsiteEvaluator

def validate_url(url: str) -> bool:
    """Valida formato de URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Evalúa el diseño de sitios web usando IA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py https://ejemplo.com
  python main.py https://ejemplo.com --no-cloud --no-sheets
  python main.py --batch urls.txt
  python main.py https://ejemplo.com --config custom_config.json
        """
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='URL del sitio web a evaluar'
    )
    
    parser.add_argument(
        '--batch',
        type=str,
        help='Archivo con lista de URLs para evaluación en lote'
    )
    
    parser.add_argument(
        '--no-cloud',
        action='store_true',
        help='No subir screenshots a la nube'
    )
    
    parser.add_argument(
        '--no-sheets',
        action='store_true',
        help='No guardar resultados en Google Sheets'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/scoring_config.json',
        help='Archivo de configuración personalizado'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directorio personalizado para reportes'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    args = parser.parse_args()
    
    # Validar argumentos
    if not args.url and not args.batch:
        parser.error('Debe especificar una URL o usar --batch')
    
    if args.url and args.batch:
        parser.error('No puede usar URL y --batch al mismo tiempo')
    
    try:
        # Inicializar evaluador
        print("🚀 Iniciando Website Design Evaluator...")
        
        config_path = args.config
        if not os.path.exists(config_path):
            print(f"❌ Error: Archivo de configuración no encontrado: {config_path}")
            return 1
        
        evaluator = WebsiteEvaluator(config_path)
        
        # Configurar opciones
        save_to_cloud = not args.no_cloud
        save_to_sheets = not args.no_sheets
        
        if args.verbose:
            print(f"📊 Configuración cargada desde: {config_path}")
            print(f"☁️  Guardar en nube: {save_to_cloud}")
            print(f"📋 Guardar en Sheets: {save_to_sheets}")
        
        # Evaluación individual
        if args.url:
            if not validate_url(args.url):
                print(f"❌ Error: URL inválida: {args.url}")
                return 1
            
            print(f"\n🔍 Evaluando: {args.url}")
            
            try:
                result = evaluator.evaluate_website(
                    args.url,
                    save_to_cloud=save_to_cloud,
                    save_to_sheets=save_to_sheets
                )
                
                print_results(result, args.verbose)
                
            except Exception as e:
                import traceback
                print(f"❌ Error durante la evaluación: {str(e)}")
                print(f"📝 Tipo de error: {type(e).__name__}")
                if hasattr(e, '__dict__'):
                    print(f"📋 Detalles del error: {e.__dict__}")
                print(f"🔍 Traceback completo:")
                traceback.print_exc()
                return 1
        
        # Evaluación en lote
        elif args.batch:
            if not os.path.exists(args.batch):
                print(f"❌ Error: Archivo no encontrado: {args.batch}")
                return 1
            
            # Leer URLs del archivo
            urls = []
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"❌ Error leyendo archivo: {str(e)}")
                return 1
            
            # Validar URLs
            valid_urls = []
            for url in urls:
                if validate_url(url):
                    valid_urls.append(url)
                else:
                    print(f"⚠️  URL inválida ignorada: {url}")
            
            if not valid_urls:
                print("❌ Error: No se encontraron URLs válidas")
                return 1
            
            print(f"\n📋 Evaluando {len(valid_urls)} sitios web...")
            
            try:
                results = evaluator.batch_evaluate(
                    valid_urls,
                    save_to_cloud=save_to_cloud,
                    save_to_sheets=save_to_sheets
                )
                
                print_batch_results(results, args.verbose)
                
            except Exception as e:
                print(f"❌ Error durante la evaluación en lote: {str(e)}")
                return 1
        
        print("\n✅ Evaluación completada exitosamente!")
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Evaluación cancelada por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        return 1
    finally:
        # Limpiar recursos
        if 'evaluator' in locals():
            if hasattr(evaluator.screenshot_capture, 'close_driver'):
                evaluator.screenshot_capture.close_driver()

def print_results(result: dict, verbose: bool = False):
    """Imprime los resultados de una evaluación individual"""
    print("\n" + "="*60)
    print(f"📊 RESULTADOS DE EVALUACIÓN")
    print("="*60)
    
    print(f"🌐 URL: {result['url']}")
    print(f"📅 Fecha: {result['timestamp']}")
    print(f"⏱️  Tiempo: {result.get('evaluation_time', 0):.2f}s")
    
    # Puntuación final
    score = result.get('final_score', 0)
    category = get_score_emoji(score)
    print(f"\n🎯 PUNTUACIÓN FINAL: {score}/100 {category}")
    
    # Puntuaciones por categoría
    print(f"\n📋 DESGLOSE POR CATEGORÍAS:")
    analysis_results = result.get('analysis_results', {})
    
    for category, data in analysis_results.items():
        category_name = category.replace('_', ' ').title()
        category_score = data.get('score', 0)
        emoji = get_score_emoji(category_score)
        print(f"  {category_name}: {category_score}/100 {emoji}")
    
    # Archivos generados
    print(f"\n📁 ARCHIVOS GENERADOS:")
    if result.get('screenshot_path'):
        print(f"  📸 Screenshot: {result['screenshot_path']}")
    if result.get('report_path'):
        print(f"  📄 Reporte: {result['report_path']}")
    if result.get('cloud_url'):
        print(f"  ☁️  Nube: {result['cloud_url']}")
    
    # Información verbose
    if verbose and analysis_results:
        print(f"\n🔍 ANÁLISIS DETALLADO:")
        for category, data in analysis_results.items():
            analysis = data.get('analysis', '')
            if analysis and len(analysis) > 50:
                print(f"\n{category.replace('_', ' ').title()}:")
                print(f"  {analysis[:200]}...")

def print_batch_results(results: List[dict], verbose: bool = False):
    """Imprime los resultados de evaluación en lote"""
    print("\n" + "="*60)
    print(f"📊 RESULTADOS DE EVALUACIÓN EN LOTE")
    print("="*60)
    
    successful = [r for r in results if 'final_score' in r]
    failed = [r for r in results if 'error' in r]
    
    print(f"✅ Exitosas: {len(successful)}")
    print(f"❌ Fallidas: {len(failed)}")
    print(f"📊 Total: {len(results)}")
    
    if successful:
        scores = [r['final_score'] for r in successful]
        avg_score = sum(scores) / len(scores)
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"  Promedio: {avg_score:.2f}/100")
        print(f"  Mejor: {max(scores):.2f}/100")
        print(f"  Peor: {min(scores):.2f}/100")
        
        print(f"\n🏆 TOP 3 SITIOS:")
        sorted_results = sorted(successful, key=lambda x: x['final_score'], reverse=True)
        for i, result in enumerate(sorted_results[:3], 1):
            score = result['final_score']
            url = result['url']
            emoji = get_score_emoji(score)
            print(f"  {i}. {url} - {score}/100 {emoji}")
    
    if failed and verbose:
        print(f"\n❌ ERRORES:")
        for result in failed[:5]:  # Mostrar solo los primeros 5 errores
            print(f"  {result['url']}: {result['error']}")

def get_score_emoji(score: float) -> str:
    """Obtiene emoji según la puntuación"""
    if score >= 90:
        return "🏆"  # Excelente
    elif score >= 80:
        return "🥇"  # Muy bueno
    elif score >= 70:
        return "🥈"  # Bueno
    elif score >= 60:
        return "🥉"  # Regular
    else:
        return "❌"  # Pobre

if __name__ == "__main__":
    sys.exit(main())