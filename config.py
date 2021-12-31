from os import environ, path
import os


class Config:

    # General Flask Config
    SECRET_KEY = b'winerylove/'
    USE_PROXYFIX = True

    APPLICATION_ROOT = '/'

    FLASK_APP = 'flask_template.py'
    FLASK_RUN_HOST = '127.0.0.1'
    FLASK_RUN_PORT = 5000

    FLASK_DEBUG = 0
    # FLASK_ENV = "development" #production
    FLASK_ENV = "production"  # production

    DEBUG = False
    TESTING = False  # True

    SESSION_TYPE = 'sqlalchemy'  # 'redis'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_COOKIE_NAME = 'my_cookieGetFace'
    SESSION_PERMANENT = True

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///example.sqlite"  # = 'mysql://username:password@localhost/db_name'

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "simple"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 100
