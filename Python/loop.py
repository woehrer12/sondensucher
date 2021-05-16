import threading
import logging
import sys
import configparser
import mysql.connector
import time

#Import eigene Module
import getradiosondycsv
import hoehen
import Database
import config
import verarbeiten
import getsondehub
import startort_stats
import prediction
import wind

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/loop.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


#Konfigdatei erstellen
config.config()

#Konfigdatei initialisieren
try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen loop.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Config lesen loop.py:" + str(sys.exc_info()))


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
    print("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))

#Datenbanken anlegen
try:
    Database.sonden(mydb)
    Database.hoehen(mydb)
    Database.statistiken(mydb)
    Database.startorte(mydb)
    Database.startort_stats(mydb)
    Database.prediction(mydb)
    print("Datenbanken erstellt")
except:
    print("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))

#TODO eigenen Mosquitto auch abfragen

starttime = int(time.time())
halbmintime = 0
mintime = 0
fuenfmintime = 0
print(starttime)

while True:
    print("loop")
    logging.info("loop")
    #Ausführung bei halber Minute
    if halbmintime < int(time.time()):
        if conf['getradiosondycsv'] == "1":
            getradiosondycsv.csv(mydb)
        verarbeiten.sonden(mydb)
        startort_stats.stats(mydb)
        logging.info("Halbe Minute")
        halbmintime = int(time.time()) + 30

    #Ausführung jede Minute
    if mintime < int(time.time()):
        prediction.predict(mydb)
        Database.löschen(mydb)
        mintime = int(time.time()) + 60
        logging.info("Ganze Minute")


    #Ausführung 5 Minuten
    if fuenfmintime < int(time.time()):
        if conf['gethoehen'] == "1":
            hoehen.hoehe(mydb)
        if conf['getsondehub'] == "1":
            getsondehub.csv(mydb)
        fuenfmintime = int(time.time()) + 300
        logging.info("5 Minuten")

    if conf['wind'] == "1":
        wind.wind_xml(mydb)

    time.sleep(30)
