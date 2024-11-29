"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#Image URL 
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
     db.app = app
     db.init_app(app)

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
    
    #Set up attribute
    #post = db.relationship('Post')
    
class Post(db.Model):
     __tablename__ = 'blog_posts'
     
     def __repr__(self):
           p = self
           return f"<User name={p.title} {p.content} {p.user_id}>"
     
     post_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)

     title = db.Column(db.String(50),
                           nullable=False)
     
     content = db.Column(db.String,
                          nullable=False)
     
     created_at = db.Column(db.DateTime,
                             nullable=False,
                           default=datetime.now)
     
     user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
     
     #Set up the relationship
     #Use backref set to the desired reference name, not the model
     user = db.relationship('User', backref='posts')


def get_posts():
     all_posts = Post.query.all()

     for post in all_posts:
          return post.title, post.content
     