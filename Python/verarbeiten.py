import mysql.connector
import configparser
import functions
import logging
import sys

from sonden_class import Sonden
sonde = Sonden()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/verarbeiten.log")
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
    print("Unexpected error Config lesen verarbeiten.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Config lesen verarbeiten.py:" + str(sys.exc_info()))

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
    print("Unexpected error Datenbankverbindung verarbeiten.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Datenbankverbindung verarbeiten.py:" + str(sys.exc_info()))

def sonden():
  try:
    sondenids = functions.sondenids()
    anzahlids = len(sondenids)
    j = 0


    

    while j <anzahlids:
        sonde.setid(sondenids[j])
        print(sonde.getgroudhohe())
        print(type(sonde.getgroudhohe()))
        j = j + 1
  except:
        print("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        logger.error("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        return None


sonden()