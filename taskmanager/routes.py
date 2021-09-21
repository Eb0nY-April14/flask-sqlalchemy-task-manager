from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


# The 'tasks.html' is now our Home Page so when a user visits our site, they're brought to 
# the tasks page, which will automatically extend all of the content from our base template.
@app.route("/")
def home():
    return render_template("tasks.html")   


@app.route("/categories")
def categories():
    return render_template("categories.html")  


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
