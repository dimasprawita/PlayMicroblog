# application will exist in a package
# a sub-directory that includes a __init__.py is considered a package

# when you import a package, the __init__.py executes and defines 
# what symbols the package exposes to the outside world
from flask import Flask

# import the Config class from config.py
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler


# creates application object as an instance of Flask
# __name__ is python predefined variable
app = Flask(__name__)
app.config.from_object(Config)

# add db object and migration engine.
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# created and initiliazied flask-login
login = LoginManager(app)
login.login_view = 'login'

# creates a SMTPHandler instance, sets its level so that it only reports errors
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    # RotatingFileHandler rotates the logs, ensuring that the log files do not grow too large
    # the size is limited to 10KB and we're keeping the last ten log files as backup
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,backupCount=10)

    # custom formatting for the log messages
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

# the application the imports the routes module
# app package is defined by app dir and __init__.py script, referenced in from app import routes
# app variable is defined as an instance of class Flask, which makes it a member of the app package
from app import routes, models, errors
