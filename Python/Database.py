import mysql.connector
import configparser
import os
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/Database.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen API.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Config lesen API.py:" + str(sys.exc_info()))

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
    print("Unexpected error Datenbankverbindung Database.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Datenbankverbindung Database.py:" + str(sys.exc_info()))



def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


def sonden():
    try:
        #Datenbank sonden anlegen
        if checkTableExists(mydb,"sonden"):
            print("Datenbank Sonden Existiert")
        else:
            print("Datenbank Sonden Existiert nicht")
            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE sonden(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `sondenid` text NOT NULL, \
                `lat` double NOT NULL, \
                `lon` double NOT NULL, \
                `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                `hoehe` int NOT NULL, \
                `server` text NOT NULL, \
                `vgeschw` double NOT NULL, \
                `temp` double DEFAULT '0.0' NOT NULL, \
                `freq` text NOT NULL, \
                `richtung` double NOT NULL, \
                `geschw` double NOT NULL, \
                `rssi` double DEFAULT '0.0' NOT NULL, \
                `sondetime` text NOT NULL, \
                `latsucher` double DEFAULT '0.0' NOT NULL, \
                `lonsucher` double DEFAULT '0.0' NOT NULL, \
                `altsucher` double DEFAULT '0.0' NOT NULL, \
                `dirsucher` double DEFAULT '0.0' NOT NULL, \
                PRIMARY KEY (id) \
                )")
            print("Datenbank Sonden wurde erstellt")
    except:
        print("Unexpected error Datenbank Sonden anlegen Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error Datenbank Sonden anlegen Database.py:" + str(sys.exc_info()))

def Hoehen():
    try:
        #Datenbank Höhen anlegen
        if checkTableExists(mydb,"hoehen"):
            print("Datenbank Höhen Existiert")
        else:
            print("Datenbank Höhen Existiert nicht")
            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE hoehen(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `lat` double NOT NULL, \
                `lon` double NOT NULL, \
                `hoehe` double NOT NULL, \
                `quelle` text NOT NULL, \
                PRIMARY KEY (id) \
                )")
            print("Datenbank Höhen wurde erstellt")
    except:
        print("Unexpected error Datenbank Höhen anlegen Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error Datenbank Höhen anlegen Database.py:" + str(sys.exc_info()))

def Statistiken():
    try:
        #Datenbank sonden anlegen
        if checkTableExists(mydb,"sonden_stats"):
            print("Datenbank Sonden Statistiken Existiert")
        else:
            print("Datenbank Sonden Statistiken Existiert nicht")
            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE sonden_stats(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `sondenid` text NOT NULL, \
                `startort` text NOT NULL, \
                `max_hoehe` int(11) NOT NULL, \
                `vgeschposD` text NOT NULL, \
                `vgeschnegD` text NOT NULL, \
                `burst` tinyint(1) DEFAULT '0' NOT NULL, \
                `latburst` double DEFAULT '0.0' NOT NULL, \
                `lonburst` double DEFAULT '0.0' NOT NULL, \
                PRIMARY KEY (id) \
                )")
            print("Datenbank Sonden Statistiken wurde erstellt")
    except:
        print("Unexpected error Datenbank Statistiken anlegen Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error Datenbank Statistiken anlegen Database.py:" + str(sys.exc_info()))

    #TODO doppelte finden

sonden()
Hoehen()
Statistiken()