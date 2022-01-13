from flask import Flask
from flask_restful import Resource, Api
from flask import Flask, request, render_template
from config import Config
import googlemaps
from flask_sqlalchemy import SQLAlchemy
import os
from flask_ngrok import run_with_ngrok
import threading
import logging
from bridge_seriale_server import Bridge_Seriale_Server
from bridge_server_seriale import Bridge_Server_Seriale
import time
from anomaly_detection import *

app = Flask(__name__)
myconfig = Config
app.config.from_object(myconfig)
db = SQLAlchemy(app)
gmaps = googlemaps.Client(key=Config.GOOGLEMAPS_APIKEY)
run_with_ngrok(app)


def runApp():
    app.run()

def runBridge():
    br = Bridge_Seriale_Server()
    br.setup()
    br.loop()
    
if __name__ == "__main__":
    from views import *
    from bot_telegram import *
    import time
    
    def startjob():
        while True:
            time.sleep(120)
            Anomaly_Detection(wm).start()
    
    try: 
        t1 = threading.Thread(target=runApp)
        t2 = threading.Thread(target=startBot)
        t3 = threading.Thread(target=runBridge)
        t4 = threading.Thread(target=startjob)
        t1.start()
        t3.start()
        t4.start()
        t2.run()
    except Exception as e:
        print.error("Unexpecte error:"+str(e))

