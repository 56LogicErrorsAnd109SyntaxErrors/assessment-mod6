from behave import given, when, then
from   # Replace with your actual app module/class

# Initialize the app state before each scenario
def before_scenario(context, scenario):
    context.app = ToDoApp()
    context.last_created_item = None

@given("I have no to-do list")
def step_impl(context):
    context.app.clear_items()

@when('I create a to do list with a "Buy groceries" item')
def step_impl(context):
    context.last_created_item = context.app.create_item("Buy groceries")

@then("the new item should be saved to the database")
def step_impl(context):
    items = context.app.get_items()
    assert context.last_created_item in items

@given("there are items in the database")
def step_impl(context):
    context.app.create_item("Buy groceries")
    context.app.create_item("Do laundry")

@when("I view the to-do list")
def step_impl(context):
    context.items = context.app.get_items()

@then("I should see a list of all items")
def step_impl(context):
    assert len(context.items) > 0

@given("a to-do item exists")
def step_impl(context):
    context.item = context.app.create_item("Pay bills")

@when("I view the item")
def step_impl(context):
    context.viewed_item = context.app.get_item(context.item.id)

@then("I should see the attributes of the item")
def step_impl(context):
    assert context.viewed_item.name == "Pay bills"

@given("multiple items exist in the database")
def step_impl(context):
    context.app.create_item("Pay bills")
    context.app.create_item("Buy milk")
    context.app.create_item("Walk dog")

@when("I search for a keyword")
def step_impl(context):
    context.search_results = context.app.search_items("milk")

@then("only matching items should be displayed in the list")
def step_impl(context):
    assert all("milk" in item.name.lower() for item in context.search_results)

@when("I add an item")
def step_impl(context):
    context.added_item = context.app.create_item("Read book")

@then("the item should be in the to-do list")
def step_impl(context):
    assert context.added_item in context.app.get_items()

@when("I Delete an item")
def step_impl(context):
    context.app.delete_item(context.item.id)

@then("the item should be removed from the database")
def step_impl(context):
    items = context.app.get_items()
    assert context.item not in items
