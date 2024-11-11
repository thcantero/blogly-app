from models import User, db
from app import app

#Why do I need to add with app.app_context()? 
#It wasn't running without it.

with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()

    john = User(first_name='John', last_name='Doe')
    jane = User(first_name='Jane', last_name='Doe')
    will = User(first_name='Will', last_name='Smith')
    megan = User(first_name='Megan', last_name='Fox')
    brad  = User(first_name='Brad', last_name='Pitt')

    db.session.add_all([john, jane, will, megan, brad])
    db.session.commit()
