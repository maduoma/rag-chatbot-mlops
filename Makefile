# Makefile

.PHONY: run build test

run:
	@echo "Running Flask locally..."
	FLASK_APP=app/ui/flask_app.py flask run

build:
	docker build -t rag-chatbot -f docker/Dockerfile .

compose-up:
	docker-compose -f docker/docker-compose.yml up --build

compose-down:
	docker-compose -f docker/docker-compose.yml down

test:
	pytest --tb=short -q tests/
