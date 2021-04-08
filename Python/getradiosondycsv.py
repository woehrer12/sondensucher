import csv 
import requests
import mysql.connector
import configparser
import logging
import sys

#Header fälschen
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

url = "https://radiosondy.info/export/csv_live.php"

#sondenid; lat; lon; hoehe; geschw; vgeschw; richtung; freq; sondetime

def csv(mydb):
    try:
        logging.basicConfig(filename='logs/getradiosondycsv.log', level=logging.INFO)

        mycursor = mydb.cursor()

        httpx = requests.get(url, headers=headers)

        antwort = httpx.text

        #print(antwort)
        
        logging.info("Radiosondy CSV abgerufen")

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
        print("Unexpected error csv.py:" + str(sys.exc_info()))
        logging.error("Unexpected error getradiosondycsv.py:" + str(sys.exc_info()))
