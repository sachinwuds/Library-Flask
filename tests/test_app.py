import unittest
import os
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Book
from flask_jwt_extended import create_access_token
from flask import url_for
admin = "admin5"
class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test environment."""
        # Create a test app and test database
        self.app = create_app("testing")  # Assuming you have a 'testing' config in config.py
        self.app.config['TESTING'] = True  # Enables testing mode
        self.app.config['DEBUG'] = True 
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test database
        db.create_all()
        
        # Create a test admin user
        self.admin_user = User(username= admin, password='admin123', is_admin=True)
        db.session.add(self.admin_user)
        db.session.commit()
        user = {"user_id": 1, "username":admin, "is_admin": True}

        # Get JWT token for admin
        self.admin_token = create_access_token(identity=user)

    def tearDown(self):
        """Clean up the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        """Test the login and token creation."""
        response = self.client.post('auth/login', json={
            'username': admin,
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)
    

    def test_create_book_with_cover_image(self):
        """Test book creation with cover image upload."""
        # Use JWT token for authentication
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }

        # Create a book with a cover image
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': '2024-01-01',
            'isbn':4
        }
        # Mock file upload
        with open('test_cover.png', 'rb') as cover_image:
            data['cover_image'] = (cover_image, 'test_cover.png')

            response = self.client.post('books/', headers=headers, data=data, content_type='multipart/form-data')
            # print(response.status_code)  # Will show the status code
            # print(response.get_data(as_text=True)) 
            # self.assertEqual(response.status_code, 201)

            # Verify book in response
            response_data = response.get_json()
            self.assertEqual(response_data['msg'], 'Book created')
            self.assertTrue(os.path.exists(os.path.join('app/static/uploads/', '4.png')))

    def test_get_books(self):
        """Test retrieving all books."""
        response = self.client.get('books/')
        self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        """Test updating an existing book (admin only)."""
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }

        # Create a book first
        book = Book(title='Initial Title', author='Initial Author',publication_year='2023')
        db.session.add(book)
        db.session.commit()
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            "publication_year":"2024"
        }

        # Update the book's title
        response = self.client.put(f'/books/{1}', 
                                   headers=headers,
                                   data = data,
                                   content_type='multipart/form-data'
                                )
        
        print(response.get_data(as_text=True)) 
        self.assertEqual(response.status_code, 200)

        # Check if the book was updated
        updated_book = Book.query.get(book.id)
        print(updated_book)
        self.assertEqual(updated_book.title, 'Updated Title')

    def test_delete_book(self):
        """Test deleting a book (admin only)."""
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }

        # Create a book first
        book = Book(title='Delete Me', author='Test Author',publication_year='2023')
        db.session.add(book)
        db.session.commit()

        # Delete the book
        response = self.client.delete(f'/books/{book.id}', headers=headers)
        self.assertEqual(response.status_code, 200)

        # Check if the book was deleted
        deleted_book = Book.query.get(book.id)
        self.assertIsNone(deleted_book)

    def test_unauthorized_create_book(self):
        """Test that non-admin users cannot create books."""
        # Simulate login as a regular user
        regular_user = User(username='user', password='user123', is_admin=False)
        db.session.add(regular_user)
        db.session.commit()
        user = {"username":"user", "password":"user123", "is_admin":False}

        regular_token = create_access_token(identity=user)

        headers = {
            'Authorization': f'Bearer {regular_token}'
        }

        response = self.client.post('books/', headers=headers, json={
            'title': 'Unauthorized Book',
            'author': 'Unauthorized Author'
        })
        self.assertEqual(response.status_code, 403)  # Should be forbidden for non-admin users

# Run the tests
if __name__ == '__main__':
    unittest.main()