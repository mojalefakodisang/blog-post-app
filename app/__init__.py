"""Module that serves as an app for our Blog Post Web application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = "1c44f7b5791dd8ee15c99cbe3ba54bea"
db = SQLAlchemy(app)

from app import routes