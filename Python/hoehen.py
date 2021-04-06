import mysql.connector
import configparser
import requests
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/hoehen.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info("Skript gestartet")

try:
    #Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen hoehen.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Config lesen hoehen.py:" + str(sys.exc_info()))

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
    print("Unexpected error Datenbankverbindung hoehen.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Datenbankverbindung hoehen.py:" + str(sys.exc_info()))

def hoehe():
    try:
        payload = ""
        #Abfrage nach Höhen mir ?
        #TODO Exeption Handling einbauen wegen verlieren der Verbindung zur Datenbank
        mycursor.execute("SELECT id, lat, lon FROM hoehen WHERE quelle = 'sonden_class.py' LIMIT 50")
        request = mycursor.fetchall()
        länge = len(request)
        i=0
        #Funktion verlassen wenn keine Höhen erforderlich sind
        if länge == 0:
            logging.info("Keine Höhen zum Abfragen gefunden")
            return None
        #Alle Höhen in Payload packen
        while i < länge:
            request1 = request[i]
            payload = payload + str(request1[1]) + "," + str(request1[2]) + "|"
            s = str(request1[0])
            mycursor.execute("DELETE FROM hoehen WHERE Id = "+ str(request1[0]))
            i = i + 1

        response = requests.get("https://api.opentopodata.org/v1/eudem25m?locations=" + payload,  timeout=30)
        logging.info(response.url)

        quelle = "eudem25m"

        if response.status_code == 200:
            #print('Success!')
            
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
                        elevation = 0
                    if request == []: 
                    
                        #In Datenbank eintragen
                        query = "INSERT INTO hoehen (lat, lon, hoehe, quelle) VALUES (" + str(lat) + ", " + str(lng) + ", " + str(elevation) + ", '" + quelle + "' )"
                        mycursor.execute(query)        
                        mydb.commit()
                    
                j = j + 1     
            
        elif response.status_code == 404:
            print('Not Found.')
    except:
        print("Unexpected error hoehen() hoehen.py:" + str(sys.exc_info()))
        return None
