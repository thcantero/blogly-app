from unittest import TestCase
from app import app
from models import db, User

# with app.app_context():
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test' 
app.config['SQLALCHEMY_ECHO'] = False

#Make Flask errors be real errors
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user = User(first_name='John', last_name='Doe')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.user_id

    def tearDown(self):
        """Clean up any fouled transactions"""
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('John Doe', html)
    
    def test_show_user(self):
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            #self.assertIn(, html)

    # def test_create_user(self):
    #     with app.test_client() as client:
    #         d = {"first_name": "Jane", "last_name": "Doe"}
    #         response = client.post("/users/new", data=d, follow_redirects=True)
    #         html = response.get_data(as_text=True)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('Jane Doe', html)