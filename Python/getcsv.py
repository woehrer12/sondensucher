import csv 
import requests
import mysql.connector
import configparser
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/getcsv.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info("Skript gestartet")

#Config Datei auslesen
config = configparser.ConfigParser()
config.read('dbconfig.ini')
conf = config['DEFAULT']

#Datenbankverbindung herstellen
try:
    mydb = mysql.connector.connect(
        host=conf['dbpfad'],
        user=conf['dbuser'],
        password=conf['dbpassword'],
        database=conf['dbname'],
        auth_plugin='mysql_native_password'
        )
    mycursor = mydb.cursor()
except:
    print("Unexpected error:" + str(sys.exc_info()[0]))

#Header fälschen
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

url = "https://radiosondy.info/export/csv_live.php"

#sondenid; lat; lon; hoehe; geschw; vgeschw; richtung; freq; sondetime

def csv():
    try:
        httpx = requests.get(url, headers=headers)

        antwort = httpx.text

        #print(antwort)

        for line in antwort.split('\n'):
            #print(line)
            sonde = []
            if len(line) != 0:
                for line in line.split(';'):
                    if len(line) == 0:
                        line = "0"
                    sonde.append(line)
                #Leere Lines nicht eintragen
                #print(sonde)
                #Datenbank eintragen
                payload="INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime, server) VALUES ('" + sonde[0] + "', " + sonde [1] + ", " + sonde[2] + ", " + sonde [3] + ", " + sonde[4] + ", " + sonde [5] + ", " + sonde[6] + ", " + sonde [7] + ", " + sonde[8] + ", 'radiosondy')"
                #print(payload)
                mycursor.execute(payload)        
                mydb.commit()
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        logger.error("Unexpected error:" + str(sys.exc_info()[0]))


csv()