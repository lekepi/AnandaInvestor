from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from AnandaInvestor import db, bcrypt
from AnandaInvestor.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    RequestResetForm, ResetPasswordForm
from AnandaInvestor.models import User, UserActivity
from flask_login import login_user, current_user, logout_user, login_required
from AnandaInvestor.users.utils import save_picture, send_reset_email
from flask_principal import Identity, AnonymousIdentity, identity_changed, \
    identity_loaded, UserNeed, RoleNeed
from AnandaInvestor.admin.utils import add_log

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


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.password_try <= 0:
                flash('login locked, please contact IT to reset your account', 'danger')
            elif bcrypt.check_password_hash(user.password, form.password.data):
                user.password_try = 5
                db.session.commit()
                # login_user(user, remember=form.remember.data)
                login_user(user, remember=False)
                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

                logging_text = f'{user.first_name} {user.last_name} logged in'
                add_log(logging_text)
                new_user_activity = UserActivity(user_id=user.id)
                db.session.add(new_user_activity)
                db.session.commit()
                next_page = request.args.get('next')  # will be none if not there
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:  # wrong password
                user.password_try -= 1
                db.session.commit()
                flash(f'login unsuccessful, wrong password password, {user.password_try} tries left', 'danger')
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
        flash('your account has been update', 'success')
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
        flash('an email has been sent with instructions to reset your password.', 'info')
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
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated, you are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset password', form=form)


@users.route('/maintenance/')
def maintenance():
    return render_template('users/maintenance.html', title='Maintenance')