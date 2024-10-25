"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db' #Name of the db we are using 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# **GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
@app.route("/")
def home():
    #need to redirect
    return render_template("user_listing.html")

# **GET */users :*** Show all users. 
# Make these links to view the detail page for the user. 
# Have a link here to the add-user form.

# **GET */users/new :*** Show an add form for users
@app.route("/users/new")
def create_user():
    return render_template("create_user.html")

# **POST */users/new :*** Process the add form, 
# adding a new user and going back to ***/users***

# **GET */users/[user-id] :***Show information about the given user. 
# Have a button to get to their edit page, and to delete the user.
@app.route("/users/[user-id]")
def display_user():
    return render_template("display_user.html")

# **GET */users/[user-id]/edit :*** Show the edit page for a user. 
# Have a cancel button that returns to the detail page for a user, 
# and a save button that updates the user.
@app.route("/users/[user-id]/edit")
def edit_user():
    return render_template("edit_user.html")

# **POST */users/[user-id]/edit :***Process the edit form, 
# returning the user to the ***/users*** page.

# **POST */users/[user-id]/delete :*** Delete the user.

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
