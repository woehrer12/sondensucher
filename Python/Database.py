import mysql.connector
import configparser
import os

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


# Config Datei anlegen und auslesen
config = configparser.ConfigParser()
if os.path.isfile("dbconfig.ini"):
    ("Config File gefunden")
else:
    print("Config File angelegt")
    config['DEFAULT'] = {'dbpfad': 'db',
                      'dbuser': 'sondensucher',
                      'dbpassword': 'sondensucher',
                      'dbname': 'sonden'}

    with open('dbconfig.ini', 'w') as configfile:
        config.write(configfile)

config.read('dbconfig.ini')
conf = config['DEFAULT']



mydb = mysql.connector.connect(
  host=conf['dbpfad'],
  user=conf['dbuser'],
  password=conf['dbpassword'],
  database=conf['dbname'],
  auth_plugin='mysql_native_password'
)

#Datenbank sonden anlegen
if checkTableExists(mydb,"sonden"):
    print("Datenbank Sonden Existiert")
else:
    print("Datenbank Sonden Existiert nicht")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE sonden(\
        `id` int(11) NOT NULL AUTO_INCREMENT, \
        `sondenid` text NOT NULL, \
        `lat` double NOT NULL, \
        `lon` double NOT NULL, \
        `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
        `hoehe` int NOT NULL, \
        `server` text NOT NULL, \
        `vgeschw` double NOT NULL, \
        `temp` double DEFAULT '0.0' NOT NULL, \
        `freq` text NOT NULL, \
        `richtung` double NOT NULL, \
        `geschw` double NOT NULL, \
        `rssi` double DEFAULT '0.0' NOT NULL, \
        `sondetime` text NOT NULL, \
        `latsucher` double DEFAULT '0.0' NOT NULL, \
        `lonsucher` double DEFAULT '0.0' NOT NULL, \
        `altsucher` double DEFAULT '0.0' NOT NULL, \
        `dirsucher` double DEFAULT '0.0' NOT NULL, \
        PRIMARY KEY (id) \
        )")
    print("Datenbank Sonden wurde erstellt")

#Datenbank sonden anlegen
if checkTableExists(mydb,"hoehen"):
    print("Datenbank Höhen Existiert")
else:
    print("Datenbank Höhen Existiert nicht")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE hoehen(\
        `id` int(11) NOT NULL AUTO_INCREMENT, \
        `lat` double NOT NULL, \
        `lon` double NOT NULL, \
        `hoehe` double NOT NULL, \
        `quelle` text NOT NULL, \
        PRIMARY KEY (id) \
        )")
    print("Datenbank Höhen wurde erstellt")


#Datenbank sonden anlegen
if checkTableExists(mydb,"sonden_stats"):
    print("Datenbank Sonden Statistiken Existiert")
else:
    print("Datenbank Sonden Statistiken Existiert nicht")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE sonden_stats(\
        `id` int(11) NOT NULL AUTO_INCREMENT, \
        `sondenid` text NOT NULL, \
        `startort` text NOT NULL, \
        `max_hoehe` int(11) NOT NULL, \
        `vgeschposD` text NOT NULL, \
        `vgeschnegD` text NOT NULL, \
        `burst` tinyint(1) DEFAULT '0' NOT NULL, \
        `latburst` double DEFAULT '0.0' NOT NULL, \
        `lonburst` double DEFAULT '0.0' NOT NULL, \
        PRIMARY KEY (id) \
        )")
    print("Datenbank Sonden Statistiken wurde erstellt")    