from flask import render_template
from taskmanager import app, db
from taskmanager.models import Category, Task


# The 'tasks.html' is now our Home Page so when a user visits our site, they're brought to 
# the tasks page, which will automatically extend all of the content from our base template.
@app.route("/")
def home():
    return render_template("tasks.html")   
