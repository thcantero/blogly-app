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
    return redirect("/users")

# **GET */users :*** Show all users. 
# Make these links to view the detail page for the user. 
# Have a link here to the add-user form.
@app.route("/users")
def list_users():
    """Show list of all users"""
    users = User.query.all()
    return render_template("user_listing.html", users=users)

# **GET */users/new :*** Show an add form for users
# **POST */users/new :*** Process the add form, 
# adding a new user and going back to ***/users***
@app.route("/users/new", methods=["GET","POST"])
def create_user():
    if request.method == "GET":
        #Show form
        return render_template("create_user.html")
    
    else:
        #Handle form submission and redirect to /user
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        image_url = request.form.get("img_url")

        #I had to add this because I was getting an error: 
        #IntegrityError sqlalchemy.exc.IntegrityError: (psycopg2.errors.NotNullViolation) 
        # null value in column "first_name" of relation "users" violates not-null constraint
        #What do I do to fix it?
        if not first_name or not last_name:
            flash("First and Last Name are required!", "error")
            return redirect("/users/new")

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect(f"/users/{new_user.user_id}")

# **GET */users/[user-id] :***Show information about the given user. 
# Have a button to get to their edit page, and to delete the user.
@app.route("/users/<int:user_id>")
def display_user(user_id):
    user = User.query.get_or_404(user_id)
    #user = User.query.get(user_id)
    return render_template("display_user.html", user=user)

# **GET */users/[user-id]/edit :*** Show the edit page for a user. 
# Have a cancel button that returns to the detail page for a user, 
# and a save button that updates the user.
# **POST */users/[user-id]/edit :***Process the edit form, 
# returning the user to the ***/users*** page.
@app.route("/users/<int:user_id>/edit", methods=["GET","POST"])
def edit_user(user_id):
    #Show edit form
    if request.method == "GET":
        user = User.query.get_or_404(user_id)
        return render_template("edit_user.html", user=user)
    
    else:
        #Handle form submission: edit
        user = User.query.get_or_404(user_id)
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.image_url = request.form.get("img_url")

        db.session.add(user)
        db.session.commit()

        return redirect(f"/users")

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.query.filter_by(user_id = user_id).delete()
    db.session.commit()

    return redirect("/users")

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
 