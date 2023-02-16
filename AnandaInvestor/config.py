from configparser import ConfigParser
import os
from pathlib import Path
import cryptocode

THIS_DIR = Path(__file__)
config_path = THIS_DIR.parent.parent
config_path_file = os.path.join(config_path, 'default_config.ini')


class ConfigDefault:
    config = ConfigParser()
    config.read(config_path_file)
    DEFAULT_CONFIG = config['MAIN']['DEFAULT_CONFIG']
    if DEFAULT_CONFIG == 'ConfigProd':
        SECRET_KEY = config['SECRET_KEY']['CODE']
        SQLALCHEMY_DATABASE_URI = config['DB']['SQLALCHEMY_DATABASE_URI']
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = '587'
        MAIL_USE_TLS = True
        MAIL_USERNAME_ENCRYPTED = config['EMAIL']['EMAIL_USER']
        MAIL_USERNAME = cryptocode.decrypt(MAIL_USERNAME_ENCRYPTED, SECRET_KEY)
        MAIL_PASSWORD_ENCRYPTED = config['EMAIL']['EMAIL_PASS']
        MAIL_PASSWORD = cryptocode.decrypt(MAIL_PASSWORD_ENCRYPTED, SECRET_KEY)
        APPLICATION_TYPE = 'PROD'
        MAINTENANCE_MODE = config['OTHER']['MAINTENANCE_MODE']

