# Taskinity - Intelligent Task Orchestration Framework

Taskinity is a modern framework for defining, managing, and monitoring task flows using an intuitive DSL and Python decorators. Designed with simplicity and efficiency in mind, Taskinity offers significantly less overhead than Prefect, Airflow, or Luigi, working instantly without complicated configuration.

![Taskinity Logo](./assets/taskinity-logo.svg)

## Mission

Our mission is to provide a simple yet powerful task orchestration tool that allows teams to focus on business logic rather than infrastructure management. We believe workflow automation should be accessible to everyone, regardless of team size or budget.

## Strategy

Taskinity achieves its mission through:

1. **Ease of use** - intuitive interface and minimal configuration
2. **Scalability** - from simple scripts to complex production workflows
3. **Flexibility** - easy integration with existing systems and tools
4. **Transparency** - full visibility of task status and execution history
5. **Reliability** - fault tolerance and automatic recovery mechanisms

## Navigation Menu

- [Documentation](./docs/documentation.md) - Complete technical documentation
- [Tutorial](./docs/tutorial.md) - Step-by-step introduction to Taskinity
- [Examples](./examples/README.md) - Ready-to-use flow examples
- [FAQ](./docs/faq.md) - Frequently asked questions
- [Troubleshooting](./docs/troubleshooting.md) - Help with solving problems

## Table of Contents

