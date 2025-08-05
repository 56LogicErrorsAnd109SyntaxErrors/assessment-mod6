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
        region = "ap-southeast-1"
        # aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        # aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        # aws_session_token = os.getenv('AWS_SESSION_TOKEN')
    title = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute()
    status = BooleanAttribute()
    description = UnicodeAttribute()


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
   
    def validate_task_not_exists(self, name : str):
        """
        Validates if the task is already added.
        """
        all_tasks = self.get_tasks()
        for task in all_tasks:
            if name == task["title"]:
                return "Task is already added to the list"


        return True


       
    def add_task(self, title, description):
        """
        This method should add a task to the DynamoDB table
        """
        if self.validate_task_name(title) == "Task name cannot be empty":
            return "Task name cannot be empty"
       
        if self.validate_task_not_exists(title) == "Task is already added to the list":
            return "Task is already added to the list"


        task = Task(title=title, status=False, date_created=str(datetime.now().date()), description=description)
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
       


    def update_task(self, title):
        """
        This method should update the task status with the given todo_id to the new_title.
        """
        task = Task.get(hash_key=title)
        task.status = True
        task.save()
        return True


    def delete_task(self, title):
        """
        This method should delete the task with the given todo_id from the DynamoDB table.
        """
        task = Task.get(hash_key=title)
        task.delete()
        return True
   
