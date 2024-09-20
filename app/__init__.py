from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, resources={r"*": {"origins": "*"}})

    # Load configurations
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    elif config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from app.routes import books_bp
    from app.auth import auth_bp
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Create tables before the first request
    @app.before_request
    def create_tables():
        db.create_all()

    return app