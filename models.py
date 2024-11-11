"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
                          nullable=True)
    
    def edit_user(self):
         """Edit user information"""
         