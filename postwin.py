import requests
from random import randint, randrange

#POST WINERY
url = 'http://127.0.0.1:5000/add/winery'
myobj = {
    'winery_id': 1,
    'winery_lat': 44.52820,
    'winery_long': 10.92102
}
print(myobj)
x = requests.post(url, data=myobj)
print(x)
print(x.text)

myobj2 = {
    'winery_id': 2,
    'winery_lat': 44.50462842959038,
    'winery_long': 10.923375979946016
}
print(myobj2)
x2 = requests.post(url, data=myobj2)
print(x2)
print(x2.text)

myobj3 = {
    'winery_id': 3,
    'winery_lat': 44.50342955149953,
    'winery_long': 11.086431198448272
}
print(myobj3)
x3 = requests.post(url, data=myobj3)
print(x3)
print(x3.text)

# POST SENSORS
url = 'http://127.0.0.1:5000/add/sensor'
types = ['T', 'D', 'H', 'B']
for i in range(1, 5):
    myobj = {
        'sensor_id': i,
        'sensor_type': types[(i-1)],
        'winery_id': 1
    }
    print(myobj)
    x = requests.post(url, data = myobj)
    print(x)
    print(x.text)


# POST VALUE
url = "http://127.0.0.1:5000/add/value"
for i in range(1, 100):
    id = randint(1, 4)
    print('id', id)
    myobj = {"value": randrange(10, 20), "sensor_id": id}
    print(myobj)
    x = requests.post(url, data=myobj)
    print(x)
    print(x.text)



