import mysql.connector
import configparser
import requests

#Config Datei auslesen
config = configparser.ConfigParser()
config.read('dbconfig.ini')
conf = config['DEFAULT']

#Datenbankverbindung herstellen
mydb = mysql.connector.connect(
    host=conf['dbpfad'],
    user=conf['dbuser'],
    password=conf['dbpassword'],
    database=conf['dbname'],
    auth_plugin='mysql_native_password'
    )
mycursor = mydb.cursor() 

def hoehe():
    payload = ""
    #Abfrage nach Höhen mir ?
    #TODO Exeption Handling einbauen wegen verlieren der Verbindung zur Datenbank
    mycursor.execute("SELECT Id, Lat, Lon FROM hoehen WHERE Hoehe = '?' LIMIT 25")
    request = mycursor.fetchall()
    länge = len(request)
    i=0
    #Funktion verlassen wenn keine Höhen erforderlich sind
    if länge == 0:
        return None
        print("Keine Höhen zum Abfragen gefunden")
    #Alle Höhen in Payload packen
    while i < länge:
        request1 = request[i]
        payload = payload + str(request1[1]) + "," + str(request1[2]) + "|"
        print(payload)
        s = str(request1[0])
        mycursor.execute("DELETE FROM hoehen WHERE Id = "+ str(request1[0]))
        i = i + 1

    response = requests.get("https://api.opentopodata.org/v1/eudem25m?locations=" + payload,  timeout=30)
    print (response.url)

    quelle = "eudem25m"

    if response.status_code == 200:
        print('Success!')
        
        #print(response.text)
        
        ok = response.json()['status']
        print(ok)
        
        j = 0
        k = len(response.json()['results'])
        while j < k:
            if ok == "OK":
                print("Abfrage war OK")
                    
                lat = response.json()['results'][j]['location']['lat']
                print("Lat", lat)
            
                lng = response.json()['results'][j]['location']['lng']
                print("Lon", lng)  
            
                elevation = response.json()['results'][j]['elevation']
                print("Höhe", elevation)
    
                #Prüfen ob schon in Datenbank vorhanden

                mycursor.execute("SELECT Lat, Lon FROM hoehen WHERE Lat LIKE %s AND Lon LIKE %s LIMIT 25", (lat, lng ))
                request = mycursor.fetchall()
                print(request)
                if elevation == None:
                    elevation = "Wasser"
                if request == []: 
                
                    #In Datenbank eintragen       
                    mycursor.execute("INSERT INTO hoehen (Lat, Lon, Hoehe, Quelle) VALUES (%s,%s,%s,%s)",(lat,lng,elevation,quelle,))        
                    mydb.commit()
                    neue = neue + 1
                
                
                
            j = j + 1     
        
    elif response.status_code == 404:
        print('Not Found.')


