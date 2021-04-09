import mysql.connector
import configparser
import os
import logging
import sys


def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


def sonden(mydb):
    try:
        mycursor = mydb.cursor()
        # Datenbank sonden anlegen
        if checkTableExists(mydb, "sonden"):
            logging.info("Datenbank Sonden Existiert")
        else:
            logging.info("Datenbank Sonden Existiert nicht")
            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE sonden(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `sondenid` text NOT NULL, \
                `lat` double NOT NULL, \
                `lon` double NOT NULL, \
                `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                `hoehe` int NOT NULL, \
                `server` text NOT NULL, \
                `vgeschw` double NOT NULL, \
                `temp` double DEFAULT '0.0' NOT NULL, \
                `freq` text NOT NULL, \
                `richtung` double NOT NULL, \
                `geschw` double NOT NULL, \
                `rssi` double DEFAULT '0.0' NOT NULL, \
                `sondetime` text NOT NULL, \
                `latsucher` double DEFAULT '0.0' NOT NULL, \
                `lonsucher` double DEFAULT '0.0' NOT NULL, \
                `altsucher` double DEFAULT '0.0' NOT NULL, \
                `dirsucher` double DEFAULT '0.0' NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Sonden wurde erstellt")
    except:
        print("Unexpected error Datenbank Sonden anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Sonden anlegen Database.py:" + str(sys.exc_info()))


def hoehen(mydb):
    try:
        mycursor = mydb.cursor()
        # Datenbank Höhen anlegen
        if checkTableExists(mydb, "hoehen"):
            logging.info("Datenbank Höhen Existiert")
        else:
            logging.info("Datenbank Höhen Existiert nicht")
            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE hoehen(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `lat` double NOT NULL, \
                `lon` double NOT NULL, \
                `hoehe` double NOT NULL, \
                `quelle` text NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Höhen wurde erstellt")
    except:
        print("Unexpected error Datenbank Höhen anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Höhen anlegen Database.py:" + str(sys.exc_info()))


def statistiken(mydb):
    try:
        mycursor = mydb.cursor()
        # Datenbank sonden anlegen
        if checkTableExists(mydb, "sonden_stats"):
            logging.info("Datenbank Sonden Statistiken Existiert")
        else:
            logging.info("Datenbank Sonden Statistiken Existiert nicht")
            mycursor.execute("CREATE TABLE sonden_stats(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `sondenid` text NOT NULL, \
                `startort` text NOT NULL, \
                `max_hoehe` int(11) NOT NULL, \
                `vgeschposD` text NOT NULL, \
                `vgeschnegD` text NOT NULL, \
                `burst` tinyint(1) DEFAULT '0' NOT NULL, \
                `latburst` double DEFAULT '0.0' NOT NULL, \
                `lonburst` double DEFAULT '0.0' NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Sonden Statistiken wurde erstellt")
    except:
        print("Unexpected error Datenbank Statistiken anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Statistiken anlegen Database.py:" + str(sys.exc_info()))


def löschen(mydb):
    # try:
    mycursor = mydb.cursor()
    payload = "SELECT d1.id FROM sonden d1, sonden d2 WHERE d1.id != d2.id AND d1.sondenid = d2.sondenid AND d1.sondetime = d2.sondetime LIMIT 2000 "
    mycursor.execute(payload)
    sonden = mycursor.fetchall()
    # print(str(sonden[1])[1:-2])

    string = ""
    for i in sonden:
        payload = "DELETE FROM sonden WHERE id = " + str(i)[1:-2]
        mycursor.execute(payload)
    mydb.commit()
    logging.info("Datensätze gelöscht Anzahl: " + str(len(sonden)))
    # except:
    #     print("Unexpected error Datenbank doppelte Löchen Database.py:" + str(sys.exc_info()))
    #     logging.error("Unexpected error Datenbank doppelte Löschen Database.py:" + str(sys.exc_info()))
