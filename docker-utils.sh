#!/bin/bash
# Scripts de utilidad para Docker Compose

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}Website Design Evaluator - Docker Utility${NC}"
    echo "=========================================="
    echo
    echo "Uso: $0 [COMANDO] [OPCIONES]"
    echo
    echo "Comandos disponibles:"
    echo "  build       - Construir las imágenes Docker"
    echo "  up          - Iniciar servicios completos"
    echo "  dev         - Iniciar modo desarrollo (con Jupyter)"
    echo "  api         - Iniciar solo API y dependencias"
    echo "  evaluate    - Ejecutar evaluación de un sitio"
    echo "  batch       - Ejecutar evaluación en lote"
    echo "  demo        - Ejecutar demostración"
    echo "  test        - Ejecutar pruebas"
    echo "  logs        - Ver logs de servicios"
    echo "  stop        - Detener todos los servicios"
    echo "  clean       - Limpiar contenedores y volúmenes"
    echo "  monitor     - Iniciar servicios de monitoreo"
    echo "  status      - Ver estado de servicios"
    echo
    echo "Ejemplos:"
    echo "  $0 evaluate https://www.google.com"
    echo "  $0 batch example_urls.txt"
    echo "  $0 up"
    echo "  $0 dev"
}

# Función para construir imágenes
build() {
    echo -e "${BLUE}🔨 Construyendo imágenes Docker...${NC}"
    docker-compose build
    echo -e "${GREEN}✅ Imágenes construidas exitosamente${NC}"
}

# Función para iniciar servicios completos
up() {
    echo -e "${BLUE}🚀 Iniciando servicios completos...${NC}"
    docker-compose --profile full up -d
    echo -e "${GREEN}✅ Servicios iniciados${NC}"
    echo -e "${YELLOW}📊 MongoDB: http://localhost:27017${NC}"
    echo -e "${YELLOW}🔥 Redis: localhost:6379${NC}"
}

# Función para modo desarrollo
dev() {
    echo -e "${BLUE}💻 Iniciando modo desarrollo...${NC}"
    docker-compose --profile dev up -d
    echo -e "${GREEN}✅ Modo desarrollo iniciado${NC}"
    echo -e "${YELLOW}📓 Jupyter Lab: http://localhost:8888${NC}"
}

# Función para API
api() {
    echo -e "${BLUE}🌐 Iniciando servicios API...${NC}"
    docker-compose --profile api up -d
    echo -e "${GREEN}✅ Servicios API iniciados${NC}"
    echo -e "${YELLOW}🔗 API: http://localhost:8000${NC}"
}

# Función para evaluación individual
evaluate() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Error: URL requerida${NC}"
        echo "Uso: $0 evaluate <URL>"
        exit 1
    fi
    
    echo -e "${BLUE}🔍 Evaluando: $1${NC}"
    docker-compose run --rm website-evaluator python main.py "$1"
}

# Función para evaluación en lote
batch() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Error: Archivo de URLs requerido${NC}"
        echo "Uso: $0 batch <archivo_urls>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        echo -e "${RED}❌ Error: Archivo no encontrado: $1${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📋 Evaluación en lote desde: $1${NC}"
    docker-compose run --rm website-evaluator python main.py --batch "$1"
}

# Función para demo
demo() {
    echo -e "${BLUE}🎬 Ejecutando demostración...${NC}"
    docker-compose run --rm website-evaluator python demo.py
}

# Función para pruebas
test() {
    echo -e "${BLUE}🧪 Ejecutando pruebas...${NC}"
    docker-compose run --rm website-evaluator python tests/test_evaluator.py
}

# Función para ver logs
logs() {
    if [ -z "$1" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$1"
    fi
}

# Función para detener servicios
stop() {
    echo -e "${BLUE}⏹️  Deteniendo servicios...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Servicios detenidos${NC}"
}

# Función para limpiar
clean() {
    echo -e "${YELLOW}⚠️  ¿Estás seguro que quieres limpiar todos los contenedores y volúmenes? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${BLUE}🧹 Limpiando contenedores y volúmenes...${NC}"
        docker-compose down -v --remove-orphans
        docker system prune -f
        echo -e "${GREEN}✅ Limpieza completada${NC}"
    else
        echo -e "${YELLOW}Operación cancelada${NC}"
    fi
}

# Función para monitoreo
monitor() {
    echo -e "${BLUE}📊 Iniciando servicios de monitoreo...${NC}"
    docker-compose --profile monitoring up -d
    echo -e "${GREEN}✅ Servicios de monitoreo iniciados${NC}"
    echo -e "${YELLOW}📈 Prometheus: http://localhost:9090${NC}"
    echo -e "${YELLOW}📊 Grafana: http://localhost:3000 (admin:admin123)${NC}"
}

# Función para estado
status() {
    echo -e "${BLUE}📋 Estado de servicios:${NC}"
    docker-compose ps
}

# Parsear comando
case "$1" in
    build)
        build
        ;;
    up)
        up
        ;;
    dev)
        dev
        ;;
    api)
        api
        ;;
    evaluate)
        evaluate "$2"
        ;;
    batch)
        batch "$2"
        ;;
    demo)
        demo
        ;;
    test)
        test
        ;;
    logs)
        logs "$2"
        ;;
    stop)
        stop
        ;;
    clean)
        clean
        ;;
    monitor)
        monitor
        ;;
    status)
        status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando desconocido: $1${NC}"
        echo
        show_help
        exit 1
        ;;
esac