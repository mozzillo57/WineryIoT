import requests

url = 'http://127.0.0.1:5000/add/anomaly'
for i in range(1, 3):
    myobj = {
        'anomaly_id': i,
        'sensor_id': i
    }
    print(myobj)
    x = requests.post(url, data = myobj)
    print(x)
    print(x.text)