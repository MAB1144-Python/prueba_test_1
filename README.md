# Website Design Evaluator

Una herramienta automatizada para evaluar el diseño de sitios web usando Python, Selenium y OpenAI.

## 🚀 Características

- 📸 Captura automática de pantallas de sitios web
- 🤖 Análisis de diseño usando IA (OpenAI GPT-4 Vision)
- 📊 Sistema de puntuación ponderado (0-100)
- 📄 Generación de reportes PDF profesionales
- ☁️ Almacenamiento en la nube (Google Drive, AWS S3, Dropbox)
- 📋 Integración con Google Sheets
- 🎨 Evaluación de tipografía, colores, layout y usabilidad
- 🐳 Configuración completa con Docker Compose

## 🐳 Instalación con Docker (Recomendada)

### Prerrequisitos
- Docker Desktop instalado
- Al menos 4GB de RAM disponible

### Inicio Rápido
```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/website-design-evaluator.git
cd website-design-evaluator

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 3. Evaluar un sitio web
.\docker-utils-simple.ps1 evaluate https://www.google.com

# En Linux/Mac:
./docker-utils.sh evaluate https://www.google.com
```

### Comandos Docker Disponibles
```bash
# Construir imágenes
.\docker-utils-simple.ps1 build

# Evaluar sitio individual
.\docker-utils-simple.ps1 evaluate https://ejemplo.com

# Evaluación en lote
.\docker-utils-simple.ps1 batch example_urls.txt

# Modo desarrollo con Jupyter
.\docker-utils-simple.ps1 dev

# Ver estado de servicios
.\docker-utils-simple.ps1 status

# Detener servicios
.\docker-utils-simple.ps1 stop
```

## 💻 Instalación Manual

### Prerrequisitos
- Python 3.8+
- Chrome/Chromium instalado

### Instalación Automática
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

### Instalación Manual
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar entorno
python setup.py

# 3. Configurar credenciales
cp .env.example .env
# Editar .env con tus credenciales
```

## ⚙️ Configuración

### Variables de Entorno Mínimas
```env
# Obligatorio para IA
OPENAI_API_KEY=sk-tu-api-key-aqui

# Opcionales para almacenamiento en nube
GOOGLE_DRIVE_CREDENTIALS_PATH=credentials/google_drive_credentials.json
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
DROPBOX_ACCESS_TOKEN=tu_token
```

### Credenciales de Servicios
Ver `credentials/README.md` para instrucciones detalladas de configuración.

## 📖 Uso

### Línea de Comandos
```bash
# Evaluar sitio individual
python main.py https://www.ejemplo.com

# Evaluación en lote
python main.py --batch urls.txt

# Sin servicios en la nube
python main.py https://ejemplo.com --no-cloud --no-sheets

# Ejecutar demo
python demo.py
```

### Uso Programático
```python
from src.website_evaluator import WebsiteEvaluator

evaluator = WebsiteEvaluator()
result = evaluator.evaluate_website("https://ejemplo.com")
print(f"Puntuación: {result['final_score']}/100")
```

## 🔧 Personalización

### Configuración de Puntuación
Edita `config/scoring_config.json`:
```json
{
  "scoring_weights": {
    "typography": {"weight": 0.25},
    "color": {"weight": 0.20},
    "layout": {"weight": 0.25},
    "usability": {"weight": 0.20},
    "modern_design": {"weight": 0.10}
  }
}
```

## 📁 Estructura del Proyecto

```
website-design-evaluator/
├── src/                    # Código fuente principal
│   ├── website_evaluator.py
│   ├── screenshot_capture.py
│   ├── design_analyzer.py
│   ├── cloud_storage.py
│   ├── report_generator.py
│   └── google_sheets_integration.py
├── config/                 # Configuración
│   └── scoring_config.json
├── docker/                 # Archivos Docker
├── credentials/            # Credenciales de servicios
├── screenshots/            # Capturas generadas
├── reports/               # Reportes PDF
├── tests/                 # Pruebas unitarias
├── docker-compose.yml     # Configuración Docker
├── Dockerfile            # Imagen Docker
├── main.py              # Script principal
├── demo.py             # Demostración
└── setup.py           # Configuración inicial
```

## 🐳 Docker Compose

### Perfiles Disponibles
- `full`: Servicios completos (evaluador, MongoDB, Redis)
- `dev`: Modo desarrollo con Jupyter Lab
- `api`: Servicios API (futuro)
- `monitoring`: Prometheus y Grafana

### Servicios Incluidos
| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| website-evaluator | - | Servicio principal |
| jupyter | 8888 | Desarrollo interactivo |
| mongodb | 27017 | Base de datos |
| redis | 6379 | Cache y cola |
| prometheus | 9090 | Métricas |
| grafana | 3000 | Dashboard |

## 🔍 Ejemplos de Uso

### Evaluación Básica
```bash
# Docker
.\docker-utils-simple.ps1 evaluate https://www.apple.com

# Manual
python main.py https://www.apple.com
```

### Evaluación en Lote
```bash
# Crear archivo urls.txt
echo "https://www.google.com
https://www.apple.com
https://www.microsoft.com" > urls.txt

# Ejecutar
.\docker-utils-simple.ps1 batch urls.txt
```

### Modo Desarrollo
```bash
# Iniciar Jupyter Lab
.\docker-utils-simple.ps1 dev
# Acceder a http://localhost:8888
```

## 🧪 Pruebas

```bash
# Docker
.\docker-utils-simple.ps1 test

# Manual
python tests/test_evaluator.py
```

## 📊 Resultados Generados

### Archivos de Salida
- **Screenshots**: `screenshots/sitio_timestamp.png`
- **Reportes PDF**: `reports/report_sitio_timestamp.pdf`
- **Google Sheets**: Hoja "Website Evaluations" (si configurado)
- **Cloud URLs**: Enlaces a screenshots en la nube

### Formato del Reporte
- Portada con screenshot y puntuación
- Resumen ejecutivo
- Análisis detallado por categorías
- Recomendaciones específicas
- Datos técnicos y métricas

## 🔧 Solución de Problemas

### Docker
```bash
# Ver logs
.\docker-utils-simple.ps1 logs

# Reconstruir imágenes
.\docker-utils-simple.ps1 clean
.\docker-utils-simple.ps1 build

# Verificar estado
.\docker-utils-simple.ps1 status
```

### Manual
- Verificar versión de Python: `python --version`
- Verificar Chrome instalado
- Revisar variables de entorno en `.env`
- Ejecutar `python demo.py` para diagnóstico

## 📚 Documentación Adicional

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Guía detallada de uso
- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Documentación completa de Docker
- `credentials/README.md` - Configuración de credenciales

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/website-design-evaluator/issues)
- **Documentación**: Ver archivos `.md` en el proyecto
- **Demo**: Ejecutar `python demo.py` o `.\docker-utils-simple.ps1 demo`




"C:\Users\Inspiron G15\Programacion\test pag\.venv\Scripts\Activate.ps1"

pip install -r requirements.txt

main.py https://www.google.com

pip install webdriver-manager --upgrade

python main.py https://www.google.com --no-cloud --no-sheets