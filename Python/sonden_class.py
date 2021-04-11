import mysql.connector
import numpy as np
import functions
import time
import re
import logging
import sys
import configparser

try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen API.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Config lesen API.py:" + str(sys.exc_info()))

try:
    #Datenbankverbindung herstellen
    mydb = mysql.connector.connect(
        host=conf['dbpfad'],
        user=conf['dbuser'],
        password=conf['dbpassword'],
        database=conf['dbname'],
        auth_plugin='mysql_native_password'
        )
    mycursor = mydb.cursor() 
except:
    print("Unexpected error Datenbankverbindung API.py:" + str(sys.exc_info()))
    logging.error("Unexpected error Datenbankverbindung API.py:" + str(sys.exc_info()))

class Sonden():
    sondenid = ""
    lat = 0.0
    lon = 0.0
    hoehe = 0
    server = 0.0
    vgeschw = 0.0
    freq = ""
    richtung = 0.0
    geschw = 0.0
    sondentime = ""
    server = ""
    confirm = False
    groundhoehe = 0

    
    def clear(self):
        Sonden.sondenid = ""
        Sonden.lat = 0.0
        Sonden.lon = 0.0
        Sonden.hoehe = 0
        Sonden.server = 0.0
        Sonden.vgeschw = 0.0
        Sonden.freq = ""
        Sonden.richtung = 0.0
        Sonden.geschw = 0.0
        Sonden.sondentime = ""
        Sonden.server = ""
        Sonden.confirm = False
        Sonden.groundhoehe = 0


    def setid(self, id):
        mycursor = mydb.cursor()
        Sonden.clear(self)
        logging.info("setid id = " + id)
        text = id
        if text.isalnum() and text[0].isalpha() and len(text) > 7:
            Sonden.sondenid = id
            query = "SELECT sondenid, lat, lon, hoehe, server, vgeschw, freq, richtung, geschw, sondetime FROM sonden WHERE sondenid = '" + Sonden.sondenid + "' ORDER BY `sonden`.`sondetime` DESC LIMIT 1"
            mycursor.execute(query)
            data = mycursor.fetchall()
            if data != []:
                sondendaten = data[0]
                Sonden.sondenid = sondendaten[0]
                Sonden.lat = sondendaten[1]
                Sonden.lon = sondendaten[2]
                Sonden.hoehe = sondendaten[3]
                Sonden.server = sondendaten[4]
                Sonden.vgeschw = sondendaten[5]
                Sonden.freq = sondendaten[6]
                Sonden.richtung = sondendaten[7]
                Sonden.geschw = sondendaten[8]
                Sonden.sondentime = sondendaten[9]
                Sonden.confirm = True

            else:
                print("Not confirm")
                logging.error("ID not confirm" + id)
    
    def refresh(self):
        mycursor = mydb.cursor()
        query = "SELECT sondenid, lat, lon, hoehe, server, vgeschw, freq, richtung, geschw, sondetime FROM sonden WHERE sondenid = '" + Sonden.sondenid + "' ORDER BY `sonden`.`date` DESC LIMIT 1"
        mycursor.execute(query)
        data = mycursor.fetchall()
        sondendaten = data[0]
        Sonden.sondenid = sondendaten[0]
        Sonden.lat = sondendaten[1]
        Sonden.lon = sondendaten[2]
        Sonden.hoehe = sondendaten[3]
        Sonden.server = sondendaten[4]
        Sonden.vgeschw = sondendaten[5]
        Sonden.freq = sondendaten[6]
        Sonden.richtung = sondendaten[7]
        Sonden.geschw = sondendaten[8]
        Sonden.sondentime = sondendaten[9]
    
    
    def print(self):
        print("Sondenid: " + Sonden.sondenid)
        print("Lat: " + Sonden.lat)
        print("Lon: " + Sonden.lon)
        print("Höhe: " + Sonden.hoehe)
        print("Server: " + Sonden.server)
        print("vGesch: " + Sonden.vgeschw)
        print("Freq: " + Sonden.freq)
        print("Richtung: " + Sonden.richtung)
        print("Geschw: " + Sonden.geschw)

    def getid(self):
        return Sonden.sondenid

    def getlat(self):
        return Sonden.lat
    
    def getlon(self):
        return(Sonden.lon)
    
    def gethoehe(self):
        return(Sonden.hoehe)
    
    def getserver(self):
        return(Sonden.server)
        
    def getvgeschw(self):
        return(Sonden.vgeschw)
    
    def getfreq(self):
        return(Sonden.freq)
    
    def getrichtung(self):
        return(Sonden.richtung)
    
    def getgeschw(self):
        return(Sonden.geschw)
        
    def getsondentime(self):
        
        return(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(Sonden.sondentime))))
        #return(Sonden.sondentime)
  

    def getvgeschposD(self):
        query = "SELECT Avg (vgeschw) FROM `sonden` WHERE sondenid = '" + Sonden.sondenid + "'  AND vgeschw > 0"
        mycursor = mydb.cursor()
        mycursor.execute(query)
        a = mycursor.fetchone()
        mycursor.close()
        if type(a[0]) != float:
            return 0
        return(a[0])

    def getvgeschnegD(self):
        query = "SELECT Avg (vgeschw) FROM `sonden` WHERE sondenid = '" + Sonden.sondenid + "'  AND vgeschw < 0"
        mycursor = mydb.cursor()
        mycursor.execute(query)
        a = mycursor.fetchone()
        mycursor.close()
        if type(a[0]) != float:
            return 0
        return(a[0])

    def getmaxhoehe(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT hoehe FROM sonden WHERE sondenid = '" + Sonden.sondenid + "' LIMIT 5000")
        sondendaten = mycursor.fetchall()
        mycursor.close()
        anzahl = len(sondendaten)
        j = 0
        data = np.zeros((3,5000))
        while j < anzahl:
            sondendaten1 = sondendaten[j]
            data[0][j] = sondendaten1[0]
            j = j + 1
        return(max(data[0]))

    def checkburst(self):
        #print(Sonden.vgeschw)
        if float(Sonden.vgeschw) < -2.0 and float(Sonden.hoehe) > 5000 :
            Sonden.setburst(self)

    def isburst(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT burst FROM sonden_stats WHERE sondenid = '" + Sonden.sondenid + "'")
        sondendaten = mycursor.fetchone()
        mycursor.close()
        #print(Sonden.sondenid)
        #if isinstance(sondendaten, list): 
        if sondendaten[0]:
            #print("Burst")
            return True
        else:
            #print("Not Burst")	
            return False
	
    def getstartort(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT startort FROM sonden_stats WHERE sondenid = '" + Sonden.sondenid + "'")
        startort = mycursor.fetchone()
        mycursor.close()
        return str(startort)[2:-3]
    
    def setburst(self):
        Sonden.refresh(self)
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE sonden_stats SET burst = TRUE, latburst = '" + str(Sonden.lat) + "', lonburst = '" + str(Sonden.lon) + "' WHERE sondenid = '" + Sonden.sondenid + "'")
        mydb.commit()

    def startort(self):
        if Sonden.confirm:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM startorte")
            startorte = mycursor.fetchall()
            mycursor.close()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT lat, lon FROM sonden WHERE sondenid = '" + Sonden.sondenid + "' ORDER BY `sonden`.`date` ASC LIMIT 1")
            sondendaten = mycursor.fetchone()
            k = len(startorte)
            i = 0
            while i < k:
                if (float(sondendaten[0]) < float(startorte[i][2]) + 0.1) and (float(sondendaten[0]) > float(startorte[i][2]) - 0.1):
                    if (float(sondendaten[1]) < float(startorte[i][3]) + 0.1) and (float(sondendaten[1]) > float(startorte[i][3]) - 0.1):
                        #print(startorte[i][1])
                        #print(type(startorte[i][1]))
                        return(startorte[i][1])
                i = i + 1
                #print(i)
        else:
            logging.error("Not Confirmed startort() sonden_class")
        return("unbekannt")

    def updatestartort(self):
        if Sonden.confirm:
            logging.error("Startort konnte nicht definiert werden:  " + Sonden.sondenid)
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM startorte")
            startorte = mycursor.fetchall()
            mycursor.close()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT lat, lon FROM sonden WHERE sondenid = '" + Sonden.sondenid + "' ORDER BY `sonden`.`date` ASC LIMIT 1")
            sondendaten = mycursor.fetchone()
            k = len(startorte)
            i = 0
            while i < k:
                if (float(sondendaten[0]) < float(startorte[i][2]) + 0.1) and (float(sondendaten[0]) > float(startorte[i][2]) - 0.1):
                    if (float(sondendaten[1]) < float(startorte[i][3]) + 0.1) and (float(sondendaten[1]) > float(startorte[i][3]) - 0.1):
                        payload = "UPDATE sonden_stats SET startort = '" + startorte[i][1] + "' WHERE sondenid = '" + Sonden.sondenid + "'"
                        print(payload)
                        mycursor.execute(payload)
                        mydb.commit()
                i = i + 1
        else:
            logging.error("Not Confirmed updatestartort() sonden_class")        


    def isconfirm(self):
        return Sonden.confirm

    def set_stats(self):
        if Sonden.confirm == True:
            Sonden.checkburst(self)
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM `sonden_stats` WHERE sondenid = '"+ Sonden.sondenid + "' ")
            sonden = mycursor.fetchall()
            if sonden != []:
                mycursor.execute("UPDATE sonden_stats SET max_hoehe = '" + str(Sonden.getmaxhoehe(self)) + "', vgeschposD = '" + str(Sonden.getvgeschposD(self)) + "', vgeschnegD = '" + str(Sonden.getvgeschnegD(self)) + "' WHERE sondenid = '" + Sonden.sondenid + "'")
                mydb.commit()
            else:
                payload = "INSERT INTO sonden_stats (sondenid, startort, max_hoehe, vgeschposD, vgeschnegD, sondetime) VALUES ('" + Sonden.sondenid + "', '" + Sonden.startort(self) + "', " + str(Sonden.getmaxhoehe(self)) + "," + str(Sonden.getvgeschposD(self)) + "," + str(Sonden.getvgeschnegD(self)) + "," + str(Sonden.sondentime) + ")"
                mycursor.execute(payload)
                mydb.commit()
        else:
            logging.error("Set_Stat konnte nicht durchgeführt werden ")

    def getgroudhohe(self):
        mycursor = mydb.cursor() 
        mycursor.execute("SELECT Hoehe FROM hoehen WHERE Lat = " + str(Sonden.lat) + " AND  Lon = " + str(Sonden.lon))
        hoehe = mycursor.fetchone()
        #Um den Fetch zu leeren
        buffer = mycursor.fetchall()
        #print(hoehe)
        if hoehe == None:
            mycursor.execute("INSERT INTO hoehen (lat, lon, hoehe, quelle) VALUES (%s,%s,%s,%s)",(str(Sonden.lat),str(Sonden.lon),"0","sonden_class.py",))
            mydb.commit()
            return 0
        return hoehe