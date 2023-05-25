from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from AnandaInvestor import db, bcrypt
from AnandaInvestor.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    RequestResetForm, ResetPasswordForm
from AnandaInvestor.models import User, UserActivity, AuthEmails
from flask_login import login_user, current_user, logout_user, login_required
from AnandaInvestor.users.utils import save_picture, send_reset_email
from flask_principal import Identity, AnonymousIdentity, identity_changed, \
    identity_loaded, UserNeed, RoleNeed
from AnandaInvestor.admin.utils import add_log
from AnandaInvestor.users.utils import send_activity_email


users = Blueprint('users', __name__)


@users.before_request
def check_under_maintenance():
    maintenance_mode = current_app.config['MAINTENANCE_MODE']
    if maintenance_mode == 'ON':
        return render_template('errors/503.html'), 503


# @identity_loaded.connect_via(current_app._get_current_object())
@identity_loaded.connect_via(current_app._get_current_object())
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))


@users.route('/webinar', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data)

        my_text = f"The user {user.first_name} {user.last_name} ({user.email}) registered into Ananda Website"
        send_activity_email(my_text)
        new_user_activity = UserActivity(user_id=user.id, action='Register')
        db.session.add(new_user_activity)
        db.session.commit()
        logging_text = f'{user.first_name} {user.last_name} {user.email} registered'
        add_log(logging_text)

        db.session.add(user)
        db.session.commit()

        send_reset_email(user)
        flash(f'Your account has been created. An email has been sent to {user.email} to confirm your identity.', 'info')

        return redirect(url_for('users.notification'))
    return render_template('users/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user, remember=False)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

            logging_text = f'{user.first_name} {user.last_name} {user.email} logged in'
            add_log(logging_text)
            my_text = f"The user {user.first_name} {user.last_name} ({user.email}) logged in into Ananda Website"
            send_activity_email(my_text)
            new_user_activity = UserActivity(user_id=user.id, action='Login')
            db.session.add(new_user_activity)
            db.session.commit()
            next_page = request.args.get('next')  # will be none if not there
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('login unsuccessful, this email does not exist', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    identity_changed.send(current_app, identity=AnonymousIdentity())
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updateD', 'success')
        return redirect(url_for('users.account'))  # need to redirect to have a get request this time
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent to {user.email} with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:  # if not user
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    else:
        logout_user()
        identity_changed.send(current_app, identity=AnonymousIdentity())
        login_user(user, remember=False)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        flash(f'Your password has been updated. You are now logged in.', 'success')
        my_text = f"The user {user.first_name} {user.last_name} ({user.email}) logged in into Ananda Website"
        send_activity_email(my_text)
        return redirect(url_for('main.webinar', start_time=0))


@users.route('/maintenance/')
def maintenance():
    return render_template('users/maintenance.html', title='Maintenance')


@users.route('/notification/')
def notification():
    return render_template('users/notification.html')