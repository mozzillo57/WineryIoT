from datetime import datetime
from schema import Winery, Sensor, Anomaly, Value
from flask import render_template, request, jsonify, redirect, url_for
from flask_template import app, db
from winerys import WineryManager
from config import Config
import requests
import telegram
from bridge_server_seriale import Bridge_Server_Seriale
from random import randint

wm = WineryManager(db)
url_sen = Config.BASE_URL + 'add/sensor'
url_val = Config.BASE_URL + 'add/value'
bot = telegram.Bot(Config.BOTKEY)
bss = Bridge_Server_Seriale()
bss.setup()

def create_payload(winery_id, rm = 0):
    if rm != -1:
        sensors = wm.get_all_sensors_with_anomaly(winery_id)
    else:
        sensors = rm

    payload = {
        'winery_id': winery_id,
        'sensor': sensors
    }
    return payload

@app.route("/")
def index():
    winerys = wm.get_all_winerys()
    return render_template("index.html", winerys=winerys)    

@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        sensor_type = request.form['sensor_type']
        value =  request.form['value']
        winery_id = 3
        sensor = {"sensor_id": sensor_id, "sensor_type": sensor_type, 'winery_id': winery_id}
        requests.post(url_sen, data=sensor)
        val = {"value": value, "sensor_id": sensor_id}
        requests.post(url_val, data=val)
    return render_template('insert.html')
    

@app.route("/winery/<winery_id>", methods=["GET"])
def winery(winery_id):
    winery = wm.get_winery_by_id(winery_id)
    sensors = wm.get_winery_sensors(winery_id)
    return render_template(
        "wyneri.html",  APIKEY=Config.GOOGLEMAPS_APIKEY, winery=winery, sensors=sensors)


@app.route("/anomaly/<anomaly_id>")
def anomaly(anomaly_id):
    anomaly = wm.get_anomaly_by_id(anomaly_id)
    sensor = wm.get_senor_by_id(anomaly.sensor_id)
    winery_id = sensor.winery_id
    return render_template("anomaly.html", anomaly = anomaly, winery_id = winery_id)  

@app.route("/add/winery", methods=["POST"])
def add_winery():
    winery_id = request.form.get("winery_id", None)
    winery_lat = request.form.get("winery_lat", None)
    winery_long = request.form.get("winery_long", None)
    winery = wm.get_winery_by_id(winery_id)
    if not winery:
        winery = Winery(winery_id, winery_lat, winery_long)
        db.session.add(winery)
        db.session.commit()
    
    return str(winery.winery_id)
    

@app.route("/add/sensor", methods=["POST"])
def add_sensor():
    sensor_id = request.form.get("sensor_id")
    sensor_type = request.form.get("sensor_type")
    winery_id = request.form.get("winery_id")
    sensor = wm.get_senor_by_id(sensor_id)
    if not sensor:
        winery = Winery.query.filter_by(winery_id=winery_id).first()
        sensor = Sensor(sensor_id, sensor_type, winery_id)
        winery.sensors.append(sensor)
        db.session.add(sensor)
        db.session.commit()
    return str(sensor.sensor_id)

@app.route("/add/anomaly", methods=["POST"])
def add_anomaly():
    sensor_id = request.form.get("sensor_id")
    sensor = wm.get_senor_by_id(sensor_id)
    for s in wm.get_all_sensors_by_type(sensor.sensor_type):       
        #print('S',s)
        if s.anomaly is None:
            print('CI SONO')
            anomaly = Anomaly(randint(1, 1000000), s.sensor_id)
            #print(anomaly)
            db.session.add(anomaly)
            db.session.commit()
            print(create_payload(s.winery_id))
            bss.use_data(create_payload(s.winery_id))
    return str(sensor.anomaly)

@app.route("/remove_anomalys", methods=["POST"])
def remove_anomalys():
    winery_id = request.form.get("winery_id")
    winery = wm.get_winery_by_id(winery_id)
    print(winery)
    for sensor in winery.sensors:
        if sensor.anomaly:
            db.session.delete(sensor.anomaly)
            db.session.commit()
    
    print(create_payload(winery_id, rm = -1))
    bss.use_data(create_payload(winery_id, rm = -1))
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
    return str(value.value_id)


