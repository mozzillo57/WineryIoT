import requests
from random import randint, randrange
from config import Config
from views import *

winery = wm.get_winery_by_id(3)
for s in winery.sensors:
    for v in s.values:
        db.session.delete(v)
        db.session.commit()
    db.session.delete(s)
    db.session.commit()

""" base = Config.BASE_URL

#POST WINERY
url = base+'/add/sensor'
types = ['T', 'D', 'H', 'B']
for i in range(1, 5):
    myobj = {
        'sensor_id': i+100,
        'sensor_type': types[(i-1)],
        'winery_id': 3
    }
    
    print(myobj)
    x = requests.post(url, data = myobj)
    print(x)
    print(x.text)

# POST VALUE
url = base+"/add/value"
for i in range(1, 100):
    id = randint(1, 4)
    print('id', id)
    myobj = {"value": randrange(10, 20), "sensor_id": id+100}
    print(myobj)
    x = requests.post(url, data=myobj)
    print(x)
    print(x.text) """