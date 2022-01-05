from datetime import datetime
from schema import Winery, Sensor, Anomaly, Value
from flask import render_template, request, jsonify, redirect, url_for
from flask_template import app, db
from winerys import WineryManager
from config import Config
import requests
import json

wm = WineryManager(db)

@app.route("/")
def index():
    winerys = wm.get_all_winerys()
    return render_template("index.html", winerys=winerys)    

@app.route("/insert", methods=["GET", "POST"])
def insert():
    url_sen = 'http://127.0.0.1:5000/add/sensor'
    url_val = 'http://127.0.0.1:5000/add/value'
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        sensor_type = request.form['sensor_type']
        winery_id = 1
        value =  request.form['value']
        sensor = {"sensor_id": sensor_id, "sensor_type": sensor_type, 'winery_id': winery_id}
        x = requests.post(url_sen, data=sensor)
        val = {"value": value, "sensor_id": sensor_id}
        x2 = requests.post(url_val, data=val)
    return render_template('insert.html')
    

@app.route("/winery/<winery_id>", methods=["GET"])
def winery(winery_id):
    winery = wm.get_winery_by_id(winery_id)
    sensors = wm.get_winery_sensors(winery_id)
    data = wm.sensors_todict(winery_id)
    return render_template(
        "wyneri.html",  APIKEY=Config.GOOGLEMAPS_APIKEY, winery_id=winery_id, winery=winery, sensors=sensors, lng = winery.winery_long, lat = winery.winery_lat)


@app.route("/anomaly/<anomaly_id>")
def anomaly(anomaly_id):
    anomaly = wm.get_anomaly_by_id(anomaly_id)
    sensor = wm.get_senor_by_id(anomaly.sensor_id)
    winery_id = sensor.winery_id
    print(anomaly, sensor)
    return render_template("anomaly.html", anomaly = anomaly, winery_id = winery_id)  

@app.route("/add/winery", methods=["POST"])
def add_winery():
    winery_id = request.form.get("winery_id", None)
    winery_lat = request.form.get("winery_lat", None)
    winery_long = request.form.get("winery_long", None)
    winery = Winery(winery_id, winery_lat, winery_long)
    db.session.add(winery)
    db.session.commit()
    return str(winery.winery_id)

@app.route("/add/sensor", methods=["POST"])
def add_sensor():
    sensor_id = request.form.get("sensor_id")
    sensor_type = request.form.get("sensor_type")
    winery_id = request.form.get("winery_id")
    winery = Winery.query.filter_by(winery_id=winery_id).first()
    sensor = Sensor(sensor_id, sensor_type, winery_id)
    winery.sensors.append(sensor)
    db.session.add(sensor)
    db.session.commit()
    return str(sensor.sensor_id)

@app.route("/add/anomaly", methods=["POST"])
def add_anomaly():
    anomaly_id = request.form.get("anomaly_id")
    sensor_id = request.form.get("sensor_id")
    sensor = wm.get_senor_by_id(sensor_id)
    anomaly = Anomaly(anomaly_id, sensor_id)
    sensor.anomaly_id = anomaly_id
    db.session.add(anomaly)
    db.session.commit()
    return str(anomaly.anomaly_id)

@app.route("/remove_anomaly", methods=["POST"])
def remove_anomaly():
    anomaly_id = request.form.get("anomaly_id")
    anomaly = wm.get_anomaly_by_id(anomaly_id)
    sensor = wm.get_senor_by_id(anomaly.sensor_id)
    winery_id = sensor.winery_id
    db.session.delete(anomaly)
    db.session.commit()
    return redirect(url_for('winery', winery_id = winery_id))


@app.route("/add/value", methods=["POST"])
def add_value():
    value_id = datetime.now()
    val = request.form.get("value")
    sensor_id = request.form.get("sensor_id")
    sensor = wm.get_senor_by_id(sensor_id)
    value = Value(value_id, val, sensor_id)
    sensor.values.append(value)
    db.session.add(value)
    db.session.commit()
    for key, val in wm.sensors_todict(1).items():
        for v in val.items():
            print(key, v)
                
    return str(value.value_id)


