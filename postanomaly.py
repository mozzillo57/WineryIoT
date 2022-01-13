import requests
from config import Config
url = Config.BASE_URL+'/add/anomaly'
for i in range(1, 5):
    myobj = {
        'anomaly_id': i,
        'sensor_id': i
    }
    print(myobj)
    x = requests.post(url, data = myobj)
    print(x)
    print(x.text)