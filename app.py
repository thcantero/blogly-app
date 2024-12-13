"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
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

with app.app_context():
    db.create_all()

# **Make a Homepage**
#Change the homepage to a page that shows the 5 most recent posts.
@app.route("/")
def home():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)

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
    #posts = Post.query.all()
    #user = User.query.get(user_id)
    return render_template("display_user.html", user=user) #posts=posts)

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
        user.image_url = request.form.get("image_url")

        db.session.add(user)
        db.session.commit()

        return redirect(f"/users")

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(user_id = user_id).delete()
    db.session.commit()
    flash("User deleted successfully!", "success")

    return redirect("/users")


##POSTS ROUTES

#  **GET */users/[user-id]/posts/new :
# *** Show form to add a post for that user.
# **POST */users/[user-id]/posts/new :
# *** Handle add form; add post and redirect to the user detail page.
@app.route("/users/<int:user_id>/posts/new", methods=["GET","POST"])
def new_post(user_id):
    """Show a form to create a new post for a specific user"""
    """Handle form submission for creating a new post for a specific user"""
    if request.method == "GET":
        user = User.query.get_or_404(user_id)
        return render_template("post_form.html", user=user)
    
    else:
        new_post = Post(
            title = request.form["title"],
            content = request.form["content"],
            user_id=user_id)

        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(f"/users/{user_id}")
    

# **GET */posts/[post-id] :
# *** Show a post. Show buttons to edit and delete the post.
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a page with info on a specific post"""
    post = Post.query.get_or_404(post_id)
    return render_template("show_post.html", post = post)

# **GET */posts/[post-id]/edit :
# *** Show form to edit a post, and to cancel (back to user page).
# **POST */posts/[post-id]/edit :
# *** Handle editing of a post. Redirect back to the post view.
@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    """Show a form to edit an existing post"""
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    
    if request.method == "GET":
        return render_template("edit_post.html", post=post)
    
    else:
        post.title = request.form.get('title')
        post.content = request.form.get('content')
    
    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited", "success")
    return redirect(f"/users/{post.user_id}")
 
 # **POST */posts/[post-id]/delete :
# *** Delete the post.
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted", "success")

    return redirect(f"/users/{post.user_id}")