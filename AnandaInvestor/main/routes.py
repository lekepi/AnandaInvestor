from flask import Blueprint, render_template, url_for, current_app
from flask_login import login_required


main = Blueprint('main', __name__)


@main.before_request
def check_under_maintenance():
    maintenance_mode = current_app.config['MAINTENANCE_MODE']
    if maintenance_mode == 'ON':
        return render_template('errors/503.html'), 503


@main.route('/home')
@main.route('/')
@login_required
def home():
    image_file = url_for('static', filename='ananda.JPG')
    return render_template('main/home.html', image_file=image_file)


@main.route('/webinar/<int:start_time>')
@login_required
def webinar(start_time):
    video_url = url_for('static', filename='videos/Ananda Webinar 23-05-2023.mp4')
    video_url_with_time = f'{video_url}?start={start_time}'
    return render_template('main/webinar.html', title='Webinar', video_url=video_url_with_time)
