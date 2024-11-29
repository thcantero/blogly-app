"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
@app.route("/users", methods=["GET"])
def list_users():
    """Show list of all users"""
    users = User.query.all()
    return render_template("user_listing.html", users=users)

# **GET */users/new :*** Show an add form for users
# **POST */users/new :*** Process the add form, 
# adding a new user and going back to ***/users***

@app.route("/users/new", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    else:
        new_user = User(
            first_name = request.form["first_name"],
            last_name = request.form["last_name"],
            image_url = request.form["image_url"] or None)

        db.session.add(new_user)
        db.session.commit()

        flash("User created successfully!", "success")
        return redirect(f"/users/{new_user.user_id}")
    
# @app.route("/users/new", methods=["GET","POST"])
# def create_user():
#     if request.method == "GET":
#         #Show form
#         return render_template("create_user.html")
    
#     else:
#         #Handle form submission and redirect to /user
#         first_name = request.form.get("first_name")
#         last_name = request.form.get("last_name")
#         image_url = request.form.get("image_url")

#         new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect(f"/users/{new_user.user_id}")

        #I had to add this because I was getting an error: 
        #IntegrityError sqlalchemy.exc.IntegrityError: (psycopg2.errors.NotNullViolation) 
        # null value in column "first_name" of relation "users" violates not-null constraint
        #What do I do to fix it?
        # if not first_name or not last_name:
        #     flash("First and Last Name are required!", "error")
        #     return redirect("/users/new")

# **GET */users/[user-id] :***Show information about the given user. 
# Have a button to get to their edit page, and to delete the user.
@app.route("/users/<int:user_id>")
def display_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.all()
    #user = User.query.get(user_id)
    return render_template("display_user.html", user=user, posts=posts)

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
        return render_template("edit_user.html", user_id=user_id)
    
    else:
        #Handle form submission: edit
        user = User.query.get_or_404(user_id)
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.image_url = request.form.get("image_url")

        db.session.add(user)
        db.session.commit()

        return redirect(f"/users")

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.query.filter_by(user_id = user_id).delete()
    db.session.commit()

    return redirect("/users")


##POSTS ROUTES

#  **GET */users/[user-id]/posts/new :
# *** Show form to add a post for that user.
# **POST */users/[user-id]/posts/new :
# *** Handle add form; add post and redirect to the user detail page.
@app.route("/users/<int:user_id>/posts/new", methods=["GET","POST"])
def new_post(user_id):
    if request.method == "GET":
        return render_template("post_form.html", user_id=user_id)
    
    else:
        new_post = Post(
            title = request.form["title"],
            content = request.form["content"])

        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully!", "success")
        #If i have the action in the form, then I don't need to redirect here?
        return redirect(f"/users/{user_id}")
    

# **GET */posts/[post-id] :
# *** Show a post. Show buttons to edit and delete the post.
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    #post_id = Post.query.get_or_404(post_id)
    return render_template("show_post.html", post_id = post_id)

# **GET */posts/[post-id]/edit :
# *** Show form to edit a post, and to cancel (back to user page).
# **POST */posts/[post-id]/edit :
# *** Handle editing of a post. Redirect back to the post view.
# **POST */posts/[post-id]/delete :
# *** Delete the post.
@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    return render_template("edit_post.html", post_id=post_id)

 