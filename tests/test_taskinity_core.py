"""
Tests for the core functionality of Taskinity.
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
    
    def test_task_decorator_with_validation(self):
        """Test task decorator with input and output validation."""
        # Create a mock function that will be used for testing
        def mock_task_function(x, y):
            return x + y
        
        # Define validation functions
        def validate_input(x, y):
            if not isinstance(x, int) or not isinstance(y, int):
                raise ValueError("Inputs must be integers")
            return True
        
        def validate_output(result):
            if not isinstance(result, int):
                raise ValueError("Output must be an integer")
            return True
        
        # Create the task with validation
        test_task = task(validate_input=validate_input, validate_output=validate_output)(mock_task_function)
        
        # Check if validation functions are set correctly
        assert test_task.__taskinity_task__["validate_input"] == validate_input
        assert test_task.__taskinity_task__["validate_output"] == validate_output
        
        # Test with valid inputs and output
        assert test_task(2, 3) == 5
        
        # Test with invalid inputs
        with pytest.raises(ValueError) as excinfo:
            test_task("2", 3)
        assert "Inputs must be integers" in str(excinfo.value)
    
    def test_task_decorator_with_output_validation(self):
        """Test task decorator with output validation."""
        # This test is separate because we need to mock the function's return value
        def validate_output(result):
            if not isinstance(result, int):
                raise ValueError("Output must be an integer")
            return True
        
        # Create a mock function that returns a string
        def mock_task_returns_string(x, y):
            return str(x + y)
        
        # Create the task with output validation
        test_task = task(validate_output=validate_output)(mock_task_returns_string)
        
        # Test with invalid output (function returns a string instead of int)
        with pytest.raises(ValueError) as excinfo:
            test_task(2, 3)
        assert "Output must be an integer" in str(excinfo.value)


class TestFlowDecorator:
    """Tests for the Taskinity core module decorator."""
    
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
        
        # parse_dsl should handle invalid DSL gracefully and return a default flow
        result = parse_dsl(invalid_dsl)
        assert isinstance(result, dict)
        assert "name" in result
        assert "tasks" in result
        assert "connections" in result
        assert result["name"] == "UnnamedFlow"  # Default name for invalid DSL
    
    def test_parse_dsl_empty(self):
        """Test parsing empty DSL."""
        empty_dsl = ""
        
        # parse_dsl should handle empty DSL gracefully and return a default flow
        result = parse_dsl(empty_dsl)
        assert isinstance(result, dict)
        assert "name" in result
        assert "tasks" in result
        assert "connections" in result
        assert result["name"] == "UnnamedFlow"  # Default name for empty DSL


class TestRunFlowFromDSL:
    """Tests for the run_flow_from_dsl function."""
    
    def test_run_flow_from_dsl_basic(self, sample_dsl):
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
        
        # Parse the sample DSL to get the expected flow data
        flow_data = parse_dsl(sample_dsl)
        
        # Mock the parse_dsl function to return the parsed flow data
        with patch("taskinity.parse_dsl", return_value=flow_data):
            # Mock the REGISTRY
            with patch("taskinity.core.taskinity_core.REGISTRY", task_registry):
                # Run the flow
                results = run_flow_from_dsl(sample_dsl)
                
                # Check if the results are correct
                assert results["task1"] == "task1_result"
                assert results["task2"] == "task2_result(task1_result)"
                assert results["task3"] == "task3_result(task1_result)"
                assert results["task4"] == "task4_result(task2_result(task1_result), task3_result(task1_result))"
    
    def test_run_flow_from_dsl_with_input(self, sample_dsl):
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
        
        # Parse the sample DSL to get the expected flow data
        flow_data = parse_dsl(sample_dsl)
        
        # Mock the parse_dsl function to return the parsed flow data
        with patch("taskinity.parse_dsl", return_value=flow_data):
            # Mock the REGISTRY
            with patch("taskinity.core.taskinity_core.REGISTRY", task_registry):
                # Run the flow with input data
                results = run_flow_from_dsl(sample_dsl, {"input_param": "test_input"})
                
                # Check if the results are correct
                assert results["task1"] == "task1_result(test_input)"
                assert results["task2"] == "task2_result(task1_result(test_input))"
                assert results["task3"] == "task3_result(task1_result(test_input))"
                assert results["task4"] == "task4_result(task2_result(task1_result(test_input)), task3_result(task1_result(test_input)))"
    
    def test_run_flow_from_dsl_error(self, sample_dsl):
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
        
        # Mock the task registry
        task_registry = {
            "task1": task1_func,
            "task2": task2_func,
            "task3": task3_func,
            "task4": task4_func
        }
        
        # Mock the parse_dsl function to return a predefined flow data
        with patch("taskinity.parse_dsl", return_value=pytest.fixture(lambda: sample_flow_data)()):
            # Mock the task registry
            with patch("taskinity.get_task_registry", return_value=task_registry):
                # Run the flow and expect an error
                with pytest.raises(ValueError, match="Task 1 error"):
                    run_flow_from_dsl(sample_dsl)
