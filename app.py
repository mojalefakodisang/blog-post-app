"""Module that serves as an app for our Blog Post Web application"""
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask import Flask, render_template, url_for, flash, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = "1c44f7b5791dd8ee15c99cbe3ba54bea"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

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


post = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    """
    Render the home page.

    Returns:
        The rendered home.html template with the title set to "Home" and posts set to post.
    """
    return render_template("home.html", title="Home", posts=post)

@app.route("/about")
def about():
    """
    Renders the about.html template with the title "About".

    Returns:
        The rendered HTML page.
    """
    return render_template("about.html", title="About")

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Logs in the user.

    This function handles the login process for the user. It validates the login form,
    checks if the provided email and password match the admin credentials, and redirects
    the user to the home page if the login is successful. Otherwise, it displays an error
    message and renders the login page again.

    Returns:
        If the login is successful, it redirects the user to the home page.
        Otherwise, it renders the login page with an error message.

    """
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username/email and password', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This function handles the registration process for a new user. It renders the registration form,
    validates the form data, creates a new user account, and redirects the user to the home page.

    Returns:
        A redirect response to the home page with the username as a query parameter.

    """
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home', name=f"{form.username.data}"))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)