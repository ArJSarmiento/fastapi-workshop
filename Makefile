# Variables
DOCKER_COMPOSE := docker compose
COMPOSE_FILE := docker-compose.yml
REVISION_NAME ?= init

# Start postgres only
start-db:
	@echo "Starting PostgreSQL..."
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up postgres

# Start application services
start-app:
	@echo "Starting application services..."
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d fastapi

# Initialize database schema
init-schema:
	@echo "Creating database schema..."
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec fastapi alembic revision --autogenerate -m "Create item table"
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec fastapi alembic upgrade head
	@echo "Schema created!"


# Clean up command
clean:
	@echo "Cleaning up..."
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v
	rm -rf db/postgres_data/*