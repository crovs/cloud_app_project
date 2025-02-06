import unittest
import os

from app import app, db, User, Task

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['TESTING'] = True
class CloudAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for testing
        self.app = app
        self.client = self.app.test_client()  # Initialize the test client
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_user_registration(self):
        response = self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        # Register user
        self.client.post('/register', json={'username': 'testuser2', 'password': 'testpass2'})
        # Login user
        self.client.post('/login', json={'username': 'testuser2', 'password': 'testpass2'})
        # Create task
        response = self.client.post('/tasks', json={'title': 'Test Task'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
