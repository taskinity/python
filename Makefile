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
	@echo "  example-basic    - Run basic flow example"
	@echo "  example-email    - Run email processing example"
	@echo "  example-data     - Run data processing example"
	@echo "  example-api      - Run API integration example"
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

## Run email processing tests
test-email:
	@echo "Running email processing tests..."
	pytest -xvs /home/tom/github/taskinity/examples/email_processing/tests/

## Run basic flow example
example-basic:
	@echo -e "Running basic flow example..."
	python /home/tom/github/taskinity/examples/basic_flow.py --mock

## Run email processing example
example-email:
	@echo -e "Running email processing example..."
	python /home/tom/github/taskinity/examples/email_flow.py --mock

## Run data processing example
example-data:
	@echo -e "Running data processing example..."
	python /home/tom/github/taskinity/examples/data_flow.py --mock

## Run API integration example
example-api:
	@echo -e "Running API integration example..."
	python /home/tom/github/taskinity/examples/api_flow.py --mock

## Build and publish package to PyPI
publish:
	@echo "Building and publishing package..."
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

## Generate example markdown with syntax highlighting and flow diagrams
render-examples:
	@echo "Generating example markdown with syntax highlighting and flow diagrams..."
	@mkdir -p examples/markdown
	@cat > examples/markdown/basic_flow.md << 'EOL'
# Basic Flow Example

This example demonstrates a simple flow with syntax highlighting and flow diagram rendering.

## Flow Definition

```
flow BasicFlow:
    description: "Simple data processing flow"
    fetch_data -> process_data
    process_data -> analyze_data
    analyze_data -> visualize_results
```

## Python Implementation

```python
from taskinity import task, run_flow_from_dsl

@task(name="Fetch Data")
def fetch_data(url: str):
    # Implementation
    return {"data": [1, 2, 3, 4, 5]}

@task(name="Process Data")
def process_data(data):
    # Implementation
    return {"processed": [x * 2 for x in data["data"]]}

@task(name="Analyze Data")
def analyze_data(processed):
    # Implementation
    return {
        "sum": sum(processed["processed"]),
        "average": sum(processed["processed"]) / len(processed["processed"])
    }

@task(name="Visualize Results")
def visualize_results(sum, average):
    # Implementation
    print(f"Sum: {sum}, Average: {average}")
    return {"visualization": "chart.png"}

# Define flow using DSL
flow_dsl = """
flow BasicFlow:
    description: "Simple data processing flow"
    fetch_data -> process_data
    process_data -> analyze_data
    analyze_data -> visualize_results
"""

# Run the flow
results = run_flow_from_dsl(flow_dsl, {"url": "https://example.com/data"})
```
EOL
	@echo "Example markdown generated at examples/markdown/basic_flow.md"
	@echo "To view with syntax highlighting and flow diagrams, open in a browser with the taskinity-render.min.js script."

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
	@read CONFIRM && if [ $$CONFIRM = "y" ]; then cd ../render && npm publish; else echo "Publishing canceled"; fi
