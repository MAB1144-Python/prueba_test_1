"""
Report Generator Module
Genera reportes PDF detallados con los resultados de la evaluación
"""

import os
from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from PIL import Image as PILImage

class ReportGenerator:
    """
    Genera reportes PDF profesionales con los resultados de evaluación
    """
    
    def __init__(self, config: Dict, reports_dir: str = "reports"):
        """
        Inicializa el generador de reportes
        
        Args:
            config: Configuración de puntuación
            reports_dir: Directorio para guardar reportes
        """
        self.config = config
        self.reports_dir = reports_dir
        self.ensure_directory_exists()
        
        # Configurar estilos
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Configurar colores
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def ensure_directory_exists(self):
        """Asegura que el directorio de reportes existe"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el reporte"""
        # Estilo para títulos principales
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2E86AB'),
            alignment=TA_CENTER
        )
        
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor('#A23B72'),
            borderWidth=1,
            borderColor=HexColor('#A23B72'),
            borderPadding=5
        )
        
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        )
        
        # Estilo para recomendaciones
        self.recommendation_style = ParagraphStyle(
            'Recommendation',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=8,
            textColor=HexColor('#F18F01')
        )
    
    def generate_report(self, evaluation_data: Dict) -> str:
        """
        Genera el reporte PDF completo
        
        Args:
            evaluation_data: Datos de la evaluación
            
        Returns:
            Ruta del archivo PDF generado
        """
        # Generar nombre de archivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(evaluation_data['url']).netloc.replace("www.", "").replace(".", "_")
        filename = f"report_{domain}_{timestamp}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=0.5*inch)
        story = []
        
        # Generar contenido del reporte
        self._add_cover_page(story, evaluation_data)
        self._add_executive_summary(story, evaluation_data)
        self._add_score_visualization(story, evaluation_data)
        self._add_detailed_analysis(story, evaluation_data)
        self._add_recommendations(story, evaluation_data)
        self._add_technical_data(story, evaluation_data)
        
        # Generar PDF
        doc.build(story)
        
        # Limpiar archivos temporales
        self._cleanup_temp_files()
        
        print(f"Reporte generado: {filepath}")
        return filepath
    
    def _add_cover_page(self, story: List, evaluation_data: Dict):
        """Añade la página de portada"""
        # Título principal
        title = f"Reporte de Evaluación de Diseño Web"
        story.append(Paragraph(title, self.title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # URL evaluada
        url_text = f"<b>Sitio Web Evaluado:</b><br/>{evaluation_data['url']}"
        story.append(Paragraph(url_text, self.normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Screenshot si está disponible
        if evaluation_data.get('screenshot_path') and os.path.exists(evaluation_data['screenshot_path']):
            try:
                # Usar directamente la imagen original en lugar de crear temporal
                original_path = evaluation_data['screenshot_path']
                
                # Verificar que el archivo existe
                if os.path.exists(original_path):
                    story.append(Image(original_path, width=4*inch, height=3*inch))
                    story.append(Spacer(1, 0.3*inch))
            except Exception as e:
                print(f"Error añadiendo screenshot: {str(e)}")
        
        # Puntuación final destacada
        score = evaluation_data.get('final_score', 0)
        score_category = self._get_score_category(score)
        
        score_text = f"""
        <para align="center">
        <b><font size="20" color="{self.config['score_ranges'][score_category]['color']}">
        Puntuación Final: {score}/100
        </font></b><br/>
        <font size="14">Categoría: {score_category.replace('_', ' ').title()}</font>
        </para>
        """
        story.append(Paragraph(score_text, self.normal_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Información del reporte
        report_info = f"""
        <b>Fecha de Evaluación:</b> {datetime.fromisoformat(evaluation_data['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}<br/>
        <b>Tiempo de Evaluación:</b> {evaluation_data.get('evaluation_time', 0):.2f} segundos<br/>
        <b>Generado por:</b> Website Design Evaluator v1.0
        """
        story.append(Paragraph(report_info, self.normal_style))
        story.append(PageBreak())
    
    def _add_executive_summary(self, story: List, evaluation_data: Dict):
        """Añade el resumen ejecutivo"""
        story.append(Paragraph("Resumen Ejecutivo", self.title_style))
        
        analysis_results = evaluation_data.get('analysis_results', {})
        score = evaluation_data.get('final_score', 0)
        
        # Resumen general
        summary_text = f"""
        La evaluación del sitio web {evaluation_data['url']} ha resultado en una puntuación 
        general de {score}/100, clasificándolo en la categoría 
        "{self._get_score_category(score).replace('_', ' ').title()}".
        
        Esta evaluación se basa en el análisis de cinco criterios principales: 
        Tipografía, Color, Layout, Usabilidad y Diseño Moderno, cada uno con 
        pesos específicos según su importancia para la experiencia del usuario.
        """
        story.append(Paragraph(summary_text, self.normal_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Puntuaciones por categoría
        categories_table = []
        categories_table.append(['Categoría', 'Puntuación', 'Peso', 'Contribución'])
        
        weights = self.config['scoring_weights']
        for category, data in analysis_results.items():
            if category in weights:
                weight = weights[category]['weight']
                score_cat = data.get('score', 0)
                contribution = score_cat * weight
                
                categories_table.append([
                    category.replace('_', ' ').title(),
                    f"{score_cat}/100",
                    f"{weight*100:.0f}%",
                    f"{contribution:.1f}"
                ])
        
        # Crear tabla
        table = Table(categories_table, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(table)
        story.append(PageBreak())
    
    def _add_score_visualization(self, story: List, evaluation_data: Dict):
        """Añade visualizaciones de las puntuaciones"""
        story.append(Paragraph("Visualización de Puntuaciones", self.title_style))
        
        # Crear gráficos
        chart_path = self._create_score_charts(evaluation_data)
        
        if chart_path and os.path.exists(chart_path):
            story.append(Image(chart_path, width=6*inch, height=4*inch))
            # Guardar la ruta para limpiar después
            self._temp_files_to_clean = getattr(self, '_temp_files_to_clean', [])
            self._temp_files_to_clean.append(chart_path)
        
        story.append(PageBreak())
    
    def _add_detailed_analysis(self, story: List, evaluation_data: Dict):
        """Añade análisis detallado por categoría"""
        story.append(Paragraph("Análisis Detallado", self.title_style))
        
        analysis_results = evaluation_data.get('analysis_results', {})
        
        for category, data in analysis_results.items():
            # Título de categoría
            category_title = category.replace('_', ' ').title()
            story.append(Paragraph(category_title, self.subtitle_style))
            
            # Puntuación
            score = data.get('score', 0)
            score_text = f"<b>Puntuación:</b> {score}/100"
            story.append(Paragraph(score_text, self.normal_style))
            
            # Análisis
            analysis = data.get('analysis', 'No disponible')
            if analysis and analysis != 'Análisis no disponible':
                story.append(Paragraph(f"<b>Análisis:</b> {analysis}", self.normal_style))
            
            story.append(Spacer(1, 0.2*inch))
    
    def _add_recommendations(self, story: List, evaluation_data: Dict):
        """Añade sección de recomendaciones"""
        story.append(Paragraph("Recomendaciones de Mejora", self.title_style))
        
        analysis_results = evaluation_data.get('analysis_results', {})
        
        for category, data in analysis_results.items():
            recommendations = data.get('recommendations', [])
            
            if recommendations:
                category_title = category.replace('_', ' ').title()
                story.append(Paragraph(category_title, self.subtitle_style))
                
                for rec in recommendations:
                    bullet_text = f"• {rec}"
                    story.append(Paragraph(bullet_text, self.recommendation_style))
                
                story.append(Spacer(1, 0.2*inch))
        
        story.append(PageBreak())
    
    def _add_technical_data(self, story: List, evaluation_data: Dict):
        """Añade datos técnicos del análisis"""
        story.append(Paragraph("Datos Técnicos", self.title_style))
        
        analysis_results = evaluation_data.get('analysis_results', {})
        
        # Cloud URL si está disponible
        if evaluation_data.get('cloud_url'):
            cloud_text = f"<b>Screenshot en la nube:</b> <link href='{evaluation_data['cloud_url']}'>{evaluation_data['cloud_url']}</link>"
            story.append(Paragraph(cloud_text, self.normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Datos técnicos por categoría
        for category, data in analysis_results.items():
            technical_data = data.get('technical_data')
            
            if technical_data:
                category_title = f"Datos Técnicos - {category.replace('_', ' ').title()}"
                story.append(Paragraph(category_title, self.subtitle_style))
                
                # Convertir datos técnicos a texto legible
                for key, value in technical_data.items():
                    if isinstance(value, (int, float)):
                        value = f"{value:.2f}" if isinstance(value, float) else str(value)
                    elif isinstance(value, list):
                        value = ", ".join(str(v) for v in value[:5])  # Limitar para legibilidad
                    
                    tech_text = f"<b>{key.replace('_', ' ').title()}:</b> {value}"
                    story.append(Paragraph(tech_text, self.normal_style))
    
    def _create_score_charts(self, evaluation_data: Dict) -> str:
        """
        Crea gráficos de puntuaciones
        
        Returns:
            Ruta del archivo de gráfico generado
        """
        try:
            analysis_results = evaluation_data.get('analysis_results', {})
            
            # Preparar datos
            categories = []
            scores = []
            
            for category, data in analysis_results.items():
                categories.append(category.replace('_', ' ').title())
                scores.append(data.get('score', 0))
            
            # Crear figura con subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Gráfico de barras
            colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
            bars = ax1.bar(categories, scores, color=colors)
            ax1.set_title('Puntuaciones por Categoría', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Puntuación')
            ax1.set_ylim(0, 100)
            
            # Añadir valores en las barras
            for bar, score in zip(bars, scores):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'{score:.1f}', ha='center', va='bottom')
            
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
            
            # Gráfico circular
            ax2.pie(scores, labels=categories, autopct='%1.1f%%', colors=colors)
            ax2.set_title('Distribución de Puntuaciones', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # Guardar gráfico
            chart_path = os.path.join(self.reports_dir, "temp_chart.png")
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Error creando gráficos: {str(e)}")
            return None
    
    def _get_score_category(self, score: float) -> str:
        """Obtiene la categoría de puntuación"""
        try:
            # Validar que score sea un número
            if score is None:
                print(f"⚠️ Advertencia: Score es None, usando 'poor' por defecto")
                return 'poor'
            
            # Convertir a float si es necesario
            score = float(score)
            
            # Validar rango
            if score < 0:
                print(f"⚠️ Advertencia: Score negativo ({score}), usando 'poor'")
                return 'poor'
            elif score > 100:
                print(f"⚠️ Advertencia: Score mayor a 100 ({score}), usando 'excellent'")
                return 'excellent'
            
            ranges = self.config['score_ranges']
            
            for category, range_data in ranges.items():
                if range_data['min'] <= score <= range_data['max']:
                    return category
            
            print(f"⚠️ Advertencia: Score {score} no está en ningún rango válido")
            print(f"📋 Rangos disponibles: {ranges}")
            return 'poor'  # Valor por defecto más seguro que 'unknown'
            
        except (ValueError, TypeError) as e:
            print(f"❌ Error convirtiendo score a número: {score} ({type(score)})")
            print(f"📝 Error: {e}")
            return 'poor'
    
    def _cleanup_temp_files(self):
        """Limpia archivos temporales creados durante la generación del reporte"""
        if hasattr(self, '_temp_files_to_clean'):
            for temp_file in self._temp_files_to_clean:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        print(f"Archivo temporal eliminado: {temp_file}")
                except Exception as e:
                    print(f"Error eliminando archivo temporal {temp_file}: {e}")
            # Limpiar la lista
            self._temp_files_to_clean = []


# Importaciones adicionales necesarias
import numpy as np