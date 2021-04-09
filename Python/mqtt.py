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


def subscribe(client: mqtt_client,mydb):
    mycursor = mydb.cursor()
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

def run(mydb):
    client = connect_mqtt()
    subscribe(client,mydb)
    client.loop_forever()


# if __name__ == '__main__':
#     while True:
#         try:
#             run()
#         except:
#             print("Unexpected error mqtt.py:" + str(sys.exc_info()))
#             logger.error("Unexpected error mqtt.py:" + str(sys.exc_info()))
#             time.sleep(60)

#run()