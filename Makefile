# GitHub Topics Tool Makefile
# Provides convenient commands for common operations

# Variables
DOCKER_IMAGE = github-topics:latest
CONFIG_FILE = github-topics.yml
PYTHON_ENTRY = src/main.py

# Default target
.PHONY: help
help: ## Show this help message
	@echo "GitHub Topics Tool - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment Variables:"
	@echo "  GITHUB_TOKEN    Required - GitHub personal access token"
	@echo "  CONFIG_FILE     Optional - Path to config file (default: github-topics.yml)"

# Setup and build commands
.PHONY: build
build: ## Build the Docker image
	@echo "Building Docker image..."
	@./scripts/build-docker.sh

.PHONY: init
init: ## Generate a sample configuration file
	@echo "Generating sample configuration file..."
	@uv run $(PYTHON_ENTRY) --init

# Docker-based commands
.PHONY: run
run: check-token check-config ## Run the tool using Docker with config file
	@echo "Running GitHub Topics Tool with Docker..."
	@docker run --rm \
		-v $(PWD):/workspace \
		-e GITHUB_TOKEN=$(GITHUB_TOKEN) \
		$(DOCKER_IMAGE)

.PHONY: run-dry
run-dry: check-token check-config ## Run in dry-run mode using Docker
	@echo "Running GitHub Topics Tool in dry-run mode..."
	@docker run --rm \
		-v $(PWD):/workspace \
		-e GITHUB_TOKEN=$(GITHUB_TOKEN) \
		$(DOCKER_IMAGE) --dry-run

.PHONY: run-config
run-config: check-token ## Run with specific config file using Docker
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: CONFIG variable required. Usage: make run-config CONFIG=my-config.yml"; \
		exit 1; \
	fi
	@if [ ! -f "$(CONFIG)" ]; then \
		echo "Error: Config file '$(CONFIG)' not found"; \
		exit 1; \
	fi
	@echo "Running GitHub Topics Tool with config: $(CONFIG)"
	@docker run --rm \
		-v $(PWD):/workspace \
		-e GITHUB_TOKEN=$(GITHUB_TOKEN) \
		$(DOCKER_IMAGE) --config $(CONFIG)

# Python-based commands
.PHONY: run-python
run-python: check-token check-config ## Run the tool using Python with config file
	@echo "Running GitHub Topics Tool with Python..."
	@uv run $(PYTHON_ENTRY)

.PHONY: run-python-dry
run-python-dry: check-token check-config ## Run in dry-run mode using Python
	@echo "Running GitHub Topics Tool in dry-run mode with Python..."
	@uv run $(PYTHON_ENTRY) --dry-run

.PHONY: run-python-config
run-python-config: check-token ## Run with specific config file using Python
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: CONFIG variable required. Usage: make run-python-config CONFIG=my-config.yml"; \
		exit 1; \
	fi
	@if [ ! -f "$(CONFIG)" ]; then \
		echo "Error: Config file '$(CONFIG)' not found"; \
		exit 1; \
	fi
	@echo "Running GitHub Topics Tool with Python using config: $(CONFIG)"
	@uv run $(PYTHON_ENTRY) --config $(CONFIG)

# Utility commands
.PHONY: check-token
check-token: ## Check if GITHUB_TOKEN is set
	@if [ -z "$(GITHUB_TOKEN)" ]; then \
		echo "Error: GITHUB_TOKEN environment variable is required"; \
		echo "Set it with: export GITHUB_TOKEN=ghp_YourTokenHere"; \
		echo "Or create a .env file with: GITHUB_TOKEN=ghp_YourTokenHere"; \
		exit 1; \
	fi

.PHONY: check-config
check-config: ## Check if default config file exists
	@if [ ! -f "$(CONFIG_FILE)" ]; then \
		echo "Error: Config file '$(CONFIG_FILE)' not found"; \
		echo "Generate one with: make init"; \
		exit 1; \
	fi

.PHONY: check-docker
check-docker: ## Check if Docker image exists
	@if ! docker image inspect $(DOCKER_IMAGE) >/dev/null 2>&1; then \
		echo "Error: Docker image '$(DOCKER_IMAGE)' not found"; \
		echo "Build it with: make build"; \
		exit 1; \
	fi

.PHONY: clean
clean: ## Remove Docker images and generated files
	@echo "Removing Docker images..."
	-docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	-docker rmi github-topics:$$(date +%Y%m%d) 2>/dev/null || true
	@echo "Cleanup complete"

.PHONY: status
status: ## Show current status of environment and files
	@echo "=== GitHub Topics Tool Status ==="
	@echo "Config file: $(CONFIG_FILE)"
	@if [ -f "$(CONFIG_FILE)" ]; then echo "  ✅ Exists"; else echo "  ❌ Not found"; fi
	@echo "GitHub Token: GITHUB_TOKEN"
	@if [ -n "$(GITHUB_TOKEN)" ]; then echo "  ✅ Set"; else echo "  ❌ Not set"; fi
	@echo "Docker Image: $(DOCKER_IMAGE)"
	@if docker image inspect $(DOCKER_IMAGE) >/dev/null 2>&1; then echo "  ✅ Built"; else echo "  ❌ Not built"; fi
	@echo "Python Environment:"
	@if command -v uv >/dev/null 2>&1; then echo "  ✅ uv available"; else echo "  ❌ uv not found"; fi

# Code quality commands
.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	@uv sync --group dev

.PHONY: lint
lint: ## Run ruff linter
	@echo "Running ruff linter..."
	@uv run --group dev ruff check src/

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	@echo "Running ruff linter with auto-fix..."
	@uv run --group dev ruff check --fix src/

.PHONY: format
format: ## Run ruff formatter
	@echo "Running ruff formatter..."
	@uv run --group dev ruff format src/

.PHONY: format-check
format-check: ## Check if code is formatted correctly
	@echo "Checking code formatting..."
	@uv run --group dev ruff format --check src/

.PHONY: check-all
check-all: format-check lint ## Run all code quality checks

# Development commands
.PHONY: dev-setup
dev-setup: ## Complete development setup
	@echo "Setting up development environment..."
	@if [ ! -f "$(CONFIG_FILE)" ]; then \
		echo "Generating sample config..."; \
		make init; \
	fi
	@echo "Installing development dependencies..."
	make install-dev
	@echo "Building Docker image..."
	make build
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "1. Edit $(CONFIG_FILE) with your repositories"
	@echo "2. Set GITHUB_TOKEN: export GITHUB_TOKEN=ghp_YourToken"
	@echo "3. Run: make run-dry"
	@echo "4. Use: make lint, make format for code quality"