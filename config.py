from os import environ, path
import os


class Config:
    #BASE_URL = "http://242b-151-67-220-217.ngrok.io"
    BASE_URL = "http://192.168.1.138:5000"
    GOOGLEMAPS_APIKEY = "AIzaSyDI4sT3Mi4HhNbjj2kphRkml2mK-GLnKPY"
    DISTTH = 0.01

    # General Flask Config
    SECRET_KEY = b"winerylove/"
    USE_PROXYFIX = True

    APPLICATION_ROOT = "/"

    FLASK_APP = "flask_template.py"
    FLASK_RUN_HOST = "0.0.0.0"
    FLASK_RUN_PORT = 5000

    FLASK_DEBUG = 1
    # FLASK_ENV = "development" #production
    FLASK_ENV = "production"  # production

    DEBUG = False
    TESTING = False  # True

    SESSION_TYPE = "sqlalchemy"  #'redis'
    SESSION_SQLALCHEMY_TABLE = "sessions"
    SESSION_COOKIE_NAME = "my_cookieGetFace"
    SESSION_PERMANENT = True

    # Database

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///wineryIOT.sqlite"  # = 'mysql://username:password@localhost/db_name'
    )

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "simple"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 100
    
    BOTKEY = '5027857717:AAEUr6p-IpLJMM3r6ObiDlr1qdE5syiaRMM'
    chatID = 837553416
