import requests

url = 'http://127.0.0.1:5000/add/sensor'
myobj = {
    'sensor_id': 1,
    'sensor_type': 'T',
    'winery_id': 1
}
print(myobj)
x = requests.post(url, data = myobj)
print(x)
print(x.text)

myobj2 = {
    'sensor_id': 2,
    'sensor_type': 'D',
    'winery_id': 1
}
print(myobj2)
x2 = requests.post(url, data = myobj2)
print(x2)
print(x2.text)