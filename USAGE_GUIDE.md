# Guía Completa de Uso - Website Design Evaluator

## 📋 Tabla de Contenidos

1. [Instalación](#instalación)
2. [Configuración](#configuración)
3. [Uso Básico](#uso-básico)
4. [Funciones Avanzadas](#funciones-avanzadas)
5. [Integración con Servicios](#integración-con-servicios)
6. [Personalización](#personalización)
7. [Solución de Problemas](#solución-de-problemas)

## 🚀 Instalación

### Instalación Automática (Recomendada)

**Windows:**
```batch
git clone https://github.com/tu-usuario/website-design-evaluator.git
cd website-design-evaluator
install.bat
```

**Linux/Mac:**
```bash
git clone https://github.com/tu-usuario/website-design-evaluator.git
cd website-design-evaluator
chmod +x install.sh
./install.sh
```

### Instalación Manual

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/website-design-evaluator.git
cd website-design-evaluator
```

2. **Crear entorno virtual (opcional pero recomendado):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar entorno:**
```bash
python setup.py
```

## ⚙️ Configuración

### 1. Variables de Entorno

Copia `.env.example` a `.env` y configura:

```env
# OpenAI API (Requerida)
OPENAI_API_KEY=sk-tu-api-key-aqui

# Google Drive (Opcional)
GOOGLE_DRIVE_CREDENTIALS_PATH=credentials/google_drive_credentials.json

# Google Sheets (Opcional)  
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials/google_sheets_credentials.json

# AWS S3 (Opcional)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_BUCKET_NAME=tu-bucket-name

# Dropbox (Opcional)
DROPBOX_ACCESS_TOKEN=tu-access-token
```

### 2. Credenciales de Servicios

#### OpenAI (Obligatorio)
1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Crea una API Key
3. Añádela a `.env`

#### Google Drive/Sheets (Opcional)
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto y habilita las APIs de Drive y Sheets
3. Crea credenciales de cuenta de servicio
4. Descarga el JSON y guárdalo en `credentials/`

#### AWS S3 (Opcional)
1. Ve a AWS IAM Console
2. Crea un usuario con acceso programático
3. Asigna política `AmazonS3FullAccess`
4. Configura las credenciales en `.env`

#### Dropbox (Opcional)
1. Ve a [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Crea una aplicación y genera un Access Token
3. Configura el token en `.env`

## 📖 Uso Básico

### Evaluación de un Solo Sitio

```bash
python main.py https://www.ejemplo.com
```

### Evaluación en Lote

1. **Crear archivo de URLs:**
```
https://www.google.com
https://www.apple.com  
https://www.microsoft.com
```

2. **Ejecutar evaluación:**
```bash
python main.py --batch urls.txt
```

### Opciones de Comando

```bash
# Sin guardar en nube ni sheets
python main.py https://ejemplo.com --no-cloud --no-sheets

# Configuración personalizada
python main.py https://ejemplo.com --config mi_config.json

# Modo verbose
python main.py https://ejemplo.com --verbose

# Directorio personalizado para reportes
python main.py https://ejemplo.com --output-dir /ruta/personalizada
```

## 🔧 Funciones Avanzadas

### Demostración Interactiva

```bash
python demo.py
```

### Ejecutar Pruebas

```bash
python tests/test_evaluator.py
```

### Uso Programático

```python
from src.website_evaluator import WebsiteEvaluator

# Crear evaluador
evaluator = WebsiteEvaluator()

# Evaluar sitio
result = evaluator.evaluate_website("https://ejemplo.com")

print(f"Puntuación: {result['final_score']}/100")
```

### Evaluación Solo de Screenshot

```python
from src.screenshot_capture import ScreenshotCapture

capturer = ScreenshotCapture()
screenshot_path = capturer.capture_website("https://ejemplo.com")
print(f"Screenshot guardado: {screenshot_path}")
capturer.close_driver()
```

### Análisis de Imagen Existente

```python
from src.design_analyzer import DesignAnalyzer
import json

# Cargar configuración
with open('config/scoring_config.json', 'r') as f:
    config = json.load(f)

analyzer = DesignAnalyzer(config)
results = analyzer.analyze_design("screenshot.png", "https://ejemplo.com")
```

## ☁️ Integración con Servicios

### Google Sheets Automático

Los resultados se guardan automáticamente en una hoja llamada "Website Evaluations" con:
- Timestamp, URL, puntuaciones por categoría
- Análisis y recomendaciones
- Enlaces a screenshots en la nube
- Datos técnicos

### Almacenamiento en la Nube

Los screenshots se suben automáticamente a:
1. **Google Drive** (preferido)
2. **AWS S3** (fallback)
3. **Dropbox** (fallback)

### Reportes PDF

Cada evaluación genera un reporte PDF profesional con:
- Portada con screenshot y puntuación
- Resumen ejecutivo
- Análisis detallado por categorías
- Recomendaciones específicas
- Datos técnicos

## 🎨 Personalización

### Configuración de Puntuación

Edita `config/scoring_config.json` para personalizar:

```json
{
  "scoring_weights": {
    "typography": {"weight": 0.30},    // Aumentar importancia
    "color": {"weight": 0.20},
    "layout": {"weight": 0.25}, 
    "usability": {"weight": 0.20},
    "modern_design": {"weight": 0.05}  // Reducir importancia
  }
}
```

### Prompts de IA Personalizados

Modifica los prompts en `analysis_prompts` para análisis específicos:

```json
{
  "analysis_prompts": {
    "typography": "Analiza específicamente la legibilidad para usuarios mayores..."
  }
}
```

### Rangos de Puntuación Personalizados

```json
{
  "score_ranges": {
    "excellent": {"min": 95, "max": 100, "color": "#00FF00"},
    "custom_range": {"min": 75, "max": 94, "color": "#FFAA00"}
  }
}
```

## 🔍 Solución de Problemas

### Errores Comunes

#### "ChromeDriver not found"
```bash
# Instalar manualmente
pip install webdriver-manager
```

#### "OpenAI API key not found"
- Verifica que `.env` existe y contiene `OPENAI_API_KEY`
- Asegúrate de que la API key es válida

#### "Google credentials not found"
- Verifica que el archivo JSON existe en `credentials/`
- Comprueba que las APIs están habilitadas en Google Cloud

#### "Module not found"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Depuración

#### Modo Verbose
```bash
python main.py https://ejemplo.com --verbose
```

#### Logs Detallados
Activa logging en el código:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Verificar Instalación
```bash
python demo.py
```

### Limitaciones Conocidas

1. **Selenium WebDriver**: Requiere Chrome instalado
2. **OpenAI API**: Limitaciones de rate limit y costo
3. **Análisis de Imagen**: Requiere buena calidad de screenshot
4. **Servicios de Nube**: Dependen de conectividad a internet

### Rendimiento

#### Optimizar Velocidad
- Usar `--no-cloud` para evaluaciones locales rápidas
- Configurar timeout más bajo en `screenshot_capture.py`
- Evaluar en lotes para eficiencia

#### Reducir Costos de OpenAI
- Usar modelo más económico en `design_analyzer.py`
- Cachear resultados para sitios repetidos
- Implementar análisis básico sin IA como fallback

## 📞 Soporte

### Reportar Problemas
1. Ejecuta `python demo.py` para diagnosticar
2. Incluye logs de error completos
3. Especifica sistema operativo y versión de Python

### Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature
3. Añade tests para nuevas funcionalidades
4. Envía pull request

### Roadmap
- [ ] Análisis de performance web
- [ ] Soporte para más formatos de imagen
- [ ] API REST para integraciones
- [ ] Dashboard web interactivo
- [ ] Análisis de accesibilidad mejorado