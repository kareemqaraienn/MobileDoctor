import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
