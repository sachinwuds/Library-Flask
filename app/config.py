import os
import datetime
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'  
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/book_covers')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max 16MB upload size
    

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
    DEBUG = True

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_library.db'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prodlibrary.db'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_SECRET_KEY = 'super-secret-key' # Change this for production,