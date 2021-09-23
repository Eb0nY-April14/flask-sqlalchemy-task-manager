from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


# The 'tasks.html' is now our Home Page so when a user visits our site, they're brought to 
# the tasks page, which will automatically extend all of the content from our base template.
# To display existing tasks to the user (i.e on the front-end) is the 'Read' part of 'CRUD' 
# functionality. We'll 1st extract all of the tasks from our database so we'll open the 
# routes.py file & since our tasks are listed on the home page, we'll find the 'home' function 
# at the top & add a new variable called 'tasks' & assign it a list of the query method used.
        # TO DISPLAY ALL TASKS IN THE DATABASE TO THE USER (SIMILAR TO THE 'categories' FUNCTION BELOW).
@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)   


            # TO DISPLAY ALL CATEGORIES IN THE DATABASE TO THE USER.
# Whenever we call this function by clicking the navbar link for Categories, it will query
# the database and retrieve all records from this table, then sort them by the category name.
@app.route("/categories")
def categories():
    # The .all() method used here is known as a Cursor Object, which is similar to an array or 
    # list of records. Anytime we query the database, a 'Cursor Object' or 'QuerySet' is returned
    # & it can't be used on the front-end or with some of the Jinja template filters so it's good 
    # to convert your queries into Python lists by wrapping any query in a Python list() as done
    # with the 'categories' variable below & other places where we queried using '.all()'.
    categories = list(Category.query.order_by(Category.category_name).all())
    # categories=categories. The 1st declaration of 'categories' is the variable name that we
    # gave our file i.e categories.html which we can now use within the HTML template.
    # The 2nd 'categories', which is now a list(), is the variable defined within our function
    # above, which is why, once again, it's important to keep your naming convention quite similar.
    return render_template("categories.html", categories=categories)  


# When a user clicks the "Add Category" button, this will use the "GET" method and render the 
# 'add_category' template. Once they submit the form, this will call the same function, but 
# will check if the request being made is a “POST“ method, which posts data somewhere, such as a database.
# When a user clicks on the large button in 'categories.html' page to add a new category, the 
# 'add_category' function in 'routes.py' is called which will in turn render the template called 
# 'add_category.html' that will display a form to add the desired category. 
# we must include a list of the two methods "GET" and "POST" since we'll be submitting a form to the database.
# To display this form to users, it uses the "GET" method to 'get' the page & when a user then 
# submits this form, the form will attempt to 'post' the data into the database so this is why we 
# need to specify both methods in the app route.
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        # Ensure that this Category model uses the same exact keys that the model is
        # expecting as its argument so when in doubt, copy from the models.py file directly.
        # For this category_name field, we can then use the requested form being posted to 
        # retrieve the name-attribute. This is why it's important to keep the naming convention 
        # consistent, which means our name-attribute matches that of our database model.
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        # After submitting, adding & committing the new data from the form to our database, we 
        # then redirect the user back to the 'categories' page.
        return redirect(url_for("categories"))
    return render_template("add_category.html")  


                # TO EDIT A CATEGORY IN THE DATABASE BY THE USER
# Since we gave an argument of 'category_id' for when clicking the href 'Edit' button in our 
# 'categories.html' file, this also needs to appear here in our app.route. These types of 
# variables being passed back into our Python functions must be wrapped inside of angle-brackets 
# within the URL. We also need to cast the 'ID' primary key as an 'int' since we know that all 
# our primary keys must be integers.
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
# We also need to pass the 'category_id' variable directly into the function so we can have the
# value available to use within this function.
def edit_category(category_id):
    # What this code below does is use the SQLAlchemy method called '.get_or_404()', which takes 
    # the argument of 'category_id' to query the database and attempts to find the specified 
    # record using the data provided. If no match is found, it will trigger a 404 error page.
    category = Category.query.get_or_404(category_id)
    # The final step is to add the "POST" functionality so the database actually gets updated with 
    # the requested changes. We'll check using 'if' statement whether the requested method is equal 
    # to "POST". If so, then we'll update the category_name for our category variable, and we'll set 
    # that to equal the form's name-attribute of 'category_name'.
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        # if the 'POST' & commit are successful, we then redirect the users back to the 'categories'
        # function which will display all of the categories in the cards once again.
        return redirect(url_for("categories"))
    # We can now pass that variable into the rendered template, which is expecting it to be 
    # called 'category' & that will be set equal to the 'category' variable defined within 
    # the 'edit_category' function.
    return render_template("edit_category.html", category=category) 


        # TO DELETE A CATEGORY IN THE DATABASE BY THE USER
@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"])
def delete_category(category_id):  
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))  


# TO ADD A TASK TO THE DATABASE BY THE USER
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
        )
        # Ensure that this Category model uses the same exact keys that the model is
        # expecting as its argument so when in doubt, copy from the models.py file directly.
        # For this task_name field, we can then use the requested form being posted to 
        # retrieve the name-attribute. This is why it's important to keep the naming convention 
        # consistent, which means our name-attribute matches that of our database model.
        db.session.add(task)
        db.session.commit()
        # After submitting, adding & committing the new data from the form to our database, we 
        # then redirect the user back to the 'categories' page.
        return redirect(url_for("home"))
    # The 1st 'categories' listed in the 'return render_template()' below is the variable name 
    # that we will be able to use on the template itself.
    # The 2nd 'categories' is simply the list of categories retrieved from the database defined above.    
    return render_template("add_task.html", categories=categories) 


                # TO EDIT/MODIFY/UPDATE AN EXISTING TASK IN THE DATABASE BY THE USER
              
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
            task.task_name = request.form.get("task_name")
            task.task_description = request.form.get("task_description")
            task.is_urgent = bool(True if request.form.get("is_urgent") else False)
            task.due_date = request.form.get("due_date")
            task.category_id = request.form.get("category_id")
            db.session.commit()
    # The 1st 'categories' listed in the 'return render_template()' below is the variable name 
    # that we will be able to use on the template itself.
    # The 2nd 'categories' is simply the list of categories retrieved from the database defined above.    
    return render_template("edit_task.html", task=task, categories=categories) 
