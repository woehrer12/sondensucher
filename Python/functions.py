import mysql.connector
import configparser
import logging
import sys
import time


def sondenids(mydb,minuten):
    try:
        sekunden = minuten * 60
        mycursor = mydb.cursor() 
        now = int(time.time())
        payload = "SELECT sondenid FROM sonden WHERE sondetime>(" + str(now) + " - " + str(sekunden) + ") AND lat!='0' AND sondenid<>'' GROUP BY sondenid"
        mycursor.execute(payload)
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
        logging.error("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))    

def sondenids_startort(mydb,minuten,startort):
    try:
        sekunden = minuten * 60
        mycursor = mydb.cursor() 
        now = int(time.time())
        payload = "SELECT sondenid FROM sonden_stats WHERE sondetime>(" + str(now) + " - " + str(sekunden) + ") AND lat!='0' AND sondenid<>'' GROUP BY sondenid"
        logging.info(payload)
        mycursor.execute(payload)
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
        logging.error("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))  