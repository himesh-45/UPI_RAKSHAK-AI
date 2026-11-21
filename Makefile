.PHONY: help install test evaluate seed run docker-up docker-down package demo-offline

help:
	@echo "Available commands:"
	@echo "  make install      Install backend and frontend dependencies"
	@echo "  make seed         Generate dataset, train model, and seed SQLite DB"
	@echo "  make evaluate     Run benchmark suite and generate docs/EVALUATION_REPORT.md"
	@echo "  make test         Run all automated unit, property, and integration tests"
	@echo "  make package      Build clean submission ZIP excluding venv/secrets/node_modules"
	@echo "  make demo-offline Launch app with pre-seeded data in offline mode"
	@echo "  make run          Start backend (:8000) and frontend (:5173)"
	@echo "  make docker-up    Build and start containers with docker-compose"
	@echo "  make docker-down  Stop docker containers"

install:
	python3 -m venv .venv
	.venv/bin/pip install -r backend/requirements.txt
	cd frontend && npm install

seed:
	python3 -m backend.app.scripts.generate_dataset
	python3 -m backend.app.scripts.train_model
	python3 -m backend.app.scripts.generate_demo_assets
	python3 -m backend.app.scripts.seed_db

test:
	.venv/bin/pytest backend/tests -v

evaluate:
	python3 -m backend.app.scripts.evaluate_models

run:
	./run.sh

docker-up:
	docker compose up --build

docker-down:
	docker compose down

package:
	python3 -m backend.app.scripts.package_submission

demo-offline: seed
	./run.sh
