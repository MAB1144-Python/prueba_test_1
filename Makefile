# Makefile para Website Design Evaluator Docker

.PHONY: help build up dev api evaluate batch demo test logs stop clean monitor status

# Variables
DOCKER_COMPOSE = docker-compose
URL ?= https://www.google.com
BATCH_FILE ?= example_urls.txt

# Colores para output
BLUE = \033[0;34m
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(BLUE)Website Design Evaluator - Docker Commands$(NC)"
	@echo "==========================================="
	@echo ""
	@echo "Comandos disponibles:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-12s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Ejemplos:"
	@echo "  make evaluate URL=https://www.google.com"
	@echo "  make batch BATCH_FILE=urls.txt"
	@echo "  make up"

build: ## Construir las imágenes Docker
	@echo "$(BLUE)🔨 Construyendo imágenes Docker...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✅ Imágenes construidas exitosamente$(NC)"

up: ## Iniciar servicios completos
	@echo "$(BLUE)🚀 Iniciando servicios completos...$(NC)"
	$(DOCKER_COMPOSE) --profile full up -d
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@echo "$(YELLOW)📊 MongoDB: http://localhost:27017$(NC)"
	@echo "$(YELLOW)🔥 Redis: localhost:6379$(NC)"

dev: ## Iniciar modo desarrollo con Jupyter
	@echo "$(BLUE)💻 Iniciando modo desarrollo...$(NC)"
	$(DOCKER_COMPOSE) --profile dev up -d
	@echo "$(GREEN)✅ Modo desarrollo iniciado$(NC)"
	@echo "$(YELLOW)📓 Jupyter Lab: http://localhost:8888$(NC)"

api: ## Iniciar servicios API
	@echo "$(BLUE)🌐 Iniciando servicios API...$(NC)"
	$(DOCKER_COMPOSE) --profile api up -d
	@echo "$(GREEN)✅ Servicios API iniciados$(NC)"
	@echo "$(YELLOW)🔗 API: http://localhost:8000$(NC)"

evaluate: ## Evaluar un sitio web (make evaluate URL=https://ejemplo.com)
	@echo "$(BLUE)🔍 Evaluando: $(URL)$(NC)"
	$(DOCKER_COMPOSE) run --rm website-evaluator python main.py $(URL)

batch: ## Evaluación en lote (make batch BATCH_FILE=urls.txt)
	@echo "$(BLUE)📋 Evaluación en lote desde: $(BATCH_FILE)$(NC)"
	@if [ ! -f "$(BATCH_FILE)" ]; then \
		echo "$(RED)❌ Error: Archivo no encontrado: $(BATCH_FILE)$(NC)"; \
		exit 1; \
	fi
	$(DOCKER_COMPOSE) run --rm website-evaluator python main.py --batch $(BATCH_FILE)

demo: ## Ejecutar demostración
	@echo "$(BLUE)🎬 Ejecutando demostración...$(NC)"
	$(DOCKER_COMPOSE) run --rm website-evaluator python demo.py

test: ## Ejecutar pruebas
	@echo "$(BLUE)🧪 Ejecutando pruebas...$(NC)"
	$(DOCKER_COMPOSE) run --rm website-evaluator python tests/test_evaluator.py

logs: ## Ver logs de todos los servicios
	$(DOCKER_COMPOSE) logs -f

logs-evaluator: ## Ver logs solo del evaluador
	$(DOCKER_COMPOSE) logs -f website-evaluator

logs-mongodb: ## Ver logs de MongoDB
	$(DOCKER_COMPOSE) logs -f mongodb

logs-redis: ## Ver logs de Redis
	$(DOCKER_COMPOSE) logs -f redis

stop: ## Detener todos los servicios
	@echo "$(BLUE)⏹️  Deteniendo servicios...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

clean: ## Limpiar contenedores y volúmenes (¡CUIDADO!)
	@echo "$(YELLOW)⚠️  ¿Estás seguro que quieres limpiar todos los contenedores y volúmenes? [y/N]$(NC)"
	@read response; \
	if [ "$$response" = "y" ] || [ "$$response" = "Y" ]; then \
		echo "$(BLUE)🧹 Limpiando contenedores y volúmenes...$(NC)"; \
		$(DOCKER_COMPOSE) down -v --remove-orphans; \
		docker system prune -f; \
		echo "$(GREEN)✅ Limpieza completada$(NC)"; \
	else \
		echo "$(YELLOW)Operación cancelada$(NC)"; \
	fi

monitor: ## Iniciar servicios de monitoreo
	@echo "$(BLUE)📊 Iniciando servicios de monitoreo...$(NC)"
	$(DOCKER_COMPOSE) --profile monitoring up -d
	@echo "$(GREEN)✅ Servicios de monitoreo iniciados$(NC)"
	@echo "$(YELLOW)📈 Prometheus: http://localhost:9090$(NC)"
	@echo "$(YELLOW)📊 Grafana: http://localhost:3000 (admin:admin123)$(NC)"

status: ## Ver estado de servicios
	@echo "$(BLUE)📋 Estado de servicios:$(NC)"
	$(DOCKER_COMPOSE) ps

shell: ## Entrar al contenedor del evaluador
	$(DOCKER_COMPOSE) run --rm website-evaluator bash

# Comandos de desarrollo
dev-install: ## Instalar dependencias en modo desarrollo
	$(DOCKER_COMPOSE) run --rm website-evaluator pip install -e .

dev-test-watch: ## Ejecutar pruebas en modo watch
	$(DOCKER_COMPOSE) run --rm website-evaluator python -m pytest tests/ -f

# Comandos de producción
prod-up: ## Iniciar en modo producción
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-build: ## Construir imagen de producción
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml build

# Comandos de backup
backup-db: ## Hacer backup de MongoDB
	@echo "$(BLUE)💾 Creando backup de MongoDB...$(NC)"
	docker exec evaluator-mongodb mongodump --out /data/backup/$(shell date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)✅ Backup completado$(NC)"

restore-db: ## Restaurar MongoDB desde backup (BACKUP_PATH=path/to/backup)
	@if [ -z "$(BACKUP_PATH)" ]; then \
		echo "$(RED)❌ Error: Especifica BACKUP_PATH$(NC)"; \
		echo "Uso: make restore-db BACKUP_PATH=path/to/backup"; \
		exit 1; \
	fi
	@echo "$(BLUE)♻️  Restaurando MongoDB desde: $(BACKUP_PATH)$(NC)"
	docker exec evaluator-mongodb mongorestore $(BACKUP_PATH)
	@echo "$(GREEN)✅ Restauración completada$(NC)"

# Comandos de utilidad
ps: ## Mostrar procesos Docker
	docker ps -a

images: ## Mostrar imágenes Docker
	docker images

volumes: ## Mostrar volúmenes Docker
	docker volume ls

networks: ## Mostrar redes Docker
	docker network ls

system-info: ## Información del sistema Docker
	docker system df
	docker system info

# Por defecto mostrar ayuda
.DEFAULT_GOAL := help