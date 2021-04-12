# -*- coding: utf-8 -*-

#from mpl_toolkits.mplot3d import Axes3D
import mysql.connector
import numpy as np
import time
import datetime
import threading
import multiprocessing as mp
import logging
import xml.etree.ElementTree as gfg
    

def hoeheeintragen(data,quelle,mydb):
    mycursor = mydb.cursor()
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            
    mycursor.execute("INSERT INTO wind (Lat, Lon, Hoehe, Geschw, Richtung, Quelle, date) VALUES (%s,%s,%s,%s,%s,%s,%s)",(data[0],data[1],data[2],data[3],data[4],quelle,timestamp))        
    mydb.commit()

#Höhen definieren
hoehemin = 1000
hoehemax = 40000
hoehestep = 1000

#Lat definieren
latmin = 47.0
latmax = 56.0
latstep = 0.5

#Lon definieren
lonmin = 5.0
lonmax = 16.0
lonstep = 0.5

def wind_xml(mydb):
    mycursor = mydb.cursor()

    root = gfg.Element("Wind") 

    data = np.zeros((6))

    mycursor.execute("DELETE FROM `wind` WHERE  date <= NOW()-INTERVAL 5 HOUR")
    mydb.commit()

    #print(lat)
    Abfragen = ((hoehemax - hoehemin + hoehestep)/hoehestep)*((latmax - latmin + latstep)/latstep)*((lonmax - lonmin + lonstep)/lonstep)
    print(Abfragen)
    abgefragt = 0
    i = 0
    dhoehe = hoehemin
    while dhoehe <=hoehemax:
        hoehebis = dhoehe + hoehestep
        dlat = latmin
        while dlat <=latmax:
            dlon = lonmin
            while dlon <=lonmax:
                latbis = dlat + latstep
                lonbis = dlon + lonstep
                print("Höhe",dhoehe)
                print("Lat",dlat)
                print("Lon",dlon)
                
                
    #            if __name__ == '__main__':
    #                p1 = mp.Process(target=abfragen(dhoehe,hoehebis,dlat,latbis,dlon,lonbis))
    #                p1.start()
                    
                mycursor.execute("SELECT geschw, richtung, sondenid FROM sonden WHERE hoehe BETWEEN %s AND %s AND lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s AND date>(NOW() - INTERVAL 1440 MINUTE) LIMIT 1",(str(dhoehe),str(hoehebis),str(dlat),str(latbis),str(dlon),str(lonbis),))
                myresult = mycursor.fetchall()
                if myresult != []:
                    myresult = myresult[0]
                    print(myresult)
                    data[0] = float(dlat)
                    data[1] = float(dlon)
                    data[2] = float(dhoehe)
                    data[3] = float(myresult[0])
                    data[4] = float(myresult[1])
                    quelle = myresult[2]



                    # t1 = threading.Thread(target=hoeheeintragen(data,quelle))
                    # t1.start()



                    data_element = gfg.SubElement(root, "Data")
                    gfg.SubElement(data_element, "Lat").text = str(dlat)
                    gfg.SubElement(data_element, "Lon").text = str(dlon)
                    gfg.SubElement(data_element, "Hoehe").text = str(dhoehe)
                    gfg.SubElement(data_element, "Geschwindigkeit").text = str(dhoehe)
                    gfg.SubElement(data_element, "Richtung").text = str(dhoehe)
                    
                    
                    
                    
                    
                abgefragt = abgefragt + 1
                print("%.2f" % (abgefragt/Abfragen*100),"%")
                dlon = dlon + lonstep
            dlat = dlat + latstep
        dhoehe = dhoehe + hoehestep

    logging.info("Datenabfrage beendet")



    tree = gfg.ElementTree(root) 

    with open ("XML/Wind.xml", "wb") as output : 
        tree.write(output) 

    logging.info("XML wurde erstellt")
