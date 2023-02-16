from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

investor = Blueprint('investor', __name__)


@investor.before_request
def check_under_maintenance():
    maintenance_mode = current_app.config['MAINTENANCE_MODE']
    if maintenance_mode == 'ON':
        return render_template('errors/503.html'), 503