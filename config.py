"""Flask config."""
import os
from os import environ, path

class Config:
    """Base config."""
    API_VERSION = '0.0.1'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SETUP_KEY = os.environ.get('SETUP_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    BASE_DIR = '/var/www/connector/'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    DB_SERVER_NAME = os.environ.get('DB_SERVER_NAME')
    DB_SERVER_PORT = os.environ.get('DB_SERVER_PORT', default="5432")
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(POSTGRES_USER, POSTGRES_PASSWORD,
                                                                        DB_SERVER_NAME, DB_SERVER_PORT, POSTGRES_DB)
    DEFAULT_USER_NAME = os.environ.get('DEFAULT_USER_NAME',default='user')
    DEFAULT_USER_PASSWD = os.environ.get('DEFAULT_USER_PASSWD',default='user')

    DEFAULT_ADMIN_NAME = os.environ.get('DEFAULT_USER_NAME',default='admin')
    DEFAULT_ADMIN_PASSWD = os.environ.get('DEFAULT_USER_PASSWD',default='admin')



class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True



