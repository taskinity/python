# Makefile for Taskinity DSL examples and tests

.PHONY: help install test test-basic test-email example-basic example-email example-data example-api publish version docs docs-preview render-examples render-test render-install render-publish

## Display help information
help:
	@echo "Taskinity DSL Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  help             - Display this help message"
	@echo "  install          - Install dependencies"
	@echo "  test             - Run all tests"
	@echo "  test-basic       - Run basic tests"
	@echo "  test-email       - Run email processing tests"
	@echo "  publish          - Build and publish package to PyPI"
	@echo "  version          - Bump package version (patch, minor, major)"
	@echo "  docs             - Generate documentation"
	@echo "  docs-preview     - Preview documentation in browser"
	@echo "  render-examples  - Generate example markdown with syntax highlighting and flow diagrams"
	@echo "  render-test      - Test render package"
	@echo "  render-install   - Install render package dependencies"
	@echo "  render-publish   - Publish render package to npm"

## Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

## Run all tests
test:
	@echo "Running all tests..."
	pytest -xvs tests/

## Run basic tests
test-basic:
	@echo "Running basic tests..."
	pytest -xvs tests/test_basic.py

## Push changes to GitHub
push:
	@echo "Staging all changes..."
	git add .
	@echo "Enter commit message: "
	@read MSG && git commit -m "$$MSG"
	@echo "Pushing to GitHub..."
	git push
	@echo "Successfully pushed changes to GitHub!"


## Build and publish package to PyPI
publish:
	@echo "Building and publishing package..."
	poetry version patch
	poetry build
	poetry publish

## Bump package version (patch, minor, major)
version:
	@echo "Current version: $$(poetry version -s)"
	@echo "Specify version bump type (patch, minor, major):"
	@read TYPE && poetry version $$TYPE
	@echo "New version: $$(poetry version -s)"

## Generate documentation
docs:
	@echo "Generating documentation..."
	mkdocs build

## Preview documentation in browser
docs-preview:
	@echo "Starting documentation server..."
	mkdocs serve

## Test render package
render-test:
	@echo "Testing render package..."
	cd ../render && npm test

## Install render package dependencies
render-install:
	@echo "Installing render package dependencies..."
	cd ../render && npm install

## Publish render package to npm
render-publish:
	@echo "Building and publishing render package to npm..."
	cd ../render && npm run build
	@echo "Do you want to publish to npm? (y/n)"
	@read CONFIRM; \
	if [ "$$CONFIRM" = "y" ]; then \
		cd ../render && npm publish; \
	else \
		echo "Publishing canceled"; \
	fi
