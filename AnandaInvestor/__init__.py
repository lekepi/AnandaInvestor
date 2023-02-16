from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from AnandaInvestor.config import ConfigDefault
from flask_principal import Principal, Permission, RoleNeed

db = SQLAlchemy()  # for DB
bcrypt = Bcrypt()  # hash password
login_manager = LoginManager()  # from flask_login
login_manager.login_view = 'users.login'  # default page
login_manager.login_message_category = 'warning'
mail = Mail()
principals = Principal()  # from flask principal used for permission
admin_permission = Permission(RoleNeed('Admin'))
investor_permission = Permission(RoleNeed('Investor'))


def create_app(config_class=ConfigDefault):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
        principals.init_app(app)

        # from AnandaIntranet import routes

        from AnandaInvestor.admin.routes import admin
        from AnandaInvestor.investor.routes import investor
        from AnandaInvestor.users.routes import users
        from AnandaInvestor.main.routes import main
        from AnandaInvestor.errors.handlers import errors

        app.register_blueprint(admin)
        app.register_blueprint(main)
        app.register_blueprint(investor)
        app.register_blueprint(users)
        app.register_blueprint(errors)

        return app
