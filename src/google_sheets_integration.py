"""
Google Sheets Integration Module
Maneja la integración con Google Sheets para logging de evaluaciones
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import gspread
from google.oauth2.service_account import Credentials
from urllib.parse import urlparse

class GoogleSheetsIntegration:
    """
    Integración con Google Sheets para almacenar resultados de evaluaciones
    """
    
    def __init__(self, spreadsheet_name: str = "Website Evaluations"):
        """
        Inicializa la integración con Google Sheets
        
        Args:
            spreadsheet_name: Nombre de la hoja de cálculo
        """
        self.spreadsheet_name = spreadsheet_name
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self._setup_client()
    
    def _setup_client(self):
        """Configura el cliente de Google Sheets"""
        try:
            # Obtener credenciales
            creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
            
            if not creds_path or not os.path.exists(creds_path):
                print("Google Sheets credentials not found")
                return False
            
            # Configurar scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Autenticar
            creds = Credentials.from_service_account_file(creds_path, scopes=scope)
            self.client = gspread.authorize(creds)
            
            # Obtener o crear hoja de cálculo
            self._setup_spreadsheet()
            
            return True
            
        except Exception as e:
            print(f"Error configurando Google Sheets: {str(e)}")
            return False
    
    def _setup_spreadsheet(self):
        """Configura la hoja de cálculo"""
        try:
            # Intentar abrir hoja existente
            try:
                self.spreadsheet = self.client.open(self.spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                # Crear nueva hoja si no existe
                self.spreadsheet = self.client.create(self.spreadsheet_name)
                print(f"Hoja de cálculo creada: {self.spreadsheet_name}")
            
            # Obtener o crear worksheet
            try:
                self.worksheet = self.spreadsheet.sheet1
            except:
                self.worksheet = self.spreadsheet.add_worksheet(title="Evaluations", rows="1000", cols="20")
            
            # Configurar headers si es una hoja nueva
            self._setup_headers()
            
        except Exception as e:
            print(f"Error configurando spreadsheet: {str(e)}")
    
    def _setup_headers(self):
        """Configura los headers de la hoja"""
        try:
            # Verificar si ya hay headers
            existing_headers = self.worksheet.row_values(1)
            
            if not existing_headers:
                headers = [
                    'Timestamp',
                    'URL',
                    'Domain',
                    'Final Score',
                    'Score Category',
                    'Typography Score',
                    'Color Score',
                    'Layout Score',
                    'Usability Score',
                    'Modern Design Score',
                    'Screenshot URL',
                    'Report Path',
                    'Evaluation Time (s)',
                    'Typography Analysis',
                    'Color Analysis',
                    'Layout Analysis',
                    'Usability Analysis',
                    'Modern Design Analysis',
                    'Top Recommendations',
                    'Technical Summary'
                ]
                
                self.worksheet.append_row(headers)
                
                # Formatear headers
                self.worksheet.format('1:1', {
                    'backgroundColor': {'red': 0.2, 'green': 0.5, 'blue': 0.7},
                    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                })
                
                print("Headers configurados en Google Sheets")
                
        except Exception as e:
            print(f"Error configurando headers: {str(e)}")
    
    def log_evaluation(self, evaluation_data: Dict) -> bool:
        """
        Registra una evaluación en Google Sheets
        
        Args:
            evaluation_data: Datos de la evaluación
            
        Returns:
            True si se registró correctamente, False en caso contrario
        """
        try:
            if not self.client or not self.worksheet:
                print("Google Sheets no está configurado")
                return False
            
            # Preparar datos para la fila
            row_data = self._prepare_row_data(evaluation_data)
            
            # Añadir fila
            self.worksheet.append_row(row_data)
            
            print("Evaluación registrada en Google Sheets")
            return True
            
        except Exception as e:
            print(f"Error registrando en Google Sheets: {str(e)}")
            return False
    
    def _prepare_row_data(self, evaluation_data: Dict) -> List[str]:
        """
        Prepara los datos para una fila de la hoja de cálculo
        
        Args:
            evaluation_data: Datos de la evaluación
            
        Returns:
            Lista de valores para la fila
        """
        # Extraer datos básicos
        url = evaluation_data.get('url', '')
        domain = urlparse(url).netloc.replace('www.', '')
        timestamp = evaluation_data.get('timestamp', datetime.now().isoformat())
        final_score = evaluation_data.get('final_score', 0)
        
        # Determinar categoría de score
        score_category = self._get_score_category(final_score)
        
        # Extraer scores por categoría
        analysis_results = evaluation_data.get('analysis_results', {})
        
        typography_score = analysis_results.get('typography', {}).get('score', 0)
        color_score = analysis_results.get('color', {}).get('score', 0)
        layout_score = analysis_results.get('layout', {}).get('score', 0)
        usability_score = analysis_results.get('usability', {}).get('score', 0)
        modern_design_score = analysis_results.get('modern_design', {}).get('score', 0)
        
        # Extraer análisis (limitar longitud para Google Sheets)
        typography_analysis = self._truncate_text(
            analysis_results.get('typography', {}).get('analysis', ''), 1000
        )
        color_analysis = self._truncate_text(
            analysis_results.get('color', {}).get('analysis', ''), 1000
        )
        layout_analysis = self._truncate_text(
            analysis_results.get('layout', {}).get('analysis', ''), 1000
        )
        usability_analysis = self._truncate_text(
            analysis_results.get('usability', {}).get('analysis', ''), 1000
        )
        modern_design_analysis = self._truncate_text(
            analysis_results.get('modern_design', {}).get('analysis', ''), 1000
        )
        
        # Extraer top recomendaciones
        top_recommendations = self._get_top_recommendations(analysis_results)
        
        # Preparar resumen técnico
        technical_summary = self._prepare_technical_summary(analysis_results)
        
        return [
            timestamp,
            url,
            domain,
            final_score,
            score_category,
            typography_score,
            color_score,
            layout_score,
            usability_score,
            modern_design_score,
            evaluation_data.get('cloud_url', ''),
            evaluation_data.get('report_path', ''),
            evaluation_data.get('evaluation_time', 0),
            typography_analysis,
            color_analysis,
            layout_analysis,
            usability_analysis,
            modern_design_analysis,
            top_recommendations,
            technical_summary
        ]
    
    def _get_score_category(self, score: float) -> str:
        """Determina la categoría de puntuación"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Poor"
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Trunca texto a una longitud máxima"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _get_top_recommendations(self, analysis_results: Dict) -> str:
        """Extrae las principales recomendaciones"""
        recommendations = []
        
        for category, data in analysis_results.items():
            category_recs = data.get('recommendations', [])
            if category_recs:
                # Tomar la primera recomendación de cada categoría
                recommendations.append(f"{category.title()}: {category_recs[0]}")
        
        return " | ".join(recommendations[:3])  # Limitar a 3 principales
    
    def _prepare_technical_summary(self, analysis_results: Dict) -> str:
        """Prepara un resumen técnico compacto"""
        summary_parts = []
        
        for category, data in analysis_results.items():
            technical_data = data.get('technical_data', {})
            if technical_data:
                # Extraer algunos datos técnicos clave
                key_metrics = []
                for key, value in list(technical_data.items())[:2]:  # Solo primeros 2
                    if isinstance(value, (int, float)):
                        key_metrics.append(f"{key}: {value:.2f}")
                
                if key_metrics:
                    summary_parts.append(f"{category}: {', '.join(key_metrics)}")
        
        return " | ".join(summary_parts)
    
    def get_evaluation_history(self, url: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Obtiene el historial de evaluaciones
        
        Args:
            url: URL específica a buscar (opcional)
            limit: Número máximo de registros a devolver
            
        Returns:
            Lista de evaluaciones
        """
        try:
            if not self.worksheet:
                return []
            
            # Obtener todos los registros
            records = self.worksheet.get_all_records()
            
            # Filtrar por URL si se especifica
            if url:
                records = [r for r in records if r.get('URL') == url]
            
            # Ordenar por timestamp (más recientes primero)
            records.sort(key=lambda x: x.get('Timestamp', ''), reverse=True)
            
            # Limitar resultados
            return records[:limit]
            
        except Exception as e:
            print(f"Error obteniendo historial: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas de las evaluaciones
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            if not self.worksheet:
                return {}
            
            records = self.worksheet.get_all_records()
            
            if not records:
                return {}
            
            # Calcular estadísticas
            scores = [float(r.get('Final Score', 0)) for r in records if r.get('Final Score')]
            
            stats = {
                'total_evaluations': len(records),
                'average_score': sum(scores) / len(scores) if scores else 0,
                'highest_score': max(scores) if scores else 0,
                'lowest_score': min(scores) if scores else 0,
                'unique_domains': len(set(r.get('Domain', '') for r in records)),
                'evaluations_last_30_days': len([
                    r for r in records 
                    if self._is_recent(r.get('Timestamp', ''), days=30)
                ])
            }
            
            # Distribución por categorías
            categories = [r.get('Score Category', '') for r in records]
            category_counts = {}
            for cat in set(categories):
                if cat:
                    category_counts[cat] = categories.count(cat)
            
            stats['category_distribution'] = category_counts
            
            return stats
            
        except Exception as e:
            print(f"Error calculando estadísticas: {str(e)}")
            return {}
    
    def _is_recent(self, timestamp_str: str, days: int = 30) -> bool:
        """Verifica si una fecha es reciente"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = datetime.now()
            return (now - timestamp).days <= days
        except:
            return False
    
    def share_spreadsheet(self, email: str, role: str = 'reader') -> bool:
        """
        Comparte la hoja de cálculo con un usuario
        
        Args:
            email: Email del usuario
            role: Rol ('reader', 'writer', 'owner')
            
        Returns:
            True si se compartió correctamente
        """
        try:
            if not self.spreadsheet:
                return False
            
            self.spreadsheet.share(email, perm_type='user', role=role)
            print(f"Hoja compartida con {email} como {role}")
            return True
            
        except Exception as e:
            print(f"Error compartiendo hoja: {str(e)}")
            return False