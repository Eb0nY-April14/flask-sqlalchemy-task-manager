import os
import re  # It's the Regular Expression package for Python.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env  


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# Usually, the app is configured to look for the local database during development 
# but for deployment to Heroku, it has to point to Heroku's database or else Heroku 
# won't see the db. To do this, we'll add a conditional check for Heroku's Postgres 
# database i.e if the "DEVELOPMENT" environment variable is set to True, then we are 
# working with our local database otherwise, since we didn't set that variable on 
# Heroku, then it should use Heroku's "DATABASE_URL" instead.
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")  # local database
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri  # Heroku database

db = SQLAlchemy(app)

from taskmanager import routes  
