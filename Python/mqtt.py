# python3.6
#https://www.emqx.io/blog/how-to-use-mqtt-in-python
import mysql.connector
import configparser
import json
import logging
import sys
import time
import random

from paho.mqtt import client as mqtt_client

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/mqtt.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

#Konfigdatei initialisieren
try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen mqtt.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Config lesen mqtt.py:" + str(sys.exc_info()))


#Datenbank initialisieren
try:
    #Datenbankverbindung herstellen
    mydb = mysql.connector.connect(
        host=conf['dbpfad'],
        user=conf['dbuser'],
        password=conf['dbpassword'],
        database=conf['dbname'],
        auth_plugin='mysql_native_password'
        )
    mycursor = mydb.cursor() 
except:
    print("Unexpected error Datenbankverbindung mqtt.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Datenbankverbindung mqtt.py:" + str(sys.exc_info()))

broker = 'sondensucher.de'
port = 1883
topic = "packet"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'sondensucher'
password = 'sondensucher'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            pass
            print("Connected to MQTT Broker!")

        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = json.loads(msg.payload.decode())
        payload="INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime, server) VALUES \
        ('" + message["id"] + "', " + str(message["lat"]) + ", " + str(message["lon"]) + ", " + str(message["alt"]) + ", " + str(message["hs"]) + ", " + str(message["vs"]) + ", \
            " + str(message["dir"]) + ", " + str(message["freq"]) + ", " + str(message["time"]) + ", '" + message["ser"] + "')"
        logging.info(message)
        mycursor.execute(payload)        
        mydb.commit()
    client.subscribe(topic)
    client.on_message = on_message

def run():
    logging.info("Config auslesen MQTT")
    if conf['mqtt-sondensucher.de'] == "1":
        logging.info("MQTT abfrage läuft")
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    else:
        logging.info("MQTT abgeschaltet")


if __name__ == '__main__':
    while True:
        try:
            run()
        except:
            print("Unexpected error mqtt.py:" + str(sys.exc_info()))
            logger.error("Unexpected error mqtt.py:" + str(sys.exc_info()))
            time.sleep(60)

#run()