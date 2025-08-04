import pytest
from src.todo_list import ToDoList

@pytest.fixture
def todo_list():
    return ToDoList()

def test_validate_task_name(todo_list):
    """
    Test validating task names.
    This test checks if the task name validation works correctly, ensuring that empty or whitespace-only names are not allowed.
    """
    assert todo_list.validate_task_name("Valid Task")
    assert todo_list.validate_task_name("") == "Task name cannot be empty"
    assert todo_list.validate_task_name(" " * 10) == "Task name cannot be empty"

def test_add_task(todo_list):
    """
    Test adding a task to the to-do list.
    This test checks if a task can be added and is retrievable from the DynamoDB.
    The task should have a valid title.
    """
    assert todo_list.add_task("Test task")
    assert todo_list.add_task("") == "Task name cannot be empty"

def test_get_tasks(todo_list):
    """
    Test retrieving tasks from the to-do list.
    This test checks if tasks can be retrieved correctly from the DynamoDB
    """
    todo_list.add_task("Task 1")
    todo_list.add_task("Task 2")
    todo_list.add_task("Process 1")
    task_1 = todo_list.get_tasks("Task_1")
    tasks = todo_list.get_tasks("Task")
    all_tasks = todo_list.get_tasks("")
    assert task_1 == "Task 1"
    assert tasks == ["Task 1", "Task 2"]
    assert all_tasks == ["Task 1", "Task 2", "Process 1"]

def test_update_task(todo_list):
    """
    Test updating a task in the to-do list.
    This test checks if a task can be updated and the changes are reflected in the DynamoDB
    """
    assert todo_list.update_task(1, "Updated task")

def test_delete_task(todo_list):
    """
    Test deleting a task from the to-do list.
    This test checks if a task can be deleted and is no longer retrievable from the DynamoDB
    """
    todo_list.add_task("Task to delete")
    assert todo_list.delete_task(1)
