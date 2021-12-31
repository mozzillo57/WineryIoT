import requests

url = 'http://127.0.0.1:5000/add/anomaly'
myobj = {
    'anomaly_id': 0,
    'sensor_id': 1
}
print(myobj)
x = requests.post(url, data = myobj)
print(x)
print(x.text)