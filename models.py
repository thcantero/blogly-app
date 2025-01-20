"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#Image URL 
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
         u = self
         return f"<User name={u.first_name} {u.last_name} {u.image_url}>"

    user_id = db.Column( db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    first_name = db.Column(db.String(50), 
                     nullable=False)
    
    last_name = db.Column(db.String(50), 
                     nullable=False)
    
    image_url = db.Column(db.String, 
                          nullable=True,
                          default= DEFAULT_IMAGE_URL)
    

    #Set up the relationship
    #Use backref set to the desired reference name, not the model
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    
    #Set up attribute
    #post = db.relationship('Post')
    
class Post(db.Model):
     __tablename__ = 'posts'
     
     def __repr__(self):
           p = self
           return f"<Post={p.title} {p.content} {p.user_id}>"
     
     post_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)

     title = db.Column(db.String(50),
                           nullable=False)
     
     content = db.Column(db.Text,
                          nullable=False)
     
     created_at = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.now)
     
     user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'),
                         nullable=False)
     
     @property
     def friendly_date(self):
          """Return nicely-formatted date"""
          
          return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
     
     
     
def get_posts():
     all_posts = Post.query.all()

     for post in all_posts:
          return post.title, post.content
 
     
class Tag(db.Model):
     __tablename__ = 'tags'
     
     id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
     
     name = db.Column(db.String(15),
                          nullable=False,
                          unique=True)
     
     posts = db.relationship(
          'Post', secondary='post_tags', cascade="all,delete", backref='tags',
     )
     
     
class PostTag(db.Model):
     __tablename__ = 'post_tags'
     
     post_id = db.Column(db.Integer,
                         db.ForeignKey('posts.post_id'),
                         nullable=False, primary_key = True)
     
     tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        nullable=False, primary_key=True)
     
     
def connect_db(app):
     """Connect database to Flask app"""
     db.app = app
     db.init_app(app)