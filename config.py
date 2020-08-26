import os
basedir = os.path.abspath(os.path.dirname(__file__))

# use a class to store configuration variables
# as the app needs more configuration items, they can be added to this class
class Config(object):
    # flask uses the value of the secret key as a cryptographic key, useful to generate signatures or tokens
    # two terms: 1. SECRET_KEY value of an environment variable, 2. hardcoded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # flask-slqalchemy takes the loc. of the app's database from URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    # disable a feature of sqlalchemy that we don't need
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    POSTS_PER_PAGE = 3