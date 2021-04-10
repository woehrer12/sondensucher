import mysql.connector
import configparser
import logging
import sys


def sondenids(mydb):
    try:
        mycursor = mydb.cursor() 
        #TODO nicht mehr auf date Abfragen sondern auf Sondetime
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
        logging.error("Unexpected error sondenids() functions.py:" + str(sys.exc_info()))    

    
