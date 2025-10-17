"""
Screenshot Capture Module
Maneja la captura automática de screenshots de sitios web
"""

import os
import time
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

class ScreenshotCapture:
    """
    Clase para capturar screenshots de sitios web
    """
    
    def __init__(self, screenshots_dir: str = "screenshots"):
        """
        Inicializa el capturador de screenshots
        
        Args:
            screenshots_dir: Directorio donde guardar las capturas
        """
        self.screenshots_dir = screenshots_dir
        self.ensure_directory_exists()
        self.driver = None
    
    def ensure_directory_exists(self):
        """Asegura que el directorio de screenshots existe"""
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
    
    def setup_driver(self, headless: bool = True, window_size: tuple = (1920, 1080)):
        """
        Configura el driver de Chrome con opciones optimizadas
        
        Args:
            headless: Si ejecutar en modo headless
            window_size: Tamaño de ventana (ancho, alto)
        """
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        # Opciones para mejorar la calidad y velocidad
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        
        # Opciones para reducir advertencias y mejorar rendimiento
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling") 
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-ipc-flooding-protection") 
        
        # Suprimir logs específicos
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--log-level=3")  # Solo errores críticos
        
        # Configurar el servicio con manejo de errores mejorado
        try:
            # Instalar ChromeDriver compatible con Windows
            chrome_driver_path = ChromeDriverManager().install()
            print(f"ChromeDriver instalado en: {chrome_driver_path}")
            service = Service(chrome_driver_path)
            
            # Crear el driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error configurando ChromeDriver: {e}")
            # Intentar con el driver del sistema si está disponible
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                raise Exception(f"No se pudo inicializar ChromeDriver: {e2}")
        self.driver.set_page_load_timeout(30)  # Timeout de 30 segundos
    
    def capture_website(self, url: str, full_page: bool = True, 
                       wait_time: int = 3) -> str:
        """
        Captura screenshot de un sitio web
        
        Args:
            url: URL del sitio web
            full_page: Si capturar toda la página o solo la vista inicial
            wait_time: Tiempo de espera después de cargar la página
            
        Returns:
            Ruta del archivo de screenshot generado
        """
        try:
            # Configurar driver si no existe
            if not self.driver:
                self.setup_driver()
            
            print(f"Navegando a: {url}")
            self.driver.get(url)
            
            # Esperar a que la página cargue
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Tiempo adicional para que se carguen elementos dinámicos
            time.sleep(wait_time)
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = urlparse(url).netloc.replace("www.", "").replace(".", "_")
            filename = f"{domain}_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            if full_page:
                # Captura de página completa
                self._capture_full_page(filepath)
            else:
                # Captura solo de la vista actual
                self.driver.save_screenshot(filepath)
            
            print(f"Screenshot guardado en: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error capturando screenshot: {str(e)}")
            raise
    
    def _capture_full_page(self, filepath: str):
        """
        Captura toda la página web (scroll completo)
        
        Args:
            filepath: Ruta donde guardar el screenshot
        """
        # Obtener dimensiones de la página
        total_width = self.driver.execute_script("return document.body.scrollWidth")
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        viewport_width = self.driver.execute_script("return document.body.clientWidth")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        
        # Configurar el tamaño del viewport para captura completa
        self.driver.set_window_size(total_width, viewport_height)
        
        # Lista para almacenar las capturas parciales
        screenshots = []
        
        # Capturar la página en secciones
        for y in range(0, total_height, viewport_height):
            # Scroll a la posición
            self.driver.execute_script(f"window.scrollTo(0, {y})")
            time.sleep(0.5)  # Pequeña pausa para que se renderice
            
            # Capturar esta sección
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(Image.open(io.BytesIO(screenshot)))
        
        # Combinar todas las capturas en una imagen
        if screenshots:
            # Calcular dimensiones finales
            final_width = screenshots[0].width
            final_height = sum(img.height for img in screenshots)
            
            # Crear imagen final
            final_image = Image.new('RGB', (final_width, final_height))
            
            # Pegar cada captura
            current_height = 0
            for img in screenshots:
                final_image.paste(img, (0, current_height))
                current_height += img.height
            
            # Guardar imagen final
            final_image.save(filepath, 'PNG', quality=95, optimize=True)
        else:
            # Fallback a captura simple
            self.driver.save_screenshot(filepath)
    
    def capture_multiple_sizes(self, url: str, sizes: list = None) -> dict:
        """
        Captura screenshots en múltiples tamaños (para responsive design)
        
        Args:
            url: URL del sitio web
            sizes: Lista de tuplas (ancho, alto) para diferentes tamaños
            
        Returns:
            Diccionario con las rutas de los screenshots por tamaño
        """
        if sizes is None:
            sizes = [
                (1920, 1080),  # Desktop
                (1366, 768),   # Laptop
                (768, 1024),   # Tablet
                (375, 667)     # Mobile
            ]
        
        screenshots = {}
        
        for width, height in sizes:
            try:
                # Configurar tamaño
                if not self.driver:
                    self.setup_driver(window_size=(width, height))
                else:
                    self.driver.set_window_size(width, height)
                
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = urlparse(url).netloc.replace("www.", "").replace(".", "_")
                filename = f"{domain}_{width}x{height}_{timestamp}.png"
                filepath = os.path.join(self.screenshots_dir, filename)
                
                # Navegar y capturar
                self.driver.get(url)
                time.sleep(2)
                self.driver.save_screenshot(filepath)
                
                screenshots[f"{width}x{height}"] = filepath
                print(f"Screenshot {width}x{height} guardado en: {filepath}")
                
            except Exception as e:
                print(f"Error capturando {width}x{height}: {str(e)}")
        
        return screenshots
    
    def close_driver(self):
        """Cierra el driver del navegador"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __del__(self):
        """Destructor para asegurar que el driver se cierre"""
        self.close_driver()


# Importar io para el método _capture_full_page
import io