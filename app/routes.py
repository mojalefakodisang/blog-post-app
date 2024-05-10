from app import app
from app.model import User, Post
from app.forms import RegistrationForm, LoginForm
from flask import Flask, render_template, url_for, flash, redirect

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
