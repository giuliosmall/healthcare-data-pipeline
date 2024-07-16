DOCKER_COMPOSE = docker compose

all: build up

build:
	@$(DOCKER_COMPOSE) build

up:
	@$(DOCKER_COMPOSE) up

down:
	@$(DOCKER_COMPOSE) down

rebuild: down build up

logs:
	@$(DOCKER_COMPOSE) logs -f

clean:
	@$(DOCKER_COMPOSE) down -v --remove-orphans

psql:
	@docker exec -it mightydataengineertest-db-1 psql -U user -d mydatabase