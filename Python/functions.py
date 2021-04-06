import mysql.connector
import configparser
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/functions.log")
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
    print("Unexpected error Config lesen functions.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Config lesen functions.py:" + str(sys.exc_info()))

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
    print("Unexpected error Datenbankverbindung functions.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Datenbankverbindung functions.py:" + str(sys.exc_info()))


def sondenids():
    try:
        mycursor = mydb.cursor() 
        mycursor.execute("SELECT sondenid FROM sonden WHERE date>(NOW() - INTERVAL 30 MINUTE) AND lat!='0' AND sondenid<>'' GROUP BY sondenid")
        sondenids = mycursor.fetchall()
        i = 0
        anzahl = len(sondenids)
        list = []
        while i < anzahl:
            string = str(sondenids[i])
            stringlänge = len(string)
            #print(stringlänge)
            list.append(string[2:stringlänge-3]) 
            i += 1

        return list
    except:
        print("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))
        logger.error("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))    

    
