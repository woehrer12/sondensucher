import mysql.connector
import configparser
import functions

from sonden_class import Sonden
sonde = Sonden()


#Config Datei auslesen
config = configparser.ConfigParser()
config.read('dbconfig.ini')
conf = config['DEFAULT']

mydb = mysql.connector.connect(
  host=conf['dbpfad'],
  user=conf['dbuser'],
  password=conf['dbpassword'],
  database=conf['dbname'],
  auth_plugin='mysql_native_password'
)

def sonde():
    sondenids = functions.sondenids()
    anzahlids = len(sondenids)
    j = 0

    while j <anzahlids:
        sonde.setid(sondenids[j])
        j = j + 1
        
        if float(sonde.getvgeschw()) < 2.0 and float(sonde.gethoehe()) > 5000 :
            if sonde.isburst() == False:
                sonde.setburst()
    

        if float(sonde.getvgeschw()) > 2.0 and float(sonde.gethoehe()) < 3000:
            sonde.startort()



sonde()