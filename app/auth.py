from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    is_admin = request.json.get('is_admin', False)

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    if is_admin == 'true':
        is_admin = True
    new_user = User(username=username, password=password, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered", "user": new_user.to_dict()}), 201

# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity={"username": user.username, "is_admin": user.is_admin})
    return jsonify(access_token=access_token), 200