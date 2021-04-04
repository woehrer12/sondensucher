import csv 
import requests
import mysql.connector
import configparser

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

#Header fälschen
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

url = "https://radiosondy.info/export/csv_live.php"

#sondenid; lat; lon; hoehe; geschw; vgeschw; richtung; freq; sondetime

httpx = requests.get(url, headers=headers)

antwort = httpx.text

print(antwort)

for line in antwort.split('\n'):
    print(line)
    sonde = []
    for line in line.split(';'):
        sonde.append(line)
        print(line)
    #Leere Lines nicht eintragen
    if sonde != [''] :
        print(sonde)
        #TODO Datenbank eintrag richtig anlegen und prüfen
        mycursor.execute("INSERT INTO sonden (sondenid, lat, lon, hoehe, geschw, vgeschw, richtung, freq, sondetime) VALUES (%s,%s,%s,%s)",(lat,lng,elevation,quelle,))        
        mydb.commit()