- [Advantages of Taskinity](#advantages-of-taskinity)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [DSL Specification](#dsl-specification)
- [Examples](#examples)
- [Flow Visualization](#flow-visualization)
- [Monitoring and Logs](#monitoring-and-logs)
- [Comparison with Other Frameworks](#comparison-with-other-frameworks)
- [Dashboard](#dashboard)
- [Notifications](#notifications)
- [Parallel Execution](#parallel-execution)
- [Flow Scheduling](#flow-scheduling)
- [API Reference](#api-reference)
- [Extensions and Plugins](#extensions-and-plugins)

## Advantages of Taskinity

- **Simplicity** - minimal feature set, easy to understand and extend
- **Decorators** - intuitive way to define tasks and flows
- **DSL** - readable language for defining connections between tasks
- **Zero-config** - works immediately without complicated setup
- **Advanced monitoring** - automatic logging and execution tracking with metrics
- **Visualization** - interactive tools for flow visualization
- **Data validation** - built-in mechanisms for input and output data validation
- **Parallel execution** - automatic flow optimization for better performance
- **Reproducibility** - full execution history and ability to recreate flows
- **Modularity** - core functionality with optional extensions
- **Data processing** - built-in tools for various data sources
- **API integration** - easy connection to external services

## Quick Start

### Installation

```bash
# Installation with pip
pip install taskinity

# OR installation with poetry
poetry add taskinity

# Run example
python -m examples.basic_flow
```

### Using with GitHub Pages

To enable syntax highlighting and flow diagram rendering in your Markdown files, simply add this script tag at the end of your Markdown file:

```html
<script src="https://taskinity.github.io/render/taskinity-render.min.js"></script>
```

This will automatically:
- Highlight syntax in all code blocks
- Render flow diagrams for DSL code blocks
- Add copy buttons to code blocks
- Add line numbers to code blocks

#### Example GitHub README.md

````markdown
# My Taskinity Project

This project uses Taskinity for workflow automation.

## Flow Definition

```
flow DataProcessing:
    description: "Data Processing Flow"
    fetch_data -> process_data
    process_data -> analyze_data
```

## Implementation

```python
from taskinity import task, run_flow_from_dsl

@task(name="Fetch Data")
def fetch_data():
    return {"data": [1, 2, 3, 4, 5]}

@task(name="Process Data")
def process_data(data):
    return {"processed": [x * 2 for x in data["data"]]}
```

<!-- Add this at the end of your README.md -->
<script src="https://taskinity.github.io/render/taskinity-render.min.js"></script>
````

### Basic Usage

```python
from taskinity import task, run_flow_from_dsl

# Define tasks
@task(name="Fetch Data")
def fetch_data(url: str):
    # Implementation
    return data

@task(name="Process Data")
def process_data(data):
    # Implementation
    return processed_data

# Define flow using DSL
flow_dsl = """
flow DataProcessing:
    description: "Data Processing Flow"
    fetch_data -> process_data
"""

# Run the flow
results = run_flow_from_dsl(flow_dsl, {"url": "https://example.com/data"})
```

## Project Structure

Taskinity follows a modular architecture for better organization and extensibility:

### Core Module

The core module (`taskinity/core/`) contains the essential functionality:

- Task and flow decorators
- DSL parser and executor
- Flow management utilities
- Registry and execution tracking

### Extensions

Optional extensions enhance Taskinity with additional features:

- **Visualization** - Convert flows to Mermaid diagrams and export to SVG/PNG
- **Code Converter** - Convert existing Python code to Taskinity flows
- **Data Processors** - Tools for working with CSV, JSON, and databases
- **API Clients** - Clients for REST, GraphQL, and WebSocket APIs

## DSL Specification

### Syntax Elements:

- **flow [FlowName]:** - Flow definition with name
- **description:** - Optional flow description
- **[source_task] -> [target_task]** - Definition of connection between tasks
- **[source_task] -> [task1, task2]** - Connect one task to multiple tasks

### Example:

```
flow EmailProcessing:
    description: "Email Processing Flow"
    fetch_emails -> classify_emails
    classify_emails -> process_urgent_emails
    classify_emails -> process_regular_emails
    process_urgent_emails -> send_responses
    process_regular_emails -> send_responses
```

## Examples

Taskinity includes a variety of examples in the `examples` directory. Each example is self-contained with its own README, configuration files, and Docker setup where applicable.

### Email Processing

```python
from taskinity import task, run_flow_from_dsl

@task(name="Fetch Emails")
def fetch_emails(server, username, password):
    # Implementation
    return ["Email 1", "Email 2"]

@task(name="Classify Emails")
def classify_emails(emails):
    # Implementation
    urgent = [e for e in emails if "URGENT" in e]
    regular = [e for e in emails if "URGENT" not in e]
    return {"urgent_emails": urgent, "regular_emails": regular}

# Flow definition using DSL
email_dsl = """
flow EmailProcessing:
    description: "Email Processing Flow"
    fetch_emails -> classify_emails
    classify_emails -> process_urgent_emails
    classify_emails -> process_regular_emails
"""
```

### Data Analysis with Validation

```python
from taskinity import task, run_flow_from_dsl

def validate_input_data(data):
    if not isinstance(data, list):
        raise ValueError("Input data must be a list")

@task(name="Analyze Data", validate_input=validate_input_data)
def analyze_data(data):
    return {"summary": sum(data), "average": sum(data) / len(data)}
```

## Flow Visualization

Taskinity includes simple tools for flow visualization:

```python
# Visualize DSL definition
python visualize_flow.py dsl --file email_processing.dsl --output flow_diagram.png

# Visualize flow execution history
python visualize_flow.py flow [flow_id] --output execution_diagram.png
```

**Example ASCII diagram:**
```
=== EmailProcessing ===

[fetch_emails]
[classify_emails]
[process_urgent_emails]
[process_regular_emails]
[send_responses]

Connections:
fetch_emails --> classify_emails
classify_emails --> process_urgent_emails
classify_emails --> process_regular_emails
process_urgent_emails --> send_responses
process_regular_emails --> send_responses
```

## Monitoring and Logs

Taskinity automatically saves flow execution logs in the `logs/` directory. They can be easily viewed using standard tools:

```python
# View logs for a specific flow
import json
from pathlib import Path

def view_flow_logs(flow_id):
    flow_file = Path("flows") / f"{flow_id}.json"
    if flow_file.exists():
        with open(flow_file, "r") as f:
            flow_data = json.load(f)
        print(f"Flow: {flow_data['name']} (Status: {flow_data['status']})")
        print(f"Duration: {flow_data.get('duration', 'N/A')} seconds")
```

## Comparison with Other Frameworks

### Framework Comparison Table

| Criterion               | Taskinity                 | Prefect                   | Airflow                  | Luigi                     |
|-------------------------|---------------------------|---------------------------|--------------------------|---------------------------|  
| **Project Type**        | Lightweight flows         | Complex orchestration     | Complex ETL              | Simple ETL                |
| **Syntax**              | DSL + decorators          | `@flow/@task` decorators  | Classes with `DAG`       | Classes with `run()`      |
| **Dependencies**        | None                      | `prefect>=2.0`            | `apache-airflow`         | `luigi`                   |
| **Observability**       | Basic logs + UI           | Grafana/Prometheus        | Built-in UI              | Text logs                 |
| **Data Validation**     | Custom functions          | Pydantic types            | None                     | None                      |
| **Parallelism**         | Threads (future)          | Threads/Processes         | Executor                 | Sequential                |
| **Setup Time**          | < 1 minute                | 15-30 minutes             | 30-60 minutes            | 5-10 minutes              |
| **Learning curve**      | Very flat                 | Moderate                  | Steep                    | Moderate                  |

### Example Implementations

#### Taskinity: Email Classification Automation
```python
from taskinity import task, run_flow_from_dsl

@task(name="Fetch emails")
def fetch_emails(server: str) -> list:
    # Implementation
    return emails

@task(name="Classify")
def classify(emails: list) -> dict:
    # Email classification
    return {"urgent": [...], "regular": [...]}

flow = """
flow EmailFlow:
    fetch_emails -> classify
"""
```

### When to use Taskinity?

- **Small and medium projects**: When you need to quickly implement a workflow without excessive complexity
- **Prototyping**: When you want to quickly test a flow concept without infrastructure configuration
- **Readability**: When you need a readable DSL that non-technical people can understand
- **Minimalism**: When you don't need advanced features like scheduling or distributed execution
- **Immediate use**: When you want to start without installing and configuring additional components

## Dashboard

Taskinity offers two types of dashboards for flow monitoring:

### Mini Dashboard

A simple, lightweight dashboard with log history view and quick diagram preview:

```bash
python mini_dashboard.py
```

**Mini Dashboard Features:**
- Flow history with filtering (All/Completed/Errors/Running)
- Reduced SVG diagrams (90% of original size)
- Diagram editing directly in the interface with syntax highlighting
- Default open logs for each flow with syntax highlighting

### Full Dashboard

An extended dashboard with full functionality:

```bash
python simple_dashboard.py
```

## Notifications

Taskinity offers a notification system for flow status via email and Slack:

```bash
# Edit notification configuration
python -c "from notification_service import load_config, save_config; config = load_config(); config['enabled'] = True; save_config(config)"
```

## Parallel Execution

Taskinity enables parallel execution of independent tasks in a flow:

```python
# Run flow with parallel execution
from taskinity.parallel_executor import run_parallel_flow_from_dsl

result = run_parallel_flow_from_dsl(dsl_content, input_data)
```

## Flow Scheduling

Taskinity allows scheduling automatic flow execution:

```bash
# Start the scheduler
python flow_scheduler.py start

# Create a schedule (every 60 minutes)
python flow_scheduler.py create dsl_definitions/email_processing.dsl 60
```

## API Reference

### Decorators

#### `@task`

```python
@task(name=None, description=None, validate_input=None, validate_output=None)
def my_task():
    pass
```

- **name**: Optional task name (default: function name)
- **description**: Optional task description
- **validate_input**: Optional function for input data validation
- **validate_output**: Optional function for output data validation

#### `@flow`

```python
@flow(name=None, description=None)
def my_flow():
    pass
```

- **name**: Optional flow name (default: function name)
- **description**: Optional flow description

### DSL Functions

```python
# Parse DSL text into a structured flow definition
parse_dsl(dsl_text: str) -> Dict[str, Any]

# Run a flow defined in DSL
run_flow_from_dsl(dsl_text: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```

## Extensions and Plugins

Taskinity can be extended with additional functionality through plugins:

```python
# Register a custom plugin
from taskinity.extensions import register_plugin

register_plugin("my_plugin", MyPluginClass)
```

Available plugins:
- **Mermaid Converter** - Convert flows to Mermaid diagrams
- **Code Converter** - Convert existing Python code to Taskinity flows
- **Data Processors** - Tools for working with various data formats

<!-- Taskinity Render - Single script for syntax highlighting and flow diagram rendering -->
<script src="https://taskinity.github.io/render/taskinity-render.min.js"></script>
