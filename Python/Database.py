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
                `sondetime` int(11) NOT NULL, \
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
                `sondetime` int(11) DEFAULT '0' NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Sonden Statistiken wurde erstellt")
    except:
        print("Unexpected error Datenbank Statistiken anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Statistiken anlegen Database.py:" + str(sys.exc_info()))

def startorte(mydb):
    try:
        mycursor = mydb.cursor()
        # Datenbank sonden anlegen
        if checkTableExists(mydb, "startorte"):
            logging.info("Datenbank Startorte Existiert")
        else:
            logging.info("Datenbank startorte Existiert nicht")
            mycursor.execute("CREATE TABLE startorte(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `name` text NOT NULL, \
                `lat` double NOT NULL, \
                `lon` double NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Startorte wurde erstellt")
            query = "INSERT INTO `startorte` ( `name`, `lat`, `lon`) VALUES \
                    ( 'Stuttgart', 48.8281, 9.20063), \
                    ( 'Idar Oberstein', 49.6927, 7.32619), \
                    ( 'Bundeswehr Altenstadt/Schongau', 47.84, 10.88), \
                    ( 'Bergen', 52.82, 9.93), \
                    ( 'Emden-Flugplatz', 53.389, 7.2284), \
                    ( 'Essen', 51.4041, 6.9682), \
                    ( 'Greifswald', 54.1, 13.4), \
                    ( 'Hohenspeissenberg', 47.8, 11.01), \
                    ( 'Kümmersbruck', 49.43, 11.9), \
                    ( 'Lindenberg', 52.2094, 14.1202), \
                    ( 'Meiningen', 50.57, 10.38), \
                    ( 'Meppen', 52.73, 7.33), \
                    ( 'München-Oberschleissheim', 48.26, 11.56), \
                    ( 'Schleswig', 54.53, 9.55), \
                    ( 'Düren', 49.31, 6.69), \
                    ( 'Norderney', 53.7124, 7.15199), \
                    ( 'Hamburg Sasel', 53.6493, 10.1102), \
                    ( 'Karlsruhe', 49.1, 8.43), \
                    ( 'Baumholder (Lager Aulenbach)', 49.633, 7.303), \
                    ( 'Calw', 48.71, 8.77), \
                    ( 'Frankfurt', 50.2225, 8.4473), \
                    ( 'Algenrodt', 49.71, 7.295), \
                    ( 'Jülich', 50.9, 6.47), \
                    ( 'Koblenz Asterstein (mil)', 50.34, 7.62), \
                    ( 'Mayen (mil)', 50.329, 7.187), \
                    ( 'Herstmonceux (G)', 50.891, 0.3164), \
                    ( 'Beauvechain (ON)', 50.75, 4.77), \
                    ( 'Uccle (ON)', 50.798, 4.3573), \
                    ( 'Brest-Guipavas (F)', 48.45, -4.42), \
                    ( 'Trappes (F)', 48.77, 2.01), \
                    ( 'Camborne (G)', 50.21, 5.32), \
                    ( 'Barcelona (EA)', 41.62, 2.2), \
                    ( 'Bordeaux-Mérignac (F)', 44.82, -0.68), \
                    ( 'Payerne (CH)', 46.82, 6.95), \
                    ( 'Santander (EA)', 43.48, -3.8), \
                    ( 'Nîmes-Courbessac (F)', 43.87, 4.4), \
                    ( 'Cuneo-Levaldigi (I)', 44.54, 7.62), \
                    ( 'Milano-Linate (I)', 45.44, 9.28), \
                    ( 'Ajaccio (F)', 41.92, 8.8), \
                    ( 'São Paulo (BR)', -23.51, -46.63 ), \
                    ( 'Melbourne (AU)', -37.65, 144.845 ), \
                    ( 'Decimomannu (IT)', -39.35, 8.97 ), \
                    ( 'Stavanger (NO)', 58.87, 5.63 ), \
                    ( 'Zagreb (HR)', 45.82, 16.03 ), \
                    ( 'Poprad (SK)', 49.07, 20.37 ), \
                    ( 'Budapest (HU)', 47.43, 19.17 ), \
                    ( 'Watnall (GB)', 52.99, -1.24 ), \
                    ( 'Legionowo (PL)', 52.411, 20.95 ), \
                    ( 'Lisbon (PT)', 38.77, -9.12 ), \
                    ( 'Camborne (GB)', 50.20, -5.32 ), \
                    ( 'Madrid (ES)', 40.46, -3.57 ), \
                    ( 'Wrocław (PL)', 51.11, 16.88 ), \
                    ( 'Prostějov (CZ)', 49.46, 17.13 ), \
                    ( 'Szeged (HU)', 46.25, 20.08 ), \
                    ( 'Adelaide (AU)', -34.94, 138.51 ), \
                    ( 'Praha (CZ)', 50.01, 14.43), \
                    ( 'A Coruña (ES)', 43.36, -8.44 ), \
                    ( 'Zadar (HR)', 44.11, 15.32 ), \
                    ( 'New Taipei (TW)', 24.99, 121.44 ), \
                    ( 'Oakland [CA] (USA)', 37.72, -122.22 ), \
                    ( 'Bucarest (RO)', 44.50, 26.20 ), \
                    ( 'San Diego [CA] (USA)', 32.81, -117.13 ), \
                    ( 'Salem [OR] (USA)', 44.9092, -123.01 ), \
                    ( 'Nicosia (CY)', 35.13, 33.39 ), \
                    ( 'Brasilia (BR)', -15.87, -47.91 ), \
                    ( 'Londrina (BR)', -23.33, -51.12 ), \
                    ( 'Curitiba (BR)', -25.48, -49.08 ), \
                    ( 'Sodankyla (FI)', 67.3525, 26.8375 ), \
                    ( 'Porto Alegre (BR)', -29.99, -51.17 ), \
                    ( 'Trapani-Birgi (IT)', 37.91, 12.48 ), \
                    ( 'Ankara (TR)', 39.97, 32.86 ), \
                    ( 'Vienna (AT)', 48.25, 16.35 ), \
                    ( 'Larkhill (GB)', 51.19, -1.75 ), \
                    ( 'Niš (RS)', 43.32, 21.89 ), \
                    ( 'Jokioinen (FI)', 60.83, 23.49 ), \
                    ( 'Sofia (BG)', 42.65, 23.38 ), \
                    ( 'Belgrade (RS)', 44.77, 20.42 ) \
                        ;"
            mycursor.execute(query)        
            mydb.commit()
    except:
        print("Unexpected error Datenbank Startorte anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Startorte anlegen Database.py:" + str(sys.exc_info()) + query)


