"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

#Image URL 

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
                          default=DEFAULT_IMAGE_URL)
    
class Post(db.Model):
     __tablename__ = 'blog_posts'
     
     def __repr__(self):
           p = self
     
     post_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)

     title = db.Column(db.String(50),
                           nullable=False)
     
     content = db.Column(db.String,
                          nullable=False)
     
     #created_at = db.Column(db.DateTime,
      #                      nullable=False,
      #                      default=datetime.datetime.now)
     
     user_id = db.Column(db.Integer)