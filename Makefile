.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:	## Build project with docker compose
	docker-compose build


.PHONY: up
up:	## Run project with docker compose
	docker-compose up --build --remove-orphans web


.PHONY: down
down: ## Reset project containers with docker compose
	docker-compose down

.PHONY: clean
clean: ## Clean Reset project containers with docker compose
	docker-compose down -v --remove-orphans

.PHONY: test
test:	## Run project tests and coverage with tox runner
	docker-compose run --rm web tox
