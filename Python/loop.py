import threading
import logging
import sys
import configparser
import mysql.connector

#Import eigene Module
import getradiosondycsv
import time
import hoehen
import Database
import config
import verarbeiten
import getsondehub

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
    print("Datenbanken erstellt")
except:
    print("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))

#TODO eigenen Mosquitto auch abfragen

while True:
    print("loop")
    logging.info("loop")
    if conf['getradiosondycsv'] == "1":
        getradiosondycsv.csv(mydb)
    if conf['gethoehen'] == "1":
        hoehen.hoehe(mydb)
    if conf['getsondehub'] == "1":
        getsondehub.csv(mydb)
    verarbeiten.sonden(mydb)
    Database.löschen(mydb)
    time.sleep(30)

    #TODO Prediction
    #TODO Startort Statistiken