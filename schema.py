from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import backref
from flask_template import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.mutable import MutableList


class Value(db.Model):
    __tablename__ = "values"
    value_id = db.Column("value_id", db.DateTime, primary_key=True)
    val = db.Column("val", db.Float, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.sensor_id"), primary_key = True)

    def __init__(self, value_id, val, sensor_id):
        self.value_id = value_id
        self.val = val
        self.sensor_id = sensor_id

    def __repr__(self):
        return "<Value %r>" % self.val


class Sensor(db.Model):
    __tablename__ = "sensors"
    sensor_id = db.Column("sensor_id", db.Integer, primary_key=True)
    sensor_type = db.Column("sensor_type", db.String(1), nullable=False)
    values = db.relationship("Value", backref="sensors")
    # sensor_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    winery_id = db.Column(db.Integer, db.ForeignKey("winerys.winery_id"))
    anomaly = db.relationship("Anomaly", backref="sensor", uselist=False)

    def __init__(self, sensor_id, sensor_type, winery_id):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.winery_id = winery_id

    def __repr__(self):
        return "<Sensor %r>" % self.sensor_id


class Winery(db.Model):
    __tablename__ = "winerys"
    winery_id = db.Column("winery_id", db.Integer, primary_key=True)
    winery_lat = db.Column(db.Float, nullable=False)
    winery_long = db.Column(db.Float, nullable=False)
    sensors = db.relationship("Sensor", backref="winerys")

    def __init__(self, winery_id, winery_lat, winery_long):
        self.winery_id = winery_id
        self.winery_lat = winery_lat
        self.winery_long = winery_long

    def __repr__(self):
        return "<Winery %r>" % self.winery_id


class Anomaly(db.Model):
    __tablename__ = "anomalies"
    anomaly_id = db.Column("anomaly_id", db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.sensor_id"))

    def __init__(self, anomaly_id, sensor_id):
        self.anomaly_id = anomaly_id
        self.sensor_id = sensor_id

    def __repr__(self):
        return "<Anomaly %r>" % self.anomaly_id


if __name__ == "__main__":
    # db.create_all()
    print("SCHEMA")
