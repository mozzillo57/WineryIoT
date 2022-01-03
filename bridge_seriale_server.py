from requests.models import HTTPError
import serial
import numpy as np
from serial.serialutil import PortNotOpenError
from requests import post
from requests.exceptions import ConnectionError


class Bridge_Seriale_Server():
    def setup(self):
        self.portname = '/dev/ttyACM0'
        self.ser = serial.Serial(self.portname, 9600, timeout=0)
        self.sensors = ["T", "H", "D", "B"]

        self.inbuffer = []
        self.listOFValues = np.array([], dtype=np.int32)

        self.winerys = {
            'w0': {
                'winery_id': 0,
                'winery_location': 'Bologna'
            },
            'w1': {
                'winery_id': 1,
                'winery_location': 'Reggio E.'
            },
            'w2': {
                'winery_id': 2,
                'winery_location': 'Modena'
            }
        }
        for w, myobj in self.winerys.items():
            print(w, myobj)
            try:
                r = post("http://127.0.0.1:5000/add/winery", data=myobj)
                print(r.status_code)
            except ConnectionError as e:
                print("No connection with server")

    def loop(self):
        while(True):
            if self.ser.in_waiting > 0:
                last_char = self.ser.read(1)

                if last_char == b'\xfe':
                    #print("\nValue Received")
                    self.useData()
                    self.inbuffer = []
                else:
                    self.inbuffer.append(last_char)

    def useData(self):

        # vedere bene inbuffer se qualcosa non funzionerà ho cambiato da 3 a 4
        if len(self.inbuffer) <= 4 or self.inbuffer[0] != b'\xff':
            return False

        info = [int.from_bytes(self.inbuffer[i], byteorder='little')
                for i in range(1, 5)]
        info[2] = chr(info[2])

        str_val = "Winery_id: %d -> %d Sensor %s: %d" % (
            info[0], info[1], info[2], info[3])
        print(str_val)
        print(info)
        try:
            myobj = {
                'sensor_id': info[1],
                'sensor_type': info[2],
                'winery_id': info[0]
            }
            r = post("http://127.0.0.1:5000/add/sensor", data=myobj)
            # postare le winerys
            print(r.status_code)
        except ConnectionError as e:
            print("No connection with server")
        try:
            myobj = {
                'value': info[3],
                'sensor_id': info[1]
            }
            r = post("http://127.0.0.1:5000/add/value", data=myobj)
            # postare le winerys
            print(r.status_code)
        except ConnectionError as e:
            print("No connection with server")

if __name__ == '__main__':
    br = Bridge_Seriale_Server()
    br.setup()
    br.loop()
