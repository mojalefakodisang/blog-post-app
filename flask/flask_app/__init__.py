"""Module that servies as an app for our Blog Post Web application"""
import logging
import os
from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_app.config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info('Initializing extensions..')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    logger.info('Extensions initialized')

    logger.info('Registering blueprints..')
    from flask_app.users.routes import users
    from flask_app.posts.routes import posts
    from flask_app.main.routes import main
    from flask_app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    logger.info('Blueprints registered')

    return app
