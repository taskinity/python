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

## Generate example markdown with syntax highlighting and flow diagrams
render-examples:
	@echo "Generating example markdown with syntax highlighting and flow diagrams..."
	@mkdir -p examples/markdown
	@echo "# Basic Flow Example" > examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo "This example demonstrates a simple flow with syntax highlighting and flow diagram rendering." >> examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo "## Flow Definition" >> examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo '```' >> examples/markdown/basic_flow.md
	@echo 'flow BasicFlow:' >> examples/markdown/basic_flow.md
	@echo '    description: "Simple data processing flow"' >> examples/markdown/basic_flow.md
	@echo '    fetch_data -> process_data' >> examples/markdown/basic_flow.md
	@echo '    process_data -> analyze_data' >> examples/markdown/basic_flow.md
	@echo '    analyze_data -> visualize_results' >> examples/markdown/basic_flow.md
	@echo '```' >> examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo "## Python Implementation" >> examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo '```python' >> examples/markdown/basic_flow.md
	@echo 'from taskinity import task, run_flow_from_dsl' >> examples/markdown/basic_flow.md
	@echo '' >> examples/markdown/basic_flow.md
	@echo '@task(name="Fetch Data")' >> examples/markdown/basic_flow.md
	@echo 'def fetch_data(url: str):' >> examples/markdown/basic_flow.md
	@echo '    # Implementation' >> examples/markdown/basic_flow.md
	@echo '    return {"data": [1, 2, 3, 4, 5]}' >> examples/markdown/basic_flow.md
	@echo '' >> examples/markdown/basic_flow.md
	@echo '@task(name="Process Data")' >> examples/markdown/basic_flow.md
	@echo 'def process_data(data):' >> examples/markdown/basic_flow.md
	@echo '    # Implementation' >> examples/markdown/basic_flow.md
	@echo '    return {"processed": [x * 2 for x in data["data"]]}' >> examples/markdown/basic_flow.md
	@echo '' >> examples/markdown/basic_flow.md
	@echo '@task(name="Analyze Data")' >> examples/markdown/basic_flow.md
	@echo 'def analyze_data(processed):' >> examples/markdown/basic_flow.md
	@echo '    # Implementation' >> examples/markdown/basic_flow.md
	@echo '    return {' >> examples/markdown/basic_flow.md
	@echo '        "sum": sum(processed["processed"]),' >> examples/markdown/basic_flow.md
	@echo '        "average": sum(processed["processed"]) / len(processed["processed"])' >> examples/markdown/basic_flow.md
	@echo '    }' >> examples/markdown/basic_flow.md
	@echo '' >> examples/markdown/basic_flow.md
	@echo '@task(name="Visualize Results")' >> examples/markdown/basic_flow.md
	@echo 'def visualize_results(sum, average):' >> examples/markdown/basic_flow.md
	@echo '    # Implementation' >> examples/markdown/basic_flow.md
	@echo '    print(f"Sum: {sum}, Average: {average}")' >> examples/markdown/basic_flow.md
	@echo '    return {"visualization": "chart.png"}' >> examples/markdown/basic_flow.md
	@echo '' >> examples/markdown/basic_flow.md
	@echo '# Define flow using DSL' >> examples/markdown/basic_flow.md
	@echo 'flow_dsl = """' >> examples/markdown/basic_flow.md
	@echo 'flow BasicFlow:' >> examples/markdown/basic_flow.md
	@echo '    description: "Simple data processing flow"' >> examples/markdown/basic_flow.md
	@echo '    fetch_data -> process_data' >> examples/markdown/basic_flow.md
	@echo '    process_data -> analyze_data' >> examples/markdown/basic_flow.md
	@echo '    analyze_data -> visualize_results' >> examples/markdown/basic_flow.md
	@echo '"""' >> examples/markdown/basic_flow.md
	@echo '' >> examples/markdown/basic_flow.md
	@echo '# Run the flow' >> examples/markdown/basic_flow.md
	@echo 'results = run_flow_from_dsl(flow_dsl, {"url": "https://example.com/data"})' >> examples/markdown/basic_flow.md
	@echo '```' >> examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo '<script src="https://taskinity.github.io/render/taskinity-render.min.js"></script>' >> examples/markdown/basic_flow.md
	@echo "" >> examples/markdown/basic_flow.md
	@echo "Example markdown generated at examples/markdown/basic_flow.md"
	@echo "To view with syntax highlighting and flow diagrams, open in a browser with the taskinity-render.min.js script."
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
	@read CONFIRM; \
	if [ "$$CONFIRM" = "y" ]; then \
		cd ../render && npm publish; \
	else \
		echo "Publishing canceled"; \
	fi
