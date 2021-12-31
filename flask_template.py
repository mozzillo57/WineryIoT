from flask import Flask
from flask_restful import Resource, Api
from flask import Flask, request, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)

if __name__ == "__main__":
    from views import *
    db.drop_all()
    db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)
