import os

# App config
DEBUG = True

# DB connection
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'postgres://localhost:5432/daedam_test')
