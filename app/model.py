"""Module containing our User models"""
from app import db
from datetime import datetime


class User(db.Model):
    """
    Represents a user in the blog post application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        image_file (str): The filename of the user's profile image.
        password (str): The hashed password of the user.
        posts (list): A list of posts authored by the user.

    Methods:
        __repr__(): Returns a string representation of the User object.

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object in the format User(username, email, image_file).
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Post(db.Model):
    """
    Represents a blog post.

    Attributes:
        id (int): The unique identifier for the post.
        title (str): The title of the post.
        date_posted (datetime): The date and time when the post was created.
        content (str): The content of the post.
        user_id (int): The foreign key referencing the user who created the post.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """
        Returns a string representation of the Post object.
        The returned string includes the title and date_posted attributes of the Post object.
        Returns:
            str: A string representation of the Post object.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
