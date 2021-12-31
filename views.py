from schema import Winery, Sensor, Anomaly
from flask import render_template, request
from flask_template import app, db
from winerys import WineryManager

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
    return render_template("winery.html", winery_id=winery_id, winery = winery, sensors = sensors)


@app.route("/add/winery", methods=["POST"])
def add_winery():
    winery_id = request.form.get("winery_id", None)
    winery_location = request.form.get("winery_location", None)
    winery = Winery(winery_id, winery_location)
    print(winery)
    db.session.add(winery)
    db.session.commit()
    return str(winery.winery_id)


@app.route("/add/sensor", methods=["POST"])
def add_sensor():
    print(type(request.get_data()))
    sensor_id = request.form.get("sensor_id")
    sensor_type = request.form.get("sensor_type")
    sensor_value = float(request.form.get("sensor_value"))
    winery_id = request.form.get("winery_id")
    winery = Winery.query.filter_by(winery_id=winery_id).first()
    sensor = Sensor(sensor_id, sensor_type, sensor_value, winery_id)
    winery.sensors.append(sensor)
    print(sensor_id, sensor_value, winery_id)
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