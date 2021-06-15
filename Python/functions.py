import mysql.connector
import configparser
import logging
import sys

Sondeframjson = {
    "sondenid" : "",
    "lat" : 0.0,
    "lon" : 0.0,
    "hoehe" : 0,
    "vgeschw" : 0.0,
    "freq" : "",
    "richtung" : 0.0,
    "geschw" : 0.0,
    "sondentime" : "",
    "server" : "",
    "groundhoehe" : 0,
}


def initlogger(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def initconfig():
    #Konfigdatei initialisieren
    try:
        #Config Datei auslesen
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        conf = config['DEFAULT']
        return conf
    except:
        print("Unexpected error Config lesen functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Config lesen functions.py:" + str(sys.exc_info()))

def configDatabase():
        #Konfigdatei initialisieren
    try:
        #Config Datei auslesen
        config = configparser.ConfigParser()
        config.read('config/Database.ini')
        Databaseconf = config['DEFAULT']
        return Databaseconf
    except:
        print("Unexpected error Database.ini Config lesen functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Database.ini Config lesen functions.py:" + str(sys.exc_info()))

def getDataBaseConnection():
    #Datenbank initialisieren
    conf = initconfig()
    try:
        #Datenbankverbindung herstellen
        mydb = mysql.connector.connect(
            host=conf['dbpfad'],
            user=conf['dbuser'],
            password=conf['dbpassword'],
            database=conf['dbname'],
            auth_plugin='mysql_native_password'
            )
        return(mydb)
    except:
        print("Unexpected error Datenbankverbindung functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Datenbankverbindung functions.py:" + str(sys.exc_info()))

def insertSonde(Sondeframjson):
    try:
        #TODO Auch als Liste übergebbar machen, um nicht die Datenbank für jede Sonde zu öffnen und zu schließen
        mydb = getDataBaseConnection()
        mycursor = mydb.cursor()
        payload="INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime, server) VALUES (" + \
            "'" + Sondeframjson['sondenid'] + "', " + \
            Sondeframjson['lat'] + ", " + \
            Sondeframjson['lon'] + ", " + \
            Sondeframjson['hoehe'] + ", " + \
            Sondeframjson['geschw'] + ", " + \
            Sondeframjson['vgeschw'] + ", " + \
            Sondeframjson['richtung'] + ", " + \
            Sondeframjson['freq'] + ", " + \
            Sondeframjson['sondetime'] + ", " + \
            "'" + Sondeframjson['server'] + "' " + \
                ")"
        mycursor.execute(payload)   
        mydb.commit()
        mydb.close()
    except:
        print("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))

