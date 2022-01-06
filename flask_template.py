from flask import Flask
from flask_restful import Resource, Api
from flask import Flask, request, render_template
from config import Config
import googlemaps
from flask_sqlalchemy import SQLAlchemy
import os
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
myconfig = Config
app.config.from_object(myconfig)
db = SQLAlchemy(app)
gmaps = googlemaps.Client(key=Config.GOOGLEMAPS_APIKEY)
#run_with_ngrok(app)

if __name__ == "__main__":
    from views import *

    db.drop_all()
    db.create_all()
    app.run(host= Config.FLASK_RUN_HOST, port=Config.FLASK_RUN_PORT, debug=Config.FLASK_DEBUG)
