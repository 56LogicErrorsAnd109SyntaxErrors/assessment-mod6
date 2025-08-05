import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from src.todo_list import ToDoList


# Link the scenarios to the feature file
scenarios("../features/todo_list.feature")
#Code below:

@pytest.fixture
def todo_list():
    return ToDoList()

#Tests for adding a task
@given("I have a to-do list")
def step_given_todo_list_page(todo_list):
    return todo_list

@when(parsers.parse("I add a new task '{title}'"))
def step_when_add_task(todo_list, title):
    result =  todo_list.add_task(title)

@then(parsers.parse("the task '{title}' should be in my to-do list"))
def step_then_task_added(todo_list, title):
    all_tasks = todo_list.get_tasks()
    all_tasks_titles = []
    for task in all_tasks:
        all_tasks_titles.append(task["title"])
    
    assert title in all_tasks_titles

@when("I try to add a task with no title", target_fixture = "result")
def step_when_add_task_no_title(todo_list):
    result = todo_list.add_task("")
    return result

@then("I should see an error message indicating the title is required")
def step_then_error_message(todo_list, result):
    assert result == "Task name cannot be empty"
    
# Tests for updating and removing a task
@given(parsers.parse("I have a to-do list with a task '{title}'"))
def step_given_todo_list_with_task(todo_list, title):
    todo_list.add_task(title)
    return todo_list

@when(parsers.parse("I update the task '{title}' to '{new_title}'"))
def step_when_update_task(todo_list, title, new_title):
    todo_list.update_task(title, new_title)

@then(parsers.parse("the task '{new_title}' should be in my to-do list and task '{title}' should not be in my to-do list"))
def step_then_task_updated(todo_list, new_title, title):
    all_tasks = todo_list.get_tasks()
    all_tasks_titles = []
    for task in all_tasks:
        all_tasks_titles.append(task["title"])

    assert new_title in all_tasks_titles
    assert title not in all_tasks_titles

@when(parsers.parse("I remove the task '{title}'"))
def step_when_delete_task(todo_list, title):
    todo_list.delete_task(title)

@then(parsers.parse("the task '{title}' should not be in my to-do list"))
def step_then_task_deleted(todo_list, title):
    all_tasks = todo_list.get_tasks()
    all_tasks_titles = []
    for task in all_tasks:
        all_tasks_titles.append(task["title"])
    
    assert title not in all_tasks_titles

# Tests for searching tasks
@given(parsers.parse("I have a to-do list with tasks '{titles}'"))
def step_given_todo_list_with_multiple_tasks(todo_list, titles):
    for title in titles.split(", "):
        todo_list.add_task(title)

    return todo_list

@when(parsers.parse("I search for the task '{search_term}'"), target_fixture="result")
def step_when_search_task(todo_list, search_term):
    result = todo_list.get_tasks(search_term)
    return result

@then(parsers.parse("I should see '{titles}' in my to-do list"))
def step_then_task_in_list(todo_list, titles, result):
    all_tasks_titles = []
    for task in result:
        all_tasks_titles.append(task["title"])
    
    for title in titles.split(", "):
        assert title in all_tasks_titles

@when("the search bar is empty", target_fixture="result")
def step_when_search_bar_empty(todo_list):
    result = todo_list.get_tasks()
    return result
