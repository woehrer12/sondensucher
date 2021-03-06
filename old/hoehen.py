import mysql.connector
import configparser
import requests
import sys
import logging

def hoehe(mydb):
    try:
        mycursor = mydb.cursor() 
        payload = ""
        #Abfrage nach Höhen mir quelle
        mycursor.execute("SELECT id, lat, lon FROM hoehen WHERE quelle = 'sonden_class.py' LIMIT 50")
        request = mycursor.fetchall()
        länge = len(request)
        i = 0
        #Funktion verlassen wenn keine Höhen erforderlich sind
        if länge == 0:
            logging.info("Keine Höhen zum Abfragen gefunden")
            return None
        #Alle Höhen in Payload packen
        while i < länge:
            request1 = request[i]
            payload = payload + str(request1[1]) + "," + str(request1[2]) + "|"
            i = i + 1

        response = requests.get("https://api.opentopodata.org/v1/eudem25m?locations=" + payload,  timeout=30)
        logging.info(response.url)

        quelle = "eudem25m"

        if response.status_code == 200:
            #print('Success!')
            
            i = 0
            #Alle Daten löschen
            while i < länge:
                request1 = request[i]
                s = str(request1[0])
                mycursor.execute("DELETE FROM hoehen WHERE Id = "+ str(request1[0]))
                i = i + 1

            #print(response.text)
            
            ok = response.json()['status']
            #print(ok)
            
            j = 0
            k = len(response.json()['results'])
            while j < k:
                if ok == "OK":
                    #print("Abfrage war OK")
                        
                    lat = response.json()['results'][j]['location']['lat']
                    #print("Lat", lat)
                
                    lng = response.json()['results'][j]['location']['lng']
                    #print("Lon", lng)  
                
                    elevation = response.json()['results'][j]['elevation']
                    #print("Höhe", elevation)
        
                    #Prüfen ob schon in Datenbank vorhanden
                    query = "SELECT lat, lon FROM hoehen WHERE lat LIKE " + str(lat) + " AND lon LIKE " + str(lng) + " LIMIT 25"
                    mycursor.execute(query)
                    request = mycursor.fetchall()
                    if elevation == None:
                        elevation = 'NULL'
                    if request == []: 
                    
                        #In Datenbank eintragen
                        query = "INSERT INTO hoehen (lat, lon, hoehe, quelle) VALUES (" + str(lat) + ", " + str(lng) + ", " + str(elevation) + ", '" + quelle + "' )"
                        mycursor.execute(query)        
                        mydb.commit()
                    
                j = j + 1     
            
        elif response.status_code == 404:
            logging.error('Höhen 404 Not Found.')
        else:
            logging.info("Höhen not 200")
    except:
        print("Unexpected error hoehen() hoehen.py:" + str(sys.exc_info()))
        logging.error("Unexpected error hoehen.py:" + str(sys.exc_info()))
        return None
