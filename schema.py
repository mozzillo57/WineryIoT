from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_template import db
from sqlalchemy.ext.hybrid import hybrid_property


class Sensor(db.Model):
    __tablename__ = "sensors"
    sensor_id = db.Column("sensor_id", db.Integer, primary_key=True)

    sensor_type = db.Column("sensor_type", db.String(20))

    sensor_value = db.Column("sensor_value", db.String(100))

    sensor_time = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)

    winery_id = db.Column(db.Integer, db.ForeignKey("winerys.winery_id"))

    anomaly = db.relationship("Anomaly", back_populates="sensors", uselist = False)

    def __repr__(self):
        return "<Sensor %r>" % self.sensor_id
    # winery = db.relationship("Winery")

    def __init__(self, sensor_id, sensor_type, sensor_value, winery_id):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_value = sensor_value
        self.winery_id = winery_id
        self.sensor_timestamp = datetime.now()

    def __repr__(self):
        return "<Sensor %r>" % self.sensor_id


class Winery(db.Model):
    __tablename__ = "winerys"
    winery_id = db.Column("winery_id", db.Integer, primary_key=True)

    winery_location = db.Column(db.String(80))

    sensors = db.relationship("Sensor", backref="winerys")

    def __init__(self, winery_id, winery_location):
        self.winery_id = winery_id
        self.winery_location = winery_location

    def __repr__(self):
        return "<Winery %r>" % self.winery_id


class Anomaly(db.Model):
    __tablename__ = "anomalies"
    anomaly_id = db.Column("anomaly_id", db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.sensor_id"))
    sensor = db.relationship("Sensor", back_populates="anomaly")
    
    
    def __init__(self, anomaly_id, sensor_id):
        self.anomaly_id = anomaly_id
        self.sensor_id = sensor_id

    def __repr__(self):
        return "<Anomaly %r>" % self.anomaly_id

if __name__ == "__main__":
    #db.create_all()
    print("SCHEMA")
