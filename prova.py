from views import wm




for s in wm.get_winery_sensors(3):
    print(s, s.values)
for a in wm.get_all_anomalies():
    print(a.sensor_id, a.anomaly_id)