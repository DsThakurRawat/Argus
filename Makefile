# Makefile for quality gates and development tasks

.PHONY: help install test lint format type-check security quality-gates clean

# Default target
help:
	@echo "Available targets:"
	@echo "  install          Install dependencies"
	@echo "  test             Run tests with coverage"
	@echo "  lint             Run linting (ruff)"
	@echo "  format           Format code (ruff)"
	@echo "  type-check       Run type checking (pyright)"
	@echo "  security         Run security scan (bandit)"
	@echo "  quality-gates    Run all quality gates"
	@echo "  quality-gates-quick  Run quick quality gates (static analysis only)"
	@echo "  quality-gates-full    Run full quality gates with all checks"
	@echo "  clean            Clean up generated files"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install ruff pyright bandit safety pytest-cov pre-commit

# Run tests with coverage
test:
	pytest --cov=argus --cov-report=xml --cov-report=html --cov-fail-under=80

# Run linting
lint:
	ruff check argus tests

# Format code
format:
	ruff format argus tests

# Run type checking
type-check:
	pyright --strict

# Run security scan
security:
	bandit -r argus -f json -o bandit-report.json
	bandit -r argus

# Run quick quality gates (static analysis only)
quality-gates-quick:
	python -m argus.core.quality.cli run \
		--gates=static_analysis,style \
		--output=quality-report-quick.json \
		--format=json

# Run full quality gates
quality-gates-full:
	python -m argus.core.quality.cli run \
		--output=quality-report-full.json \
		--format=json \
		--fail-on-warning

# Run all quality gates (default)
quality-gates:
	python -m argus.core.quality.cli run \
		--output=quality-report.json \
		--format=console

# Install pre-commit hooks
install-hooks:
	pre-commit install

# Run pre-commit on all files
pre-commit-all:
	pre-commit run --all-files

# Clean up generated files
clean:
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .pyright_cache/
	rm -rf quality-report*.json
	rm -rf bandit-report.json
	rm -rf .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Development setup
dev-setup: install install-hooks
	@echo "Development environment setup complete!"
	@echo "Run 'make quality-gates' to check code quality"

# CI/CD pipeline simulation
ci: clean quality-gates-full test security
	@echo "CI pipeline completed successfully!"

# Quick development check
dev-check: format lint type-check
	@echo "Quick development check completed!"
