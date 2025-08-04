import json
import os
from dotenv import load_dotenv

class ToDoList:
    def __init__(self):
        LAMBDA_API_URL = os.getenv("LAMBDA_API_URL")

    def validate_task_name(self, name):
        """
        Validate the task name. Task names cannot be empty or whitespace only.
        """
        
    def add_task(self, title):
        pass

    def get_tasks(self, search_term=""):
        """
        This method should return a list of tasks from the DynamoDB table.
        If search_term is provided, it should filter tasks based on the title.
        """
        pass

    def update_task(self, todo_id, new_title):
        """
        This method should update the task with the given todo_id to the new_title.
        """
        pass

    def delete_task(self, todo_id):
        """
        This method should delete the task with the given todo_id from the DynamoDB table.
        """
        pass