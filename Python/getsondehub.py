import mysql.connector
import configparser
import requests
import sys
import logging
import json
import datetime

def csv(mydb):
    try:
        logging.basicConfig(filename='logs/getsondehub.log', level=logging.INFO)
        mycursor = mydb.cursor()
        response = requests.get("https://api.v2.sondehub.org/sondes/telemetry",  timeout=30)
        logging.info(response.url)
        jobs = []
        if response.status_code == 200:
            logging.info('Success!')
            r = response.json()
            
            for i in r.keys():
                print(i)
                logging.info(i)
                s = response.json()[i]
                for j in s.keys():
                    
                    
                    sondenid = j
                    lat = response.json()[i][j]['lat']
                    lon = response.json()[i][j]['lon']
                    alt = response.json()[i][j]['alt']
                    try:
                        geschw = response.json()[i][j]['vel_h']
                    except:
                        geschw = 0.0
                    try:
                        vgeschw = response.json()[i][j]['vel_v']
                    except:
                        vgeschw = 0.0                    
                    try:
                        richtung = response.json()[i][j]['heading']
                    except:
                        richtung = 0.0
                    try:
                        freq = response.json()[i][j]['frequency']
                    except:
                        freq = 0.0
                    sondetime = int(datetime.datetime.strptime(response.json()[i][j]['datetime'],'%Y-%m-%dT%H:%M:%S.%f%z').timestamp())

                    payload="INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime, server) VALUES ('" + i + "', " + str(lat) + ", " + str(lon) + ", " + str(alt) + ", " + str(geschw) + ", " + str(vgeschw) + ", " + str(richtung) + ", " + str(freq) + ", " + str(sondetime) + ", 'Sondehub')"
                    #print(payload)
                    mycursor.execute(payload)        
                    mydb.commit()


            

        elif response.status_code == 404:
            print('Not Found.')
    except:
        print("Unexpected error getsondehub.py:" + str(sys.exc_info()))
        logging.error("Unexpected error getsondehub.py:" + str(sys.exc_info()))
        return None