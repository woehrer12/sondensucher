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
        mydb = getDataBaseConnection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(id) FROM `sonden`")
        apiStatsJson['sonden'] = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(id) FROM `hoehen`")
        apiStatsJson['hoehen'] = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(id) FROM `sonden_stats`")
        apiStatsJson['sonden_stats'] = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(id) FROM `startorte`")
        apiStatsJson['startorte'] = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(id) FROM `startort_stats`")
        apiStatsJson['startorte_stats'] = mycursor.fetchone()[0]
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
        list = []
        for ids in sondenids:
            list.append(ids[0])
        mycursor.close()
        mydb.close()
        return list
    except:
        print("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))    

def getSonde(sondenid):
    try:
        #TODO Abfrage mit Liste
        mydb = getDataBaseConnection()
        mycursor = mydb.cursor() 
        query = "SELECT sondenid, lat, lon, hoehe, server, vgeschw, freq, richtung, geschw, sondetime FROM sonden WHERE sondenid = '" + sondenid + "' ORDER BY `sonden`.`sondetime` DESC LIMIT 1"
        mycursor.execute(query)
        data = mycursor.fetchall()
        sondendaten = data[0]
        mycursor.close()
        mydb.close()


        sondeJson['sondenid'] = sondendaten[0]
        sondeJson['lat'] = sondendaten[1]
        sondeJson['lon'] = sondendaten[2]
        sondeJson['hoehe'] = sondendaten[3]
        sondeJson['vgeschw'] = sondendaten[4]
        sondeJson['freq'] = sondendaten[5]
        sondeJson['richtung'] = sondendaten[6]
        sondeJson['geschw'] = sondendaten[7]
        sondeJson['sondetime'] = sondendaten[8]
        sondeJson['server'] = sondendaten[9]
        #TODO restliche Daten auffüllen
        sondeJson['groundhoehe'] = 0
        sondeJson['vgeschposD'] = 0
        sondeJson['vgeschnegD'] = 0
        sondeJson['maxhoehe'] = 0 
        sondeJson['startort'] = 0
        sondeJson['latpredict'] = 0
        sondeJson['lonpredict'] = 0
        return sondeJson


    except:
        print("Unexpected error getSonde() functions.py:" + str(sys.exc_info()))
        logging.error("Unexpected error getSonde() functions.py:" + str(sys.exc_info()))
        return False


if __name__ == '__main__':
    #TODO only for Test
    print(getSonde('D170475'))