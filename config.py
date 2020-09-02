"""Flask config."""
import os
from os import environ, path


class Config:
    """Base config."""

    API_VERSION = "0.0.1"
    JWT_SECRET_KEY = open("/run/secrets/jwt_secret_key", "r").read().strip()
    SETUP_KEY = open("/run/secrets/setup_key", "r").read().strip()
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    BASE_DIR = "/var/www/connector/"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_PASSWORD = open("/run/secrets/psql_password", "r").read().strip()
    POSTGRES_USER = open("/run/secrets/psql_user", "r").read().strip()
    POSTGRES_DB = open("/run/secrets/psql_db", "r").read().strip()
    DB_SERVER_NAME = "db"
    DB_SERVER_PORT = "5432"
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        POSTGRES_USER, POSTGRES_PASSWORD, DB_SERVER_NAME, DB_SERVER_PORT, POSTGRES_DB
    )
    DEFAULT_USER_NAME = os.environ.get("DEFAULT_USER_NAME", default="user")
    DEFAULT_USER_PASSWD = os.environ.get("DEFAULT_USER_PASSWD", default="user")

    DEFAULT_ADMIN_NAME = os.environ.get("DEFAULT_USER_NAME", default="admin")
    DEFAULT_ADMIN_PASSWD = os.environ.get("DEFAULT_USER_PASSWD", default="admin")


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