def startort_stats(mydb):
    try:
        mycursor = mydb.cursor()
        # Datenbank sonden anlegen
        if checkTableExists(mydb, "startort_stats"):
            logging.info("Datenbank Startorte Statistiken Existiert")
        else:
            logging.info("Datenbank Startorte Statistiken Existiert nicht")
            mycursor.execute("CREATE TABLE startort_stats(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `startort` text NOT NULL, \
                `anzahl_sonden_72h` int(11) NOT NULL, \
                `vgeschposD` double NOT NULL, \
                `vgeschnegD` double NOT NULL, \
                `maxhoeheD` double NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Startorte Statistiken wurde erstellt")
    except:
        print("Unexpected error Datenbank Startorte Statistiken anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Startorte Statistiken anlegen Database.py:" + str(sys.exc_info()))

def prediction(mydb):
    try:
        mycursor = mydb.cursor()
        # Datenbank sonden anlegen
        if checkTableExists(mydb, "prediction"):
            logging.info("Datenbank Prediction Existiert")
        else:
            logging.info("Datenbank Prediction Existiert nicht")
            mycursor.execute("CREATE TABLE prediction(\
                `id` int(11) NOT NULL AUTO_INCREMENT, \
                `sondenid` text NOT NULL, \
                `lat` double NOT NULL, \
                `lon` double NOT NULL, \
                `hoehe` double NOT NULL, \
                `quelle` text NOT NULL, \
                PRIMARY KEY (id) \
                )")
            logging.info("Datenbank Startorte Statistiken wurde erstellt")
    except:
        print("Unexpected error Datenbank Startorte Statistiken anlegen Database.py:" +
              str(sys.exc_info()))
        logging.error(
            "Unexpected error Datenbank Startorte Statistiken anlegen Database.py:" + str(sys.exc_info()))

def löschen(mydb):
    try:
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
    except:
        print("Unexpected error Datenbank doppelte Löchen Database.py:" + str(sys.exc_info()))
        logging.error("Unexpected error Datenbank doppelte Löschen Database.py:" + str(sys.exc_info()))
