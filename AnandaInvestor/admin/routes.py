from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from AnandaInvestor import admin_permission, db
from flask_login import login_user, login_required, logout_user, current_user
from AnandaInvestor.models import User, AuthEmails, Role, UserRoles, LogDb
from AnandaInvestor.admin.forms import AuthEmailsForm, RoleForm, ChangeUserForm
from flask_principal import Identity,  identity_changed, AnonymousIdentity

from AnandaInvestor.admin.utils import add_log
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)


@admin.before_request
def check_under_maintenance():
    maintenance_mode = current_app.config['MAINTENANCE_MODE']
    if maintenance_mode == 'ON':
        return render_template('errors/503.html'), 503


@admin.route('/admin/userlist')
@admin_permission.require(http_exception=403)
@login_required
def admin_userlist():
    users = User.query.all()
    return render_template('admin/userlist.html', title='Admin', users=users)


@admin.route('/admin/userlist/resetPwdTry/<int:id>')
@admin_permission.require(http_exception=403)
@login_required
def admin_userlist_reset_pwd_try(id):
    user = User.query.get(id)
    user.password_try = 5
    db.session.commit()
    return redirect(url_for('admin.admin_userlist'))


@admin.route('/admin/userlist/roles/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def admin_userlist_roles(id):
    form = RoleForm()
    form.role.choices = [(r.id, r.name) for r in Role.query.order_by('name')]
    user = User.query.get(id)
    if form.validate_on_submit():
        my_role = Role.query.get(form.role.data)

        existing_role = UserRoles.query.filter_by(user_id=user.id, role_id=my_role.id).first()
        if existing_role:
            flash(f'The role \'{my_role.name}\' already exists for {user.first_name} {user.last_name}',
                  'danger')
        else:
            new_user_role = UserRoles(user_id=user.id, role_id=my_role.id)
            db.session.add(new_user_role)
            db.session.commit()
            flash(f'The role \'{my_role.name}\' has been successfully added for {user.first_name} {user.last_name}', 'success')
        return redirect(url_for('admin.admin_userlist_roles', id=id))
    return render_template('admin/users_roles.html', title='User_roles',
                           user=user, form=form)


@admin.route('/admin/userlist/roles/<int:user_id>/delete/<int:role_id>')
@admin_permission.require(http_exception=403)
@login_required
def delete_user_role(user_id, role_id):
    user_role = UserRoles.query.filter_by(user_id=user_id, role_id=role_id).first()
    db.session.delete(user_role)
    db.session.commit()
    flash(f'The role has been deleted', 'success')
    return redirect(url_for('admin.admin_userlist_roles', id=user_id))


@admin.route('/admin/auth_emails', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def admin_auth_emails():
    emails = AuthEmails.query.all()
    form = AuthEmailsForm()
    if form.validate_on_submit():
        new_email = AuthEmails(email=form.email.data)
        db.session.add(new_email)
        db.session.commit()
        flash('The email has been successfully added to the authorized list', 'success')
        return redirect(url_for('admin.admin_auth_emails'))
    return render_template('admin/auth_emails.html', title='Admin', emails=emails, form=form)


@admin.route('/admin/auth_emails/delete/<int:id>/')
@admin_permission.require(http_exception=403)
@login_required
def delete_auth_emails(id):
    email = AuthEmails.query.get(id)
    db.session.delete(email)
    db.session.commit()
    return redirect(url_for('admin.admin_auth_emails'))


@admin.route('/admin/change_user/', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def change_user():
    form = ChangeUserForm()

    form.change_user.choices = [(r.id, r.email) for r in User.query.order_by('email')]

    if form.validate_on_submit():
        user = User.query.filter_by(id=form.change_user.data).first()
        logout_user()
        identity_changed.send(current_app, identity=AnonymousIdentity())
        login_user(user, remember=False)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        logging_text = f'{user.first_name} {user.last_name} logged in'
        add_log(logging_text)
        next_page = request.args.get('next')  # will be none if not there
        return redirect(next_page) if next_page else redirect(url_for('main.home'))

    return render_template('admin/change_user.html', title='Admin - change user', form=form)
