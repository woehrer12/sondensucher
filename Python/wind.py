# -*- coding: utf-8 -*-

#from mpl_toolkits.mplot3d import Axes3D
import mysql.connector
import numpy as np
import time
import datetime
import threading
import multiprocessing as mp
import logging
import xml.etree.ElementTree as ElementTree
import plotly.figure_factory as ff
    

def hoeheeintragen(data,quelle,mydb):
    mycursor = mydb.cursor()
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            
    mycursor.execute("INSERT INTO wind (Lat, Lon, Hoehe, Geschw, Richtung, Quelle, date) VALUES (%s,%s,%s,%s,%s,%s,%s)",(data[0],data[1],data[2],data[3],data[4],quelle,timestamp))        
    mydb.commit()

#Höhen definieren
hoehemin = 1000
hoehemax = 1000
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
    logging.info("Wind start")
    root = ElementTree.Element("Wind") 

    data = np.zeros((6))
    x = np.zeros(1)
    y = np.zeros(1)
    u = np.zeros(1)
    v = np.zeros(1)


    # mycursor.execute("DELETE FROM `wind` WHERE  date <= NOW()-INTERVAL 5 HOUR")
    # mydb.commit()

    #print(lat)
    Abfragen = ((hoehemax - hoehemin + hoehestep)/hoehestep)*((latmax - latmin + latstep)/latstep)*((lonmax - lonmin + lonstep)/lonstep)
    #print(Abfragen)
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
                #print("Höhe",dhoehe)
                #print("Lat",dlat)
                #print("Lon",dlon)
                
                
    #            if __name__ == '__main__':
    #                p1 = mp.Process(target=abfragen(dhoehe,hoehebis,dlat,latbis,dlon,lonbis))
    #                p1.start()
                    
                mycursor.execute("SELECT geschw, richtung, sondenid FROM sonden WHERE hoehe BETWEEN %s AND %s AND lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s AND date>(NOW() - INTERVAL 1440 MINUTE) LIMIT 1",(str(dhoehe),str(hoehebis),str(dlat),str(latbis),str(dlon),str(lonbis),))
                myresult = mycursor.fetchall()
                if myresult != []:
                    myresult = myresult[0]
                    #print(myresult)
                    data[0] = float(dlat)
                    data[1] = float(dlon)
                    data[2] = float(dhoehe)
                    data[3] = float(myresult[0])
                    data[4] = float(myresult[1])
                    quelle = myresult[2]

                    data_element = ElementTree.SubElement(root, "Data")
                    ElementTree.SubElement(data_element, "Lat").text = str(dlat)
                    ElementTree.SubElement(data_element, "Lon").text = str(dlon)
                    ElementTree.SubElement(data_element, "Hoehe").text = str(dhoehe)
                    ElementTree.SubElement(data_element, "Geschwindigkeit").text = str(data[3])
                    ElementTree.SubElement(data_element, "Richtung").text = str(data[4])
                    
                    x = np.append(x, dlat)
                    y = np.append(y, dlon)
                    u = np.append(u, (data[4]))
                    v = np.append(v, data[3]/1000)


                    
                abgefragt = abgefragt + 1
                #print("%.2f" % (abgefragt/Abfragen*100),"%")
                dlon = dlon + lonstep
            dlat = dlat + latstep
        dhoehe = dhoehe + hoehestep
    logging.info("Datenabfrage beendet")

    tree = ElementTree.ElementTree(root) 

    with open ("Wind/Wind.xml", "wb") as output : 
        tree.write(output) 

    logging.info("Wind wurde erstellt")

    fig = ff.create_quiver(x, y, u, v)



    fig.write_html('Wind/first_figure.html', auto_open=True)
