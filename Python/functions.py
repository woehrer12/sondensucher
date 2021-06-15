import mysql.connector
import configparser
import logging
import sys
import time

sondeFrameJson = {
    'sondenid' : "",
    'lat' : 0.0,
    'lon' : 0.0,
    'hoehe' : 0,
    'vgeschw' : 0.0,
    'freq' : "",
    'richtung' : 0.0,
    'geschw' : 0.0,
    'sondentime' : "",
    'server' : "",
    'groundhoehe' : 0,
}
sondeJson = {
    'sondenid' : "",
    'lat' : 0.0,
    'lon' : 0.0,
    'hoehe' : 0,
    'vgeschw' : 0.0,
    'freq' : "",
    'richtung' : 0.0,
    'geschw' : 0.0,
    'sondentime' : "",
    'server' : "",
    'groundhoehe' : 0,
    'vgeschposD' : 0.0,
    'vgeschnegD' : 0.0,
    'maxhoehe' : 0,
    'startort' : "",
    'latpredict' : 0.0,
    'lonpredict' : 0.0,
    'timepredict' : "",
}
apiStatsJson = {
    'sonden' : 0,
    'hoehen' : 0,
    'sonden_stats' : 0,
    'startorte' :0,
    'startorte_stats' : 0
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

def insertSonde(sondeFrameJson):
    try:
        #TODO Auch als Liste übergebbar machen, um nicht die Datenbank für jede Sonde zu öffnen und zu schließen
        mydb = getDataBaseConnection()
        mycursor = mydb.cursor()
        payload="INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime, server) VALUES (" + \
            "'" + sondeFrameJson['sondenid'] + "', " + \
            sondeFrameJson['lat'] + ", " + \
            sondeFrameJson['lon'] + ", " + \
            sondeFrameJson['hoehe'] + ", " + \
            sondeFrameJson['geschw'] + ", " + \
            sondeFrameJson['vgeschw'] + ", " + \
            sondeFrameJson['richtung'] + ", " + \
            sondeFrameJson['freq'] + ", " + \
            sondeFrameJson['sondetime'] + ", " + \
            "'" + sondeFrameJson['server'] + "' " + \
                ")"
        mycursor.execute(payload)   
        mydb.commit()
        mycursor.close()
        mydb.close()
    except:
        print("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Datenbankverbindung loop.py:" + str(sys.exc_info()))

def APIStats():
    try:
        #TODO testen
        mydb = getDataBaseConnection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(id) FROM `sonden`")
        apiStatsJson['sonden'] = mycursor.fetchone()
        mycursor.execute("SELECT COUNT(id) FROM `hoehen`")
        apiStatsJson['hoehen'] = mycursor.fetchone()
        mycursor.execute("SELECT COUNT(id) FROM `sonden_stats`")
        apiStatsJson['sonden_stats'] = mycursor.fetchone()
        mycursor.execute("SELECT COUNT(id) FROM `startorte`")
        apiStatsJson['startorte'] = mycursor.fetchone()
        mycursor.execute("SELECT COUNT(id) FROM `startort_stats`")
        apiStatsJson['startorte_stats'] = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return apiStatsJson
    except:
        print("Unexpected error APIStats functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error APIStats functions.py:" + str(sys.exc_info()))    


def sondenids(minuten):
    try:
        mydb = getDataBaseConnection()
        sekunden = minuten * 60
        mycursor = mydb.cursor() 
        now = int(time.time())
        payload = "SELECT sondenid FROM sonden WHERE sondetime>(" + str(now) + " - " + str(sekunden) + ") AND lat!='0' AND sondenid<>'' GROUP BY sondenid"
        mycursor.execute(payload)
        sondenids = mycursor.fetchall()
        i = 0
        list = []
        #TODO testen
        for ids in sondenids:
            string = str(sondenids[i])
            stringlänge = len(string)
            #print(stringlänge)
            list.append(string[2:stringlänge-3])
        mycursor.close()
        mydb.close()
        return list
    except:
        print("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))    

def getSonde(sondenid):
    try:
        #TODO testen
        #TODO Abfrage mit Liste
        mydb = getDataBaseConnection()
        mycursor = mydb.cursor() 
        #TODO Alle Abfragen für das sondeJson
        mycursor.close()
        mydb.close()
        return sondeJson


    except:
        print("Unexpected error getSonde() functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error getSonde() functions.py:" + str(sys.exc_info()))    
