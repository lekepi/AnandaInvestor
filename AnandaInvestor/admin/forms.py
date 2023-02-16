from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
from AnandaInvestor.models import AuthEmails
from datetime import datetime


class AuthEmailsForm(FlaskForm):
    email = StringField('New Email', validators=[Email(), DataRequired()])
    submit = SubmitField('Add')

    def validate_email(self, email):
            my_email = AuthEmails.query.filter_by(email=email.data).first()
            if my_email:
                raise ValidationError('That email already exists. Please choose a different one')


class RoleForm(FlaskForm):
    role = SelectField(u'Role', coerce=int)
    submit = SubmitField('Add')


class ChangeUserForm(FlaskForm):
    change_user = SelectField(u'User', coerce=int)
    submit = SubmitField('Change User')

