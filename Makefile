# Makefile-like commands for testing

.PHONY: test test-unit test-integration test-coverage test-fast help

help:  ## Show this help message
	@echo "Available commands:"
	@echo "  test              - Run all tests"
	@echo "  test-unit         - Run only unit tests"
	@echo "  test-integration  - Run only integration tests"
	@echo "  test-coverage     - Run tests with coverage report"
	@echo "  test-fast         - Run tests without coverage"
	@echo "  test-verbose      - Run tests with verbose output"

test:  ## Run all tests with coverage
	python -m pytest -v --cov=api --cov-report=term-missing --cov-report=html

test-unit:  ## Run only unit tests
	python -m pytest -v -m unit

test-integration:  ## Run only integration tests  
	python -m pytest -v -m integration

test-coverage:  ## Run tests with detailed coverage
	python -m pytest --cov=api --cov-report=html --cov-report=term-missing --cov-branch

test-fast:  ## Run tests without coverage (faster)
	python -m pytest -v --no-cov

test-verbose:  ## Run tests with maximum verbosity
	python -m pytest -vvs --tb=long

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	python -m pytest --watch

clean:  ## Clean test artifacts
	rm -rf .coverage htmlcov/ .pytest_cache/
