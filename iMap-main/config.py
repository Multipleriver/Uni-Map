import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = b'_53oi3uriq9pifpff;apl'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app/', 'database/', 'locations.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
