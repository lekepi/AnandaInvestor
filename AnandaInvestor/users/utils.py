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
    msg = Message('Ananda - Join Webinar', sender='ananda.am.system@gmail.com', recipients=[user.email])
    msg.body = f'''Please click on the following link:
{url_for('users.reset_token', token=token, _external=True)}
    '''
    # _external=True to get absolute URL
    mail.send(msg)


def send_activity_email(my_text):
    mail_to = current_app.config['ML_CONNECT']
    mail_list = mail_to.split(',')
    msg = Message(my_text, sender='ananda.am.system@gmail.com', recipients=mail_list)
    mail.send(msg)
