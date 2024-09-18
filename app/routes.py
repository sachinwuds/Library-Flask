from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity 
from werkzeug.utils import secure_filename
from app.models import Book
from app import db
import os

books_bp = Blueprint('books', __name__)

# Define where to store uploaded images
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List all books
@books_bp.route('/', methods=['GET'])
def list_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

# Create a new book (Admin only)
@books_bp.route('/', methods=['POST'])
@jwt_required()
def create_book():
    print(os.path.join(UPLOAD_FOLDER, "filename"))
    # return {"path":os.path}
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"msg": "Admin access required"}), 403
    
    file = None
    book_data = request.form

    # Check if ISBN already exists
    if Book.query.filter_by(isbn=book_data['isbn']).first():
        return jsonify({'error': 'A book with this ISBN already exists'}), 400
    
    if 'cover_image' in request.files:
        file = request.files['cover_image']
    
    # Check if the file is valid and allowed
    if file and allowed_file(file.filename):
        filename = book_data['isbn'] + "." + file.filename.split(".")[-1]
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    new_book = Book(
        title=book_data['title'],
          author=book_data['author'],
          isbn=book_data['isbn'],
          publication_year=book_data['publication_year'],
          cover_image = os.path.join(UPLOAD_FOLDER[4:], filename) if file else None
    )


    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({"msg": "Book created", "book": new_book.to_dict()}), 201

# Update a book by ID (Admin only)
@books_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"msg": "Admin access required"}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"msg": "Book not found"}), 404
    
    file = None
    book_data = request.form

    # If updating ISBN, check for uniqueness
    if 'isbn' in book_data and book_data['isbn'] != book.isbn:
        if Book.query.filter_by(isbn=book_data['isbn']).first():
            return jsonify({'error': 'A book with this ISBN already exists'}), 400
        
    if 'cover_image' in request.files:
        file = request.files['cover_image']

    # Check if the file is valid and allowed
    if file and allowed_file(file.filename):
        isbn = book_data['isbn'] if 'isbn' in book_data else book.isbn
        filename = isbn + "." + file.filename.split(".")[-1]
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
    book.title = book_data.get('title', book.title)
    book.author = book_data.get('author', book.author)
    book.isbn = book_data.get('isbn', book.isbn)
    book.publication_year = book_data.get('publication_year', book.publication_year)
    book.cover_image = os.path.join(UPLOAD_FOLDER[4:], filename) if file else book.cover_image
    db.session.commit()
    
    return jsonify({"msg": "Book updated", "book": book.to_dict()}), 200

# Delete a book by ID (Admin only)
@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"msg": "Admin access required"}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"msg": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"msg": "Book deleted"}), 200