import requests
from random import randrange, randint


url = "http://127.0.0.1:5000/add/value"
id = randint(1, 2)
print('id', id)
myobj = {"value": randrange(10, 20), "sensor_id": id}
print(myobj)
x = requests.post(url, data=myobj)
print(x)
print(x.text)
