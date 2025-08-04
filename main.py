from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
#from tests.unit.test_todolist import todo_list
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
    todo_list = ""
    # can leave this line as is to use the template that's provided
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    data = {'title': title,
            'description': description}
    response = requests.post(LAMBDA_API_URL, json=data)
    return jsonify({"lambda_response": response.text}), response.status_code


@app.route("/update/<todo_id>")
def update(todo_id):
    # Complete the code below to update an existing item
    # For this particular app, updating just toggles the completion between True / False


    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Complete the code below to delete an item from the to-do list


    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)