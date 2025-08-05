from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from src.todo_list import ToDoList
TODOLIST = ToDoList()
# You will likely need a database e.g. DynamoDB so you might either boto3 or pynamodb
# Additional installs here:
#
#
#




app = Flask(__name__)


## Instantiate your database here:
#
#
#
@app.route("/")
def home():
    # Complete the code below
    # The todo_list variable should be returned by running a scan on your DDB table,
    # which is then converted to a list
    search_term = request.args.get("search_term")
    if search_term is None:
        search_term = ""
    tasks = TODOLIST.get_tasks(search_term=search_term)
    task_number = len(tasks)
    is_blank = request.args.get('is_blank')
    is_duplicate = request.args.get('is_duplicate')


    # can leave this line as is to use the template that's provided
    return render_template("index.html", tasks=tasks, task_number=task_number, is_blank=is_blank, is_duplicate=is_duplicate, search_term=search_term)




@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    is_successful = TODOLIST.add_task(title, description)
    is_duplicate = False
    is_blank = False
    if is_successful == "Task name cannot be empty":
        is_blank = True
    elif is_successful == "Task is already added to the list":
        is_duplicate = True


    return redirect(url_for("home", is_duplicate=is_duplicate, is_blank=is_blank))


   


@app.route("/update/<title>")
def update(title):
    # Complete the code below to update an existing item
    # For this particular app, updating just toggles the completion between True / False
    TODOLIST.update_task(title)
    return redirect(url_for("home"))




@app.route("/delete/<title>")
def delete(title):
    # Complete the code below to delete an item from the to-do list
    TODOLIST.delete_task(title)
    return redirect(url_for("home"))


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search")
    return redirect(url_for("home", search_term=search_term))






if __name__ == "__main__":
    app.run(debug=True, port=3000)