import mysql.connector
import configparser
import functions
import logging
import sys

from sonden_class import Sonden

sonde = Sonden()

try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen API.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Config lesen API.py:" + str(sys.exc_info()))


def mydbconnect():
    try:
        # Datenbankverbindung herstellen
        global mydb
        global mycursor
        mydb = mysql.connector.connect(
            host=conf['dbpfad'],
            user=conf['dbuser'],
            password=conf['dbpassword'],
            database=conf['dbname'],
            auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
    except:
        print("Unexpected error Datenbankverbindung API.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Datenbankverbindung API.py:" + str(sys.exc_info()))


def sonden():
  #try:
    mydbconnect()
    sondenids = functions.sondenids(mydb, 30)
    mydb.close()
    anzahlids = len(sondenids)
    j = 0
    logging.info("verarbeiten.py")   

    while j <anzahlids:
        sonde.setid(sondenids[j])
        sonde.set_stats()
        buffer = sonde.getgroudhohe()
        if sonde.startort() == "unbekannt":
          sonde.updatestartort()
        j = j + 1
  #except:
        #print("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        #logging.error("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        #return None

