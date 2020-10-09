"""Flask config."""
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    API_VERSION = "0.9.0"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SETUP_KEY = os.environ.get("SETUP_KEY")
    STATIC_FOLDER = "static"
    STATIC_URL = os.environ.get("STATIC_URL")
    TEMPLATES_FOLDER = "templates"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    DB_SERVER_NAME = os.environ.get("DB_SERVER_NAME")
    DB_SERVER_PORT = os.environ.get("DB_SERVER_PORT")
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        POSTGRES_USER, POSTGRES_PASSWORD, DB_SERVER_NAME, DB_SERVER_PORT, POSTGRES_DB
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    DEFAULT_ADMIN = os.environ.get("DEFAULT_ADMIN")
    DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL")
    DEFAULT_ADMIN_PASSWD = os.environ.get("DEFAULT_ADMIN_PASSWD")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
