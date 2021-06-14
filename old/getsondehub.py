import mysql.connector
import configparser
import requests
import sys
import logging
import json
import datetime


def csv(mydb):
    try:
        mycursor = mydb.cursor()
        logging.info("Sondehub Start")
        response = requests.get(
            "https://api.v2.sondehub.org/sondes/telemetry",  timeout=60)
        logging.info(response.url)
        jobs = []
        if response.status_code == 200:
            logging.info('Sondehub Success!')
            r = response.json()

            for i in r.keys():
                s = response.json()[i]
                for j in s.keys():
                    letzterkey = j

                dateneintrag(mydb, response, i, letzterkey)
            logging.info("Sondehub fertig")
        elif response.status_code == 404:
            print('Not Found.')
    except:
        print("Unexpected error getsondehub.py:" + str(sys.exc_info()))
        logging.error("Unexpected error getsondehub.py:" + str(sys.exc_info()))
        return None

def csv_alle(mydb):
    try:
        mycursor = mydb.cursor()
        logging.info("Sondehub Start")
        response = requests.get(
            "https://api.v2.sondehub.org/sondes/telemetry",  timeout=60)
        logging.info(response.url)
        jobs = []
        if response.status_code == 200:
            logging.info('Sondehub Success!')
            r = response.json()

            for i in r.keys():
                s = response.json()[i]
                for j in s.keys():
                    dateneintrag(mydb, response, i, j)
            logging.info("Sondehub fertig")
        elif response.status_code == 404:
            print('Not Found.')
    except:
        print("Unexpected error getsondehub.py:" + str(sys.exc_info()))
        logging.error("Unexpected error getsondehub.py:" + str(sys.exc_info()))
        return None





def dateneintrag(mydb, response, i, j):
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
    sondetime = int(datetime.datetime.strptime(
        response.json()[i][j]['datetime'], '%Y-%m-%dT%H:%M:%S.%f%z').timestamp())
    mycursor = mydb.cursor()
    payload = "INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime, server) VALUES ('" + i + "', " + str(lat) + ", " + str(
        lon) + ", " + str(alt) + ", " + str(geschw) + ", " + str(vgeschw) + ", " + str(richtung) + ", " + str(freq) + ", " + str(sondetime) + ", 'Sondehub')"
    mycursor.execute(payload)
    mydb.commit()
