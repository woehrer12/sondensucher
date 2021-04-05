import mysql.connector
import configparser

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

def sondenids():
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="sondensucher",
    #     password="g7BruFJ9sxmPJvCb",
    #     database="sonden"
    # )
    mycursor = mydb.cursor() 
    mycursor.execute("SELECT sondenid FROM sonden WHERE date>(NOW() - INTERVAL 30 MINUTE) AND lat!='0' AND sondenid<>'' GROUP BY sondenid")
    sondenids = mycursor.fetchall()
    i = 0
    anzahl = len(sondenids)
    list = []
    while i < anzahl:
        string = str(sondenids[i])
        stringlänge = len(string)
        #print(stringlänge)
        list.append(string[2:stringlänge-3]) 
        i += 1

    return list

def tupletostring(sondenid):
    string = str(sondenid)
    stringlänge = len(string)
    #print(stringlänge)
    return string[2:stringlänge-3] 

    
