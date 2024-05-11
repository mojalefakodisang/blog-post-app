import os
import secrets
from PIL import Image
from app import app, db, bcrypt
from app.model import User, Post
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, url_for, flash, redirect, request, abort


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    """
    Render the home page.

    Returns:
        The rendered home.html template with the title set to "Home" and posts set to post.
    """
    post = Post.query.all()
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful! Welcome back, {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and/or password', 'danger')
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been successfully created!', 'success')
        return redirect(url_for('home', name=f"{form.username.data}"))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', filename)
    
    # image resize
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return filename

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            filename = save_picture(form.picture.data)
            current_user.image_file = filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account is successfully updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')
    
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('home'))