import os
import secrets
from PIL import Image
from flask import url_for
from app import app, mail
from flask_mail import Message

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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('[NO REPLY] Password Reset Request',
                  sender=os.environ.get('EMAIL_USER'),
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not request, please ignore this email!
"""
    mail.send(msg)