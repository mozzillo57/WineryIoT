from schema import Winery, Sensor, Anomaly, Value


class WineryManager:
    def __init__(self, db):
        self.db = db

    def get_winery_by_id(self, winery_id):
        return Winery.query.filter_by(winery_id=winery_id).first()

    def get_senor_by_id(self, sensor_id):
        return Sensor.query.filter_by(sensor_id=sensor_id).first()
    
    def get_anomaly_by_id(self, anomaly_id):
        return Anomaly.query.filter_by(anomaly_id=anomaly_id).first()

    def get_winery_sensors(self, winery_id):
        winery = Winery.query.filter_by(winery_id=winery_id).first()
        sensors = winery.sensors
        return sensors

    def get_winery_sensors_by_type(self, winery_id, sensor_type):
        winery = Winery.query.filter_by(winery_id=winery_id).first()
        sensors = winery.sensors
        s = []
        for sensor in sensors:
            if sensor.sensor_type == sensor_type:
                s.append(sensor)
        return s

    def get_anomaly_by_id(self, anomaly_id):
        return Anomaly.query.filter_by(anomaly_id=anomaly_id).first()

    def get_anomaly_by_sensor_id(self, sensor_id):
        return Anomaly.query.filter_by(sensor_id=sensor_id).first()

    def get_all_winerys(self):
        return Winery.query.all()

    def get_all_sensors(self):
        return Sensor.query.all()

    def get_all_anomalies(self):
        return Anomaly.query.all()

    def get_all_sensors_by_type(self, sensor_type):
        return Sensor.query.filter_by(sensor_type=sensor_type).all()

    def get_winerys_by_location(self, lat, lon):
        return Winery.query.filter_by(winery_lat=lat, winery_long=lon).all()

    def get_all_values_by_sensor(self, sensor_id):
        return Value.query.filter_by(sensor_id = sensor_id).all()
    
    def get_all_values_by_sensor_and_timestamp(self, sensor_id, timestamp):
        return Value.query.filter_by(value_id = timestamp, sensor_id = sensor_id).all()
    
    def get_all_sensors_with_anomaly(self, winery_id):
        winery = Winery.query.filter_by(winery_id=winery_id).first()
        sensors = winery.sensors
        sen_anomaly = []
        for s in sensors:
            if s.anomaly:
                sen_anomaly.append(s.sensor_id)
        return sen_anomaly
    
        