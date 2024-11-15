# raise RuntimeError(unbound_message) from None
# RuntimeError: Working outside of application context.

# This typically means that you attempted to use functionality that needed
# the current application. To solve this, set up an application context
# with app.app_context(). See the documentation for more information.

from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for model for Users"""

    def setUp(self):
        """Clean up any existing users"""
        User.query.delete()

    def tearDown(self):
        """Clean up any unhandled transactions"""
        db.session.rollback()
