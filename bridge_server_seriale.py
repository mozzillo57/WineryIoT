import serial
import json
from binascii import unhexlify

class Bridge_Server_Seriale():

    def setupSerial(self):
        # open serial port
        self.portname = '/dev/ttyACM0' 
        self.ser = serial.Serial(self.portname, 9600, timeout=0)

        # internal input buffer from serial
        self.inbuffer = '/dev/ttyACM0'

    def use_data(self, payload):        
        msg_to_ser = "dd"
        msg_to_ser += "0" + str(payload["winery_id"])
        if payload["sensor"] == -1:
            msg_to_ser += "db"
        elif payload["sensor"] != "all":
            msg_to_ser += "0" + str(len(payload["sensor"]))
            for s in payload["sensor"]:
                msg_to_ser += "0"
                msg_to_ser += str(s)
        else:
            msg_to_ser += "dc"

        msg_to_ser += "de"
        self.ser.write(unhexlify(msg_to_ser))

    def setup(self):
        self.setupSerial()


if __name__ == '__main__':
    br=Bridge_Server_Seriale()
    br.setup()