.DEFAULT_GOAL := help
.PHONY: help install lint format test coverage demo build clean

help: ## Show this help
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Install the project and dev tools into .venv
	uv sync

lint: ## Lint, check formatting and type-check
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

format: ## Auto-fix lint issues and format the code
	uv run ruff check --fix .
	uv run ruff format .

test: ## Run the test suite
	uv run pytest

coverage: ## Run the tests with a coverage report
	uv run pytest --cov --cov-report=term-missing

demo: ## Render examples/sample.md (with --toc) and open it in the browser
	uv run md2html examples/sample.md --toc

build: ## Build the sdist and wheel into dist/
	uv build

clean: ## Remove build artifacts and caches
	rm -rf build dist .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
