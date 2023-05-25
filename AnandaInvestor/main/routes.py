from flask import Blueprint, render_template, url_for, current_app
from flask_login import login_required


main = Blueprint('main', __name__)


@main.before_request
def check_under_maintenance():
    maintenance_mode = current_app.config['MAINTENANCE_MODE']
    if maintenance_mode == 'ON':
        return render_template('errors/503.html'), 503


@main.route('/home_old')
@main.route('/')
@login_required
def home_old():
    image_file = url_for('static', filename='ananda.JPG')
    return render_template('main/home.html', image_file=image_file)


@main.route('/home')
@login_required
def home():
    video_url = url_for('static', filename='videos/Ananda Webinar 23-05-2023.mp4')
    return render_template('main/home.html', title='Webinar', video_url=video_url)
