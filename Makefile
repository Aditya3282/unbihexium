.PHONY: help install install-dev test lint format type-check docs build clean publish

PYTHON := python
PIP := pip

help:
	@echo "Unbihexium Development Commands"
	@echo "================================"
	@echo "install       Install package in production mode"
	@echo "install-dev   Install package with development dependencies"
	@echo "test          Run test suite with pytest"
	@echo "lint          Run ruff linter"
	@echo "format        Format code with ruff"
	@echo "type-check    Run pyright type checker"
	@echo "docs          Build documentation with mkdocs"
	@echo "docs-serve    Serve documentation locally"
	@echo "build         Build distribution packages"
	@echo "clean         Remove build artifacts"
	@echo "publish       Publish to PyPI"
	@echo "validate      Validate all models"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev,test,docs,torch]"

test:
	pytest tests/ -v --cov=src/unbihexium --cov-report=term-missing

test-fast:
	pytest tests/unit -v --ignore=tests/unit/test_zoo_tiny_inference.py

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

type-check:
	pyright src/

docs:
	mkdocs build

docs-serve:
	mkdocs serve

build:
	$(PYTHON) -m build

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

publish:
	$(PYTHON) -m twine upload dist/*

validate:
	$(PYTHON) scripts/validate_models.py

verify:
	$(PYTHON) -c "import unbihexium; print(f'Version: {unbihexium.__version__}')"
	$(PYTHON) -c "from unbihexium.zoo import list_models; print(f'Models: {len(list_models())}')"
