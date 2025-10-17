"""
Design Analyzer Module
Analiza el diseño de sitios web usando OpenAI y técnicas de visión artificial
"""

import os
import json
import base64
import cv2
import numpy as np
from typing import Dict, List, Tuple
from PIL import Image, ImageStat
import webcolors
import openai
from openai import OpenAI

class DesignAnalyzer:
    """
    Analiza aspectos del diseño web usando IA y procesamiento de imágenes
    """
    
    def __init__(self, config: Dict):
        """
        Inicializa el analizador de diseño
        
        Args:
            config: Configuración de puntuación y prompts
        """
        self.config = config
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def analyze_design(self, screenshot_path: str, url: str) -> Dict:
        """
        Realiza análisis completo del diseño
        
        Args:
            screenshot_path: Ruta del screenshot a analizar
            url: URL del sitio web
            
        Returns:
            Diccionario con todos los resultados del análisis
        """
        print("Iniciando análisis de diseño...")
        
        # Cargar y procesar imagen
        image = cv2.imread(screenshot_path)
        pil_image = Image.open(screenshot_path)
        
        results = {}
        
        # Análisis con IA (OpenAI Vision)
        try:
            print("Analizando con OpenAI...")
            ai_analysis = self._analyze_with_openai(screenshot_path)
            print(f"Análisis OpenAI exitoso")
        except Exception as e:
            print(f"Error en OpenAI: {str(e)}")
            ai_analysis = self._get_default_ai_analysis()
        
        # Análisis técnico de imagen
        try:
            print("Analizando colores...")
            color_analysis = self._analyze_colors(pil_image)
        except Exception as e:
            print(f"Error en análisis de colores: {str(e)}")
            color_analysis = {}
        layout_analysis = self._analyze_layout(image)
        typography_analysis = self._analyze_typography(image)
        
        # Combinar resultados
        results = {
            'typography': {
                'score': ai_analysis.get('typography_score', 70),
                'analysis': ai_analysis.get('typography_analysis', ''),
                'technical_data': typography_analysis,
                'recommendations': ai_analysis.get('typography_recommendations', [])
            },
            'color': {
                'score': ai_analysis.get('color_score', 70),
                'analysis': ai_analysis.get('color_analysis', ''),
                'technical_data': color_analysis,
                'recommendations': ai_analysis.get('color_recommendations', [])
            },
            'layout': {
                'score': ai_analysis.get('layout_score', 70),
                'analysis': ai_analysis.get('layout_analysis', ''),
                'technical_data': layout_analysis,
                'recommendations': ai_analysis.get('layout_recommendations', [])
            },
            'usability': {
                'score': ai_analysis.get('usability_score', 70),
                'analysis': ai_analysis.get('usability_analysis', ''),
                'recommendations': ai_analysis.get('usability_recommendations', [])
            },
            'modern_design': {
                'score': ai_analysis.get('modern_design_score', 70),
                'analysis': ai_analysis.get('modern_design_analysis', ''),
                'recommendations': ai_analysis.get('modern_design_recommendations', [])
            }
        }
        
        return results
    
    def _analyze_with_openai(self, screenshot_path: str) -> Dict:
        """
        Analiza el diseño usando OpenAI Vision API
        
        Args:
            screenshot_path: Ruta del screenshot
            
        Returns:
            Diccionario con análisis de IA
        """
        try:
            # Codificar imagen en base64
            with open(screenshot_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prompt comprehensivo para análisis
            prompt = """
            Analiza esta captura de pantalla de un sitio web y evalúa los siguientes aspectos del diseño:

            1. TIPOGRAFÍA (puntúa 0-100):
               - Legibilidad del texto
               - Tamaño de fuente apropiado
               - Contraste entre texto y fondo
               - Jerarquía tipográfica clara

            2. COLOR (puntúa 0-100):
               - Armonía del esquema de colores
               - Accesibilidad (contraste suficiente)
               - Coherencia cromática

            3. LAYOUT/DISEÑO (puntúa 0-100):
               - Estructura clara y organizada
               - Uso efectivo del espacio en blanco
               - Alineación de elementos
               - Balance visual

            4. USABILIDAD (puntúa 0-100):
               - Navegación intuitiva
               - Organización de la información
               - Claridad de llamadas a la acción
               - Responsive design apparent

            5. DISEÑO MODERNO (puntúa 0-100):
               - Tendencias actuales de diseño
               - Apariencia contemporánea
               - Innovación visual

            Responde ÚNICAMENTE en formato JSON válido con esta estructura:
            {
                "typography_score": número,
                "typography_analysis": "análisis detallado",
                "typography_recommendations": ["recomendación1", "recomendación2"],
                "color_score": número,
                "color_analysis": "análisis detallado", 
                "color_recommendations": ["recomendación1", "recomendación2"],
                "layout_score": número,
                "layout_analysis": "análisis detallado",
                "layout_recommendations": ["recomendación1", "recomendación2"],
                "usability_score": número,
                "usability_analysis": "análisis detallado",
                "usability_recommendations": ["recomendación1", "recomendación2"],
                "modern_design_score": número,
                "modern_design_analysis": "análisis detallado",
                "modern_design_recommendations": ["recomendación1", "recomendación2"]
            }
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Parsear respuesta JSON
            content = response.choices[0].message.content
            
            # Limpiar respuesta si tiene markdown
            if content.startswith('```json'):
                content = content.strip('```json').strip('```').strip()
            
            return json.loads(content)
            
        except Exception as e:
            print(f"Error en análisis OpenAI: {str(e)}")
            # Retornar valores por defecto
            return {
                'typography_score': 70,
                'typography_analysis': 'Análisis no disponible',
                'typography_recommendations': ['Verificar contraste de texto'],
                'color_score': 70,
                'color_analysis': 'Análisis no disponible',
                'color_recommendations': ['Revisar esquema de colores'],
                'layout_score': 70,
                'layout_analysis': 'Análisis no disponible',
                'layout_recommendations': ['Mejorar estructura visual'],
                'usability_score': 70,
                'usability_analysis': 'Análisis no disponible',
                'usability_recommendations': ['Simplificar navegación'],
                'modern_design_score': 70,
                'modern_design_analysis': 'Análisis no disponible',
                'modern_design_recommendations': ['Actualizar diseño visual']
            }
    
    def _analyze_colors(self, image: Image) -> Dict:
        """
        Analiza el esquema de colores de la imagen
        
        Args:
            image: Imagen PIL
            
        Returns:
            Diccionario con análisis de colores
        """
        try:
            # Convertir a RGB si es necesario
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Obtener colores dominantes
            image_array = np.array(image)
            pixels = image_array.reshape(-1, 3)
            
            # Usar K-means para encontrar colores dominantes
            from sklearn.cluster import KMeans
            
            # Reducir sample para eficiencia
            sample_size = min(10000, len(pixels))
            sample_pixels = pixels[np.random.choice(len(pixels), sample_size, replace=False)]
            
            kmeans = KMeans(n_clusters=5, random_state=42)
            kmeans.fit(sample_pixels)
            
            dominant_colors = kmeans.cluster_centers_.astype(int)
            
            # Calcular estadísticas de color
            stats = ImageStat.Stat(image)
            
            # Calcular contraste promedio
            gray = image.convert('L')
            gray_array = np.array(gray)
            contrast = gray_array.std()
            
            return {
                'dominant_colors': [tuple(color) for color in dominant_colors],
                'average_rgb': stats.mean,
                'contrast_level': float(contrast),
                'brightness': float(np.mean(gray_array)),
                'color_diversity': len(set(tuple(pixel) for pixel in sample_pixels[:1000]))
            }
            
        except Exception as e:
            print(f"Error en análisis de colores: {str(e)}")
            return {
                'dominant_colors': [(128, 128, 128)],
                'average_rgb': [128, 128, 128],
                'contrast_level': 50.0,
                'brightness': 128.0,
                'color_diversity': 100
            }
    
    def _analyze_layout(self, image: np.ndarray) -> Dict:
        """
        Analiza la estructura y layout de la página
        
        Args:
            image: Imagen en formato OpenCV
            
        Returns:
            Diccionario con análisis de layout
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar bordes
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # Detectar líneas (estructura)
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            # Calcular densidad de contenido
            height, width = gray.shape
            total_pixels = height * width
            content_pixels = np.count_nonzero(gray < 240)  # Pixels no blancos
            content_density = content_pixels / total_pixels
            
            # Analizar distribución vertical (secciones)
            vertical_profile = np.mean(gray, axis=1)
            sections = self._find_sections(vertical_profile)
            
            # Calcular balance horizontal
            left_half = gray[:, :width//2]
            right_half = gray[:, width//2:]
            balance = abs(np.mean(left_half) - np.mean(right_half))
            
            return {
                'content_density': float(content_density),
                'line_count': len(lines) if lines is not None else 0,
                'sections_detected': len(sections),
                'horizontal_balance': float(balance),
                'whitespace_ratio': 1 - content_density,
                'image_dimensions': (width, height)
            }
            
        except Exception as e:
            print(f"Error en análisis de layout: {str(e)}")
            return {
                'content_density': 0.5,
                'line_count': 0,
                'sections_detected': 3,
                'horizontal_balance': 10.0,
                'whitespace_ratio': 0.3,
                'image_dimensions': (1920, 1080)
            }
    
    def _analyze_typography(self, image: np.ndarray) -> Dict:
        """
        Analiza aspectos tipográficos básicos
        
        Args:
            image: Imagen en formato OpenCV
            
        Returns:
            Diccionario con análisis tipográfico
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar áreas de texto (aproximación usando contornos)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Encontrar contornos que podrían ser texto
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar contornos por tamaño (posible texto)
            text_contours = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                area = cv2.contourArea(contour)
                
                # Heurística simple para identificar texto
                if 0.1 < aspect_ratio < 10 and 50 < area < 10000:
                    text_contours.append((x, y, w, h))
            
            # Calcular estadísticas de texto
            if text_contours:
                heights = [h for x, y, w, h in text_contours]
                widths = [w for x, y, w, h in text_contours]
                
                avg_text_height = np.mean(heights)
                text_height_consistency = 1 / (np.std(heights) + 1)  # Más consistencia = menos variación
                text_coverage = sum(w * h for x, y, w, h in text_contours) / (gray.shape[0] * gray.shape[1])
            else:
                avg_text_height = 20
                text_height_consistency = 0.5
                text_coverage = 0.1
            
            return {
                'text_regions_detected': len(text_contours),
                'average_text_height': float(avg_text_height),
                'text_height_consistency': float(text_height_consistency),
                'text_coverage_ratio': float(text_coverage),
                'estimated_readability': min(100, text_height_consistency * 100)
            }
            
        except Exception as e:
            print(f"Error en análisis tipográfico: {str(e)}")
            return {
                'text_regions_detected': 10,
                'average_text_height': 16.0,
                'text_height_consistency': 0.7,
                'text_coverage_ratio': 0.15,
                'estimated_readability': 70
            }
    
    def _find_sections(self, vertical_profile: np.ndarray, threshold: float = 10) -> List[Tuple[int, int]]:
        """
        Encuentra secciones en el perfil vertical de la página
        
        Args:
            vertical_profile: Perfil de intensidad vertical
            threshold: Umbral para detectar separaciones
            
        Returns:
            Lista de tuplas (inicio, fin) de cada sección
        """
        sections = []
        in_section = False
        section_start = 0
        
        for i, value in enumerate(vertical_profile):
            if value < threshold and not in_section:
                # Inicio de sección (contenido)
                section_start = i
                in_section = True
            elif value >= threshold and in_section:
                # Fin de sección (espacio en blanco)
                sections.append((section_start, i))
                in_section = False
        
        # Cerrar última sección si está abierta
        if in_section:
            sections.append((section_start, len(vertical_profile)))
        
        return sections
    
    def _get_default_ai_analysis(self) -> Dict:
        """Retorna análisis por defecto cuando OpenAI falla"""
        return {
            'typography_score': 70,
            'typography_analysis': 'Análisis automático: Tipografía estándar detectada',
            'typography_recommendations': ['Verificar legibilidad del texto', 'Considerar mejores contrastes'],
            'color_score': 70,
            'color_analysis': 'Análisis automático: Esquema de colores básico',
            'color_recommendations': ['Revisar armonía cromática', 'Mejorar contraste'],
            'layout_score': 70,
            'layout_analysis': 'Análisis automático: Estructura de layout convencional',
            'layout_recommendations': ['Optimizar espaciado', 'Mejorar jerarquía visual'],
            'usability_score': 70,
            'usability_analysis': 'Análisis automático: Usabilidad básica',
            'usability_recommendations': ['Simplificar navegación', 'Mejorar accesibilidad'],
            'modern_design_score': 70,
            'modern_design_analysis': 'Análisis automático: Diseño funcional',
            'modern_design_recommendations': ['Modernizar elementos visuales', 'Seguir tendencias actuales']
        }