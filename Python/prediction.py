# -*- coding: utf-8 -*-

#from mpl_toolkits.mplot3d import Axes3D
import mysql.connector
import time
import requests
import functions
import datetime
from sonden_class import Sonden
import logging
import sys
sonde = Sonden()


def predict(mydb):
    try:
        mycursor = mydb.cursor() 
        sondenids = functions.sondenids(mydb,30)
        anzahlids = len(sondenids)

        #Datenbank leeren
        mycursor.execute("TRUNCATE `prediction`")
        mydb.commit()
        i = 0
        while i <anzahlids:
            sonde.setid(sondenids[i])
            d = datetime.datetime.utcnow()
            t = d.isoformat("T") + "Z"
            startort = sonde.getstartort()
            query = "SELECT vgeschposD, vgeschnegD, maxhoeheD FROM `startort_stats` WHERE startort = '" + startort + "'"
            mycursor.execute(query)
            daten = mycursor.fetchall()

            if daten != []:
                daten = daten[0]
                vgeschposD = daten[0]
                vgeschnegD = abs(daten[1])
                burst_altitude =  daten[2]


                if sonde.isburst():
                    payload = "launch_latitude=" + str(sonde.getlat())+ "&launch_longitude=" + str(sonde.getlon()) + "&launch_altitude=" + str(sonde.gethoehe()) + "&launch_datetime=" + t + "&ascent_rate=" + str(vgeschposD) + "&burst_altitude=" + str(float(sonde.gethoehe())+1) + "&descent_rate=" + str(vgeschnegD)
                else:
                    payload = "launch_latitude=" + str(sonde.getlat()) + "&launch_longitude=" + str(sonde.getlon()) + "&launch_altitude=" + str(sonde.gethoehe()) + "&launch_datetime=" + t + "&ascent_rate=" + str(vgeschposD) + "&burst_altitude=" + str(burst_altitude) + "&descent_rate=" + str(vgeschnegD)

                response = requests.get("http://predict.cusf.co.uk/api/v1/?" + payload,  timeout=30)
                #print(response.text)
                logging.info(response)
                if response.status_code == 200:

                    j = 0
                    #steigende Daten
                    k = len(response.json()['prediction'][0]['trajectory'])
                    #print("Länge: " + str(k))
                    while j < k:
                        lat = response.json()['prediction'][0]['trajectory'][j]['latitude']
                        #print("Lat", lat)
                    
                        lng = response.json()['prediction'][0]['trajectory'][j]['longitude']
                        #print("Lon", lng)  
                    
                        altitude = response.json()['prediction'][0]['trajectory'][j]['altitude']
                        #print("Höhe", altitude)

                        time = response.json()['prediction'][0]['trajectory'][j]['datetime']
                        time = int(datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%S.%f%z').timestamp())

                        quelle = "predict.cusf.co.uk"

                        mycursor.execute("INSERT INTO prediction (sondenid, lat, lon, hoehe, time, quelle) VALUES (%s,%s,%s,%s,%s,%s)",(sondenids[i],lat,lng,altitude,time,quelle,))        
                        mydb.commit()

                        j = j + 1
                        #print(j)

                    #fallende Daten
                    j = 0
                    k = len(response.json()['prediction'][1]['trajectory'])
                    #print("Länge: " + str(k))
                    while j < k:
                        lat = response.json()['prediction'][1]['trajectory'][j]['latitude']
                        #print("Lat", lat)
                    
                        lng = response.json()['prediction'][1]['trajectory'][j]['longitude']
                        #print("Lon", lng)  
                    
                        altitude = response.json()['prediction'][1]['trajectory'][j]['altitude']
                        #print("Höhe", altitude)

                        time = response.json()['prediction'][1]['trajectory'][j]['datetime']
                        time = int(datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%S.%f%z').timestamp())
                        quelle = "predict.cusf.co.uk"

                        mycursor.execute("INSERT INTO prediction (sondenid, lat, lon, hoehe, time, quelle) VALUES (%s,%s,%s,%s,%s,%s)",(sondenids[i],lat,lng,altitude,time,quelle,))        
                        mydb.commit()

                        j = j + 1
                        #print(j)

                else:
                    logging.error("Prediction Request not 200 " + response.url + response.text)


            i = i + 1
    except:
        print("Unexpected error prediction.py:" + str(sys.exc_info()))
        logging.error("Unexpected error presiction.py:" + str(sys.exc_info()))
        return None