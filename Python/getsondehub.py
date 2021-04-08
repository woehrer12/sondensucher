import mysql.connector
import configparser
import requests
import sys
import logging

def csv():
    try:
        mycursor = mydb.cursor() 
        logging.basicConfig(filename='logs/getsondehub.log', level=logging.INFO)

        response = requests.get("https://api.v2.sondehub.org/sondes/telemetry",  timeout=30)
        logging.info(response.url)


        if response.status_code == 200:
            #print('Success!')
            
            #print(response.text)
            
            ok = response.json()['status']
            #print(ok)
            
            j = 0
            k = len(response.json()['results'])
            while j < k:
                if ok == "OK":

            
        elif response.status_code == 404:
            print('Not Found.')
    except:
        print("Unexpected error hoehen() hoehen.py:" + str(sys.exc_info()))
        logging.error("Unexpected error hoehen.py:" + str(sys.exc_info()))
        return None

csv()