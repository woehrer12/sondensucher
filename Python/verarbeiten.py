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
    print(sondenids[1])
    mycursor = mydb.cursor()
    query = "SELECT lat FROM sonden WHERE sondenid = '" + sondenids[1] + "' LIMIT 1"
    print(query)
    mycursor.execute(query)
    sondendaten = mycursor.fetchone()
    mycursor.close()
    print(sondendaten[0])
    print(type(sondendaten[0]))


    while j <anzahlids:
        #sonde.setid(sondenids[j])
        j = j + 1
        


sonden()