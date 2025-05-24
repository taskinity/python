"""
Tests for the core flow DSL functionality of Taskinity.
"""
import pytest
from unittest.mock import patch, MagicMock
from taskinity.core.taskinity_core import task, flow, run_flow_from_dsl, parse_dsl


class TestTaskDecorator:
    """Tests for the task decorator."""
    
    def test_task_decorator_basic(self):
        """Test basic task decorator functionality."""
        @task
        def test_task(x, y):
            return x + y
        
        # Check if task function is wrapped correctly
        assert hasattr(test_task, "__taskinity_task__")
        assert test_task.__name__ == "test_task"
        assert test_task(2, 3) == 5
    
    def test_task_decorator_with_name(self):
        """Test task decorator with custom name."""
        @task(name="CustomTask")
        def test_task(x, y):
            return x + y
        
        # Check if task name is set correctly
        assert test_task.__taskinity_task__["name"] == "CustomTask"
    
    def test_task_decorator_with_description(self):
        """Test task decorator with description."""
        @task(description="Test task description")
        def test_task(x, y):
            return x + y
        
        # Check if task description is set correctly
        assert test_task.__taskinity_task__["description"] == "Test task description"
    
    def test_task_decorator_with_input_validation(self):
        """Test task decorator with input validation."""
        def validate_input(*args):
            if len(args) != 2:
                raise ValueError("Expected exactly 2 arguments")
            x, y = args
            if not isinstance(x, int) or not isinstance(y, int):
                raise ValueError("Inputs must be integers")
            return True
        
        @task(validate_input=validate_input)
        def test_task(x, y):
            return x + y
        
        # Check if validation function is set correctly
        assert test_task.__taskinity_task__["validate_input"] == validate_input
        
        # Test with valid inputs
        assert test_task(2, 3) == 5
        
        # Test with invalid inputs
        with pytest.raises(ValueError, match="Inputs must be integers"):
            test_task("2", 3)
    
    def test_task_decorator_with_output_validation(self):
        """Test task decorator with output validation."""
        def validate_output(result):
            if not isinstance(result, int):
                raise ValueError("Output must be an integer")
            return True
        
        # Create a function that returns a string instead of an int
        def failing_function():
            return "not an integer"
        
        # Apply the task decorator with output validation
        test_task = task(validate_output=validate_output)(failing_function)
        
        # Check if validation function is set correctly
        assert test_task.__taskinity_task__["validate_output"] == validate_output
        
        # Test that output validation fails with the expected error
        with pytest.raises(ValueError, match="Output must be an integer"):
            test_task()


class TestFlowDecorator:
    """Tests for the flow decorator."""
    
    def test_flow_decorator_basic(self):
        """Test basic flow decorator functionality."""
        @flow
        def test_flow():
            return "test_flow_result"
        
        # Check if flow function is wrapped correctly
        assert hasattr(test_flow, "__taskinity_flow__")
        assert test_flow.__name__ == "test_flow"
        assert test_flow() == "test_flow_result"
    
    def test_flow_decorator_with_name(self):
        """Test flow decorator with custom name."""
        @flow(name="CustomFlow")
        def test_flow():
            return "test_flow_result"
        
        # Check if flow name is set correctly
        assert test_flow.__taskinity_flow__["name"] == "CustomFlow"
    
    def test_flow_decorator_with_description(self):
        """Test flow decorator with description."""
        @flow(description="Test flow description")
        def test_flow():
            return "test_flow_result"
        
        # Check if flow description is set correctly
        assert test_flow.__taskinity_flow__["description"] == "Test flow description"


class TestParseDSL:
    """Tests for the parse_dsl function."""
    
    def test_parse_dsl_basic(self, sample_dsl):
        """Test basic DSL parsing."""
        flow_data = parse_dsl(sample_dsl)
        
        # Check if flow data is parsed correctly
        assert flow_data["name"] == "TestFlow"
        assert flow_data["description"] == "Test flow for unit tests"
        assert "tasks" in flow_data
        
        # Check if tasks are parsed correctly
        tasks = flow_data["tasks"]
        assert "task1" in tasks
        assert "task2" in tasks
        assert "task3" in tasks
        assert "task4" in tasks
        
        # Check if task connections are parsed correctly
        assert tasks["task1"]["outputs"] == ["task2", "task3"]
        assert tasks["task2"]["inputs"] == ["task1"]
        assert tasks["task2"]["outputs"] == ["task4"]
        assert tasks["task3"]["inputs"] == ["task1"]
        assert tasks["task3"]["outputs"] == ["task4"]
        assert tasks["task4"]["inputs"] == ["task2", "task3"]
        assert tasks["task4"]["outputs"] == []
    
    def test_parse_dsl_invalid(self):
        """Test parsing invalid DSL."""
        invalid_dsl = """
        invalid dsl syntax
        """
        
        # The function should return a default flow structure with the invalid content ignored
        result = parse_dsl(invalid_dsl)
        assert isinstance(result, dict)
        assert "name" in result
        assert "tasks" in result
        assert "connections" in result
        assert result["name"] == "UnnamedFlow"  # Default name for invalid DSL
    
    def test_parse_dsl_empty(self):
        """Test parsing empty DSL."""
        empty_dsl = ""
        
        # The function should return a default flow structure with empty tasks and connections
        result = parse_dsl(empty_dsl)
        assert isinstance(result, dict)
        assert "name" in result
        assert "tasks" in result
        assert "connections" in result
        assert result["name"] == "UnnamedFlow"  # Default name for empty DSL
        assert result["tasks"] == {}
        assert result["connections"] == []


class TestRunFlowFromDSL:
    """Tests for the run_flow_from_dsl function."""
    
    def test_run_flow_from_dsl_basic(self, sample_dsl, sample_flow_data):
        """Test basic flow execution from DSL."""
        # Define task functions
        @task(name="task1")
        def task1_func():
            return "task1_result"
        
        @task(name="task2")
        def task2_func(task1_result):
            return f"task2_result({task1_result})"
        
        @task(name="task3")
        def task3_func(task1_result):
            return f"task3_result({task1_result})"
        
        @task(name="task4")
        def task4_func(task2_result, task3_result):
            return f"task4_result({task2_result}, {task3_result})"
        
        # Create task registry with the expected structure
        task_registry = {
            "task1": {"function": task1_func, "name": "task1"},
            "task2": {"function": task2_func, "name": "task2"},
            "task3": {"function": task3_func, "name": "task3"},
            "task4": {"function": task4_func, "name": "task4"}
        }
        
        # Mock the parse_dsl function to return the sample_flow_data
        with patch("taskinity.parse_dsl", return_value=sample_flow_data):
            # Mock the REGISTRY
            with patch("taskinity.core.taskinity_core.REGISTRY", task_registry):
                # Run the flow
                results = run_flow_from_dsl(sample_dsl)
                
                # Check if the result is correct
                assert results["task4"] == "task4_result(task2_result(task1_result), task3_result(task1_result))"
    
    def test_run_flow_from_dsl_with_input(self, sample_dsl, sample_flow_data):
        """Test flow execution from DSL with input data."""
        # Define task functions
        @task(name="task1")
        def task1_func(input_param):
            return f"task1_result({input_param})"
        
        @task(name="task2")
        def task2_func(task1_result):
            return f"task2_result({task1_result})"
        
        @task(name="task3")
        def task3_func(task1_result):
            return f"task3_result({task1_result})"
        
        @task(name="task4")
        def task4_func(task2_result, task3_result):
            return f"task4_result({task2_result}, {task3_result})"
        
        # Create task registry with the expected structure
        task_registry = {
            "task1": {"function": task1_func, "name": "task1"},
            "task2": {"function": task2_func, "name": "task2"},
            "task3": {"function": task3_func, "name": "task3"},
            "task4": {"function": task4_func, "name": "task4"}
        }
        
        # Create a copy of the sample flow data and update the first task's inputs
        flow_data = sample_flow_data.copy()
        flow_data['tasks']['task1']['inputs'] = ['input_param']
        
        # Mock the parse_dsl function to return the modified flow_data
        with patch("taskinity.parse_dsl", return_value=flow_data):
            # Mock the REGISTRY
            with patch("taskinity.core.taskinity_core.REGISTRY", task_registry):
                # Run the flow with input data
                results = run_flow_from_dsl(sample_dsl, {"input_param": "test_input"})
                
                # Check if the result is correct
                assert results["task4"] == "task4_result(task2_result(task1_result(test_input)), task3_result(task1_result(test_input)))"
    
    def test_run_flow_from_dsl_error(self, sample_dsl, sample_flow_data):
        """Test flow execution from DSL with error."""
        # Define task functions
        @task(name="task1")
        def task1_func():
            raise ValueError("Task 1 error")
        
        @task(name="task2")
        def task2_func(task1_result):
            return f"task2_result({task1_result})"
        
        @task(name="task3")
        def task3_func(task1_result):
            return f"task3_result({task1_result})"
        
        @task(name="task4")
        def task4_func(task2_result, task3_result):
            return f"task4_result({task2_result}, {task3_result})"
        
        # Create task registry with the expected structure
        task_registry = {
            "task1": {"function": task1_func, "name": "task1"},
            "task2": {"function": task2_func, "name": "task2"},
            "task3": {"function": task3_func, "name": "task3"},
            "task4": {"function": task4_func, "name": "task4"}
        }
        
        # Mock the parse_dsl function to return the sample_flow_data
        with patch("taskinity.parse_dsl", return_value=sample_flow_data):
            # Mock the REGISTRY
            with patch("taskinity.core.taskinity_core.REGISTRY", task_registry):
                # Run the flow and expect an error
                with pytest.raises(ValueError, match="Task 1 error"):
                    run_flow_from_dsl(sample_dsl)
