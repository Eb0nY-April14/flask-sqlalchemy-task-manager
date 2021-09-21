from taskmanager import db


# the 'db' imported above already has Integer, Float, Strings, 
# Tables etc in it so we don't need to specifically import each 
# column type at the top of the file. The 'db' variable contains 
# each of those already, and we can simply use dot-notation to 
# specify the data-type for our columns as seen below.
class Category(db.Model):
    # schema for the "Category" model.
    id = db.Column(db.Integer, primary_key=True)
    # we'll set 'category_name' to have a max character length of 25, 
    # set unique=True to ensure each new Category being added to the 
    # database is unique & also set nullable=False to ensure it's not 
    # empty or blank to enforce that it's a required field.
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    # to properly link our foreign key & cascade deletion, we'll add a 
    # field to the Category table called 'tasks' variable, don't confuse 
    # it with the main'Task' class & we'll use db.relationship instead of 
    # db.Column. This won't be visible on the database itself as it's just 
    # to reference the one-to-many relationship.
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)

# For each model, we also need to create a function called __repr__ 
# that takes itself as the argument. This is a standard Python 
# function meaning 'represent’ which means to represent the class 
# objects as a string. We can also use the __str__ function that 
# behaves quite similar to the __repr__ function & either should be 
# suitable to use.
# 'self' used here is similar to 'this' keyword in JavaScript
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.category_name   


class Task(db.Model):
    # schema for the "Task" model.
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    # The value of the 'category_id' foreign key will point to the ID 
    # from our Category class so we need to use lowercase 'category.id' 
    # in quotes. Also, we'll apply something called ondelete="CASCADE" 
    # to this foreign key. What this CASCADE does is that once a category 
    # is deleted, it will perform a cascading effect and also delete any 
    # task linked to it or else a task will contain an invalid foreign key
    # & then you will get errors.
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Task: {1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent
            )   
