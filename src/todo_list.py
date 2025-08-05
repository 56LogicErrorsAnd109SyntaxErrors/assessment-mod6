import json
import os
from dotenv import load_dotenv
import boto3
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from datetime import datetime

class Task(Model):
    class Meta:
        table_name = "todo-table"
        region = "ap-southeast-1"  # Change if needed
    title = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute()

class ToDoList:
    def __init__(self):
        if not Task.exists():
            Task.create_table(read_capacity_units=1, write_capacity_units=1, wait = True)
        
    def validate_task_name(self, name : str):
        """
        Validate the task name. Task names cannot be empty or whitespace only.
        """
        if name == "" or name.isspace():
            return "Task name cannot be empty"
        
        return True

        
    def add_task(self, title):
        """
        This method should add a task to the DynamoDB table
        """
        if self.validate_task_name(title) == "Task name cannot be empty":
            return "Task name cannot be empty"
        
        task = Task(title=title, date_created=str(datetime.now().date()))
        task.save()
        return True


    def get_tasks(self, search_term=""):
        """
        This method should return a list of tasks from the DynamoDB table.
        If search_term is provided, it should filter tasks based on the title.
        If sort_mode is provided, sort and return the tasks based on the given mode,
        """
        all_tasks = [task.attribute_values for task in Task.scan()]
        if search_term == "":
            return all_tasks
        
        tasks = [task for task in all_tasks if search_term in task["title"]]
        return tasks
        

    def update_task(self, old_title, new_title):
        """
        This method should update the task with the given todo_id to the new_title.
        """
        task = Task.get(hash_key=old_title)
        task.title = new_title
        task.save()
        return True

    def delete_task(self, title):
        """
        This method should delete the task with the given todo_id from the DynamoDB table.
        """
        task = Task.get(hash_key=title)
        task.delete()
        return True
    