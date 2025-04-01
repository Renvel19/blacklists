import os

from datetime import timedelta

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(hours=100)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

