Feature: To-Do List

Scenario: Add a new task
Given I have a to-do list
When I add a new task "Buy groceries"
Then the task "Buy groceries" should be in my to-do list

Scenario: Update a task
Given I have a to-do list with a task "Buy groceries"
When I update the task "Buy groceries" to "Buy groceries and cook dinner"
Then the task "Buy groceries and cook dinner" should be in my to-do list and task "Buy groceries" should not be in my to-do list

Scenario: Remove a task
Given I have a to-do list with a task "Buy groceries"
When I remove the task "Buy groceries"
Then the task "Buy groceries" should not be in my to-do list

Scenario: Search for a task
Given I have a to-do list with tasks "Buy groceries", "Clean the house", and "Walk the dog"
When I search for the task "Clean"
Then the task "Clean the house" should be in my to-do list

Scenario: View all tasks
  Given I have a to-do list with tasks "Buy groceries" and "Walk the dog"
  When the search bar is empty
  Then I should see "Buy groceries" and "Walk the dog" in my to-do list

Scenario: Add task with missing title
  Given I have a to-do list
  When I try to add a task with no title
  Then I should see an error message indicating the title is required

