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

def sonden():
    sondenids = functions.sondenids()
    anzahlids = len(sondenids)
    j = 0


    

    while j <anzahlids:
        sonde.setid(sondenids[j])
        print(sonde.getgroudhohe())
        print(type(sonde.getgroudhohe()))
        j = j + 1
        


sonden()