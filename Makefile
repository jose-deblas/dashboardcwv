.PHONY: help install up down build pull logs clean restart dashboard-shell jobs-shell mysql-shell run-job test lint format

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Core Web Vitals Dashboard - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Initial setup - create .env and install dependencies
	@echo "$(BLUE)Setting up Core Web Vitals Dashboard...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ Created .env file from .env.example$(NC)"; \
		echo "$(YELLOW)⚠ Please update .env with your actual credentials$(NC)"; \
	else \
		echo "$(YELLOW)⚠ .env file already exists$(NC)"; \
	fi
	@mkdir -p logs
	@echo "$(GREEN)✓ Created logs directory$(NC)"
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker compose build
	@echo "$(GREEN)✓ Setup complete! Run 'make up' to start services$(NC)"

up: ## Start all services (MySQL + Dashboard)
	@echo "$(BLUE)Starting services...$(NC)"
	@docker compose up -d mysql dashboard
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo "$(BLUE)Dashboard:$(NC) http://localhost:8501"
	@echo "$(BLUE)MySQL:$(NC) localhost:3306"

down: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	@docker compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

build: ## Build/rebuild Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker compose build
	@echo "$(GREEN)✓ Build complete$(NC)"

pull: ## Pull latest base images
	@echo "$(BLUE)Pulling latest images...$(NC)"
	@docker compose pull
	@echo "$(GREEN)✓ Images updated$(NC)"

logs: ## Show logs from all services (use: make logs SERVICE=dashboard)
ifdef SERVICE
	@docker compose logs -f $(SERVICE)
else
	@docker compose logs -f
endif

clean: ## Remove all containers, volumes, and images
	@echo "$(RED)Warning: This will remove all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Cleaning up...$(NC)"; \
		docker compose down -v --rmi local; \
		rm -rf logs/*; \
		echo "$(GREEN)✓ Cleanup complete$(NC)"; \
	else \
		echo "$(YELLOW)Cleanup cancelled$(NC)"; \
	fi

restart: ## Restart all services
	@echo "$(BLUE)Restarting services...$(NC)"
	@docker compose restart
	@echo "$(GREEN)✓ Services restarted$(NC)"

dashboard-shell: ## Open shell in dashboard container
	@docker compose exec dashboard /bin/bash

jobs-shell: ## Open shell in jobs container (starts if not running)
	@docker compose run --rm jobs /bin/bash

mysql-shell: ## Open MySQL shell
	@docker compose exec mysql mysql -u$${MYSQL_USER:-cwv_user} -p$${MYSQL_PASSWORD:-cwv_password} $${MYSQL_DATABASE:-core_web_vitals}

mysql-create-db-tables: ## Create the MySQL tables executing the schema.sql file
	@echo "$(BLUE)Creating database tables...$(NC)"
	@docker compose exec mysql mysql -u$${MYSQL_USER:-cwv_user} -p$${MYSQL_PASSWORD:-cwv_password} $${MYSQL_DATABASE:-core_web_vitals} < /docker-entrypoint-initdb.d/schema.sql
	@echo "$(GREEN)✓ Database tables created$(NC)"

run-job: ## Run data collection job (use: make run-job JOB=collect_pagespeed_data)
ifdef JOB
	@echo "$(BLUE)Running job: $(JOB)$(NC)"
	@docker compose run --rm jobs python -m src.jobs.$(JOB)
	@echo "$(GREEN)✓ Job completed$(NC)"
else
	@echo "$(RED)Error: Please specify JOB name$(NC)"
	@echo "Example: make run-job JOB=collect_pagespeed_data"
endif

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	@docker compose run --rm dashboard pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete$(NC)"

lint: ## Run linting checks
	@echo "$(BLUE)Running linting checks...$(NC)"
	@docker compose run --rm dashboard ruff check src/ tests/
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	@docker compose run --rm dashboard black src/ tests/
	@echo "$(GREEN)✓ Formatting complete$(NC)"

status: ## Show status of all services
	@docker compose ps
