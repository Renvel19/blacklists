import os

from datetime import timedelta

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'mi_clave_secreta')
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(hours=100)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',"sqlite:///blacklists.db")
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

