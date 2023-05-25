import secrets
import os
from PIL import Image
from flask import url_for
from flask_mail import Message
from AnandaInvestor import mail
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # f_name, f_ext = os.path.splitext(form_picture.filename) # use OS
    _, f_ext = os.path.splitext(form_picture.filename)  # use OS
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='ananda.am.system@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request simply ignore this email
    '''
    # _external=True to get absolute URL
    mail.send(msg)


def send_activity_email(user, activity):
    my_text = f"The user {user.first_name} {user.last_name} {user.email} {activity}"
    mail_to = current_app.config['ML_CONNECT']
    msg = Message(my_text, sender='ananda.am.system@gmail.com', recipients=[mail_to])
    mail.send(msg)