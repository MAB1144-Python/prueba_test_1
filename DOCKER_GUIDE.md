# Docker Compose - Guía de Uso

## 🐳 Configuración con Docker

Esta configuración permite ejecutar el Website Design Evaluator en contenedores Docker, eliminando problemas de dependencias y proporcionando un entorno consistente.

## 📋 Prerrequisitos

- Docker Desktop instalado
- Docker Compose (incluido con Docker Desktop)
- Al menos 4GB de RAM disponible
- 2GB de espacio en disco

## 🚀 Inicio Rápido

### 1. Construir las imágenes
```bash
# Windows
.\docker-utils.ps1 build

# Linux/Mac  
./docker-utils.sh build
```

### 2. Evaluar un sitio web
```bash
# Windows
.\docker-utils.ps1 evaluate https://www.google.com

# Linux/Mac
./docker-utils.sh evaluate https://www.google.com
```

## 🎯 Perfiles Disponibles

### Perfil Completo (`full`)
Incluye todos los servicios: evaluador, Redis, MongoDB
```bash
.\docker-utils.ps1 up
```

### Perfil API (`api`)
Para desarrollo de API web (futuro)
```bash
.\docker-utils.ps1 api
```

### Perfil Desarrollo (`dev`)
Incluye Jupyter Lab para análisis interactivo
```bash
.\docker-utils.ps1 dev
# Acceder a: http://localhost:8888
```

### Perfil Monitoreo (`monitoring`)
Prometheus y Grafana para métricas
```bash
.\docker-utils.ps1 monitor
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin:admin123)
```

## 📁 Estructura de Volúmenes

Los siguientes directorios se montan en el contenedor:

```
./screenshots     -> /home/evaluator/app/screenshots
./reports        -> /home/evaluator/app/reports  
./credentials    -> /home/evaluator/app/credentials
./logs          -> /home/evaluator/app/logs
./.env          -> /home/evaluator/app/.env
```

## 🔧 Comandos Disponibles

### Construcción y gestión
```bash
# Construir imágenes
.\docker-utils.ps1 build

# Ver estado de servicios
.\docker-utils.ps1 status

# Ver logs
.\docker-utils.ps1 logs
.\docker-utils.ps1 logs website-evaluator

# Detener servicios
.\docker-utils.ps1 stop

# Limpiar todo (cuidado!)
.\docker-utils.ps1 clean
```

### Evaluación
```bash
# Evaluar sitio individual
.\docker-utils.ps1 evaluate https://ejemplo.com

# Evaluación en lote
.\docker-utils.ps1 batch example_urls.txt

# Ejecutar demo
.\docker-utils.ps1 demo

# Ejecutar pruebas
.\docker-utils.ps1 test
```

## ⚙️ Configuración

### Variables de Entorno
Crear archivo `.env` en la raíz:
```env
OPENAI_API_KEY=sk-tu-api-key
GOOGLE_DRIVE_CREDENTIALS_PATH=credentials/google_drive_credentials.json
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
DROPBOX_ACCESS_TOKEN=tu-token
```

### Credenciales
Colocar archivos de credenciales en `./credentials/`:
- `google_drive_credentials.json`
- `google_sheets_credentials.json`

## 🌐 Servicios y Puertos

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Website Evaluator | - | Servicio principal |
| Web API | 8000 | API REST (futuro) |
| Jupyter Lab | 8888 | Desarrollo interactivo |
| MongoDB | 27017 | Base de datos |
| Redis | 6379 | Cache y cola |
| Prometheus | 9090 | Métricas |
| Grafana | 3000 | Dashboard |

## 📊 Persistencia de Datos

### Volúmenes Docker
- `redis-data`: Datos de Redis
- `mongodb-data`: Base de datos MongoDB  
- `grafana-data`: Configuración de Grafana

### Directorios locales
- `screenshots/`: Capturas de pantalla
- `reports/`: Reportes PDF generados
- `logs/`: Archivos de log

## 🔍 Debugging

### Ver logs en tiempo real
```bash
# Todos los servicios
.\docker-utils.ps1 logs

# Servicio específico
.\docker-utils.ps1 logs website-evaluator
.\docker-utils.ps1 logs mongodb
```

### Ejecutar comandos en contenedor
```bash
# Entrar al contenedor
docker-compose exec website-evaluator bash

# Ejecutar comando específico
docker-compose run --rm website-evaluator python --version
```

### Verificar estado
```bash
# Estado de contenedores
docker-compose ps

# Uso de recursos
docker stats

# Logs del sistema Docker
docker system events
```

## 🐛 Solución de Problemas

### Error: "Chrome not found"
- El Dockerfile instala Chrome automáticamente
- Verificar que la imagen se construyó correctamente

### Error: "Permission denied"
- En Linux/Mac: `chmod +x docker-utils.sh`
- En Windows: ejecutar PowerShell como administrador

### Error: "Port already in use"
```bash
# Ver qué usa el puerto
netstat -tulpn | grep :8000

# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Cambiar puerto externo
```

### Error de memoria
```bash
# Verificar recursos de Docker Desktop
# Aumentar RAM asignada a Docker (mínimo 4GB)

# Limpiar recursos no utilizados
docker system prune -a
```

### MongoDB no inicia
```bash
# Verificar logs
.\docker-utils.ps1 logs mongodb

# Recrear volumen si es necesario
docker-compose down -v
docker volume rm $(docker volume ls -q)
```

## 🚀 Uso en Producción

### Optimizaciones recomendadas

1. **Imagen multi-stage**:
```dockerfile
# Agregar al Dockerfile para reducir tamaño
FROM python:3.11-slim as builder
# ... install dependencies
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```

2. **Configuración de recursos**:
```yaml
# En docker-compose.yml
services:
  website-evaluator:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

3. **Health checks**:
```yaml
# Agregar health check
healthcheck:
  test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 📈 Monitoreo y Métricas

### Prometheus Metrics
- Evaluaciones por minuto
- Tiempo promedio de evaluación
- Errores y fallos
- Uso de recursos

### Grafana Dashboards
- Panel de rendimiento
- Estadísticas de evaluación
- Alertas personalizadas

### Logs Centralizados
```bash
# Configurar log driver
version: '3.8'
services:
  website-evaluator:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
name: Docker Build and Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build and test
      run: |
        docker-compose build
        docker-compose run --rm website-evaluator python tests/test_evaluator.py
```

### Docker Hub Deployment
```bash
# Tag y push automático
docker build -t tu-usuario/website-evaluator:latest .
docker push tu-usuario/website-evaluator:latest
```

## 📚 Recursos Adicionales

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

## 🆘 Soporte

Si encuentras problemas:

1. Verifica logs: `.\docker-utils.ps1 logs`
2. Revisa el estado: `.\docker-utils.ps1 status`
3. Limpia y reconstruye: `.\docker-utils.ps1 clean && .\docker-utils.ps1 build`
4. Reporta issues con logs completos