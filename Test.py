import unittest
from flask import Flask
from flask_testing import TestCase
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash




class AuthTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        user = User(email='test@example.com', first_name='Test', password=generate_password_hash('password', method='sha256'))
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        response = self.client.post('/login', data=dict(email='test@example.com', password='password'), follow_redirects=True)
        self.assert200(response)
        self.assertNotIn(b'Incorrect password, try again.', response.data)
        self.assertIn(b'Logged in successfully!', response.data)

    # Add more test methods for different scenarios

if __name__ == '__main__':
    unittest.main()
