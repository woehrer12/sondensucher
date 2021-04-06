import threading
import logging
import sys
import configparser

#Import eigene Module
import getcsv
import time
import hoehen
import Database
import config
import API
import mqtt



#Konfigdatei erstellen
config.config()
print("Config Datei erstellt")

#Konfigdatei initialisieren
try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen API.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Config lesen API.py:" + str(sys.exc_info()))



#Datenbanken anlegen
Database.sonden()
Database.hoehen()
Database.statistiken()
print("Datenbanken erstellt")

#API starten
#t1 = API.app.run()
#t1 = start()

#MQTT starten
#t2 = mqtt.run()
#t2 = start()


while True:
    getcsv.csv()
    hoehen.hoehe()
    print("loop")
    time.sleep(30)