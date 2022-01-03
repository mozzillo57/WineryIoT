from datetime import datetime
from schema import Winery, Sensor, Anomaly, Value
from flask import render_template, request, jsonify
from flask_template import app, db
from winerys import WineryManager
from config import Config
import json

wm = WineryManager(db)


@app.route("/")
def index():
    return render_template("index.html")    


@app.route("/winery/<winery_id>", methods=["GET"])
def winery(winery_id):
    print(winery_id)
    winery = wm.get_winery_by_id(winery_id)
    print("Winery", winery)
    sensors = wm.get_winery_sensors(winery_id)
    print("Sensors", sensors)
    data = wm.sensors_todict(winery_id)
    print("data", data)
    return render_template(
        "wyneri.html",  APIKEY=Config.GOOGLEMAPS_APIKEY, winery_id=winery_id, winery=winery, sensors=sensors, lng = winery.winery_long, lat = winery.winery_lat, data = data)


@app.route("/add/winery", methods=["POST"])
def add_winery():
    winery_id = request.form.get("winery_id", None)
    winery_lat = request.form.get("winery_lat", None)
    winery_long = request.form.get("winery_long", None)
    winery = Winery(winery_id, winery_lat, winery_long)
    print(winery)
    db.session.add(winery)
    db.session.commit()
    return str(winery.winery_id)


@app.route("/add/sensor", methods=["POST"])
def add_sensor():
    print(type(request.get_data()))
    sensor_id = request.form.get("sensor_id")
    sensor_type = request.form.get("sensor_type")
    winery_id = request.form.get("winery_id")
    winery = Winery.query.filter_by(winery_id=winery_id).first()
    sensor = Sensor(sensor_id, sensor_type, winery_id)
    winery.sensors.append(sensor)

    print(sensor_id, winery_id)
    print(sensor)
    db.session.add(sensor)
    db.session.commit()
    return str(sensor.sensor_id)


@app.route("/add/anomaly", methods=["POST"])
def add_anomaly():
    print(type(request.get_data()))
    anomaly_id = request.form.get("anomaly_id")
    sensor_id = request.form.get("sensor_id")
    sensor = wm.get_senor_by_id(sensor_id)
    anomaly = Anomaly(anomaly_id, sensor_id)
    sensor.anomaly_id = anomaly_id
    print(sensor, anomaly)
    db.session.add(anomaly)
    db.session.commit()
    print(sensor, sensor.anomaly_id)
    return str(anomaly.anomaly_id)

@app.route("/add/value", methods=["POST"])
def add_value():
    print(type(request.get_data()))
    value_id = datetime.now()
    val = request.form.get("value")
    sensor_id = request.form.get("sensor_id")
    print(sensor_id, val)
    sensor = wm.get_senor_by_id(sensor_id)
    print(sensor)
    value = Value(value_id, val, sensor_id)
    sensor.values.append(value)
    db.session.add(value)
    db.session.commit()
    print(value)
    for key, val in wm.sensors_todict(1).items():
        for v in val.items():
            print(key, v)
                
    return str(value.value_id)