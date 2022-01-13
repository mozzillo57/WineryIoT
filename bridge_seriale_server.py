from requests.models import HTTPError
import serial
import numpy as np
from serial.serialutil import PortNotOpenError
from requests import post
from config import Config
from requests.exceptions import ConnectionError
from random import randrange


def post_sensor(sensor_id, sensor_type, winery_id):
    sensor = {
        "sensor_id": sensor_id,
        "sensor_type": sensor_type,
        "winery_id": winery_id,
    }
    try:
        r = post(Config.BASE_URL + "/add/sensor", data=sensor)
    except ConnectionError as e:
        print("No connection with server")


def post_winery(winery_id, winery_lat, winery_long):
    win = {
        "winery_id": winery_id,
        "winery_lat": winery_lat,
        "winery_long": winery_long,
    }
    try:
        r = post(Config.BASE_URL + "/add/winery", data=win)
    except ConnectionError as e:
        print("No connection with server")


def post_value(value, sensor_id):
    value = {"value": value, "sensor_id": sensor_id}
    try:
        r = post(Config.BASE_URL + "/add/value", data=value)
    except ConnectionError as e:
        print("No connection with server")


def generate_winery_2(sensor_id, sensor_type, sensor_value):
    post_sensor(sensor_id + 10, sensor_type, 2)
    post_value(sensor_value + randrange(-1, 1), sensor_id + 10)


class Bridge_Seriale_Server:
    def setup(self):
        self.portname = "/dev/ttyACM0"
        self.ser = serial.Serial(self.portname, 9600, timeout=0)
        self.sensors = ["T", "H", "D", "B"]

        self.inbuffer = []
        self.listOFValues = np.array([], dtype=np.int32)


    def loop(self):
        while True:
            if self.ser.in_waiting > 0:
                last_char = self.ser.read(1)

                if last_char == b"\xfe":
                    # print("\nValue Received")
                    self.useData()
                    self.inbuffer = []
                else:
                    self.inbuffer.append(last_char)

    def useData(self):
        post_winery(3, 44.50342955149953, 11.086431198448272)       
        post_winery(1, 44.52820, 10.92102)
        post_winery(2, 44.50462842959038, 10.923375979946016)
        if len(self.inbuffer) <= 4 or self.inbuffer[0] != b"\xff":
            return False

        info = [
            int.from_bytes(self.inbuffer[i], byteorder="little") for i in range(1, 5)
        ]

        winery_id = info[0]
        sensor_id = info[1]
        sensor_type = chr(info[2])
        sensor_value = info[3]

        str_val = "Winery_id: %d -> %d Sensor %s: %d" % (
            winery_id,
            sensor_id,
            sensor_type,
            sensor_value,
        )
        print(str_val)
        if sensor_type in self.sensors:
            # w1
            post_sensor(sensor_id, sensor_type, winery_id)
            post_value(sensor_value, sensor_id)
            # w2
            generate_winery_2(sensor_id, sensor_type, sensor_value)
        else:
            print("Sensor not supported")


if __name__ == "__main__":
    br = Bridge_Seriale_Server()
    br.setup()
    br.loop()
