import sys

from mysql.connector.cursor import MySQLCursor
import functions

logger = functions.initlogger("logs/Database.log")

Databaseconf = functions.configDatabase()

def execute(query):
    try:
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mycursor.close()
        mydb.commit()
        logger.info("Datenbank erstellt")
    except:
        print("Unexpected error Datenbank anlegen Database.py:" +
              str(sys.exc_info()))
        logger.error(
            "Unexpected error Datenbank anlegen Database.py:" + str(sys.exc_info()) + "\n" + query)



def checkTableExists(tablename):
    mycursor = mydb.cursor()
    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if mycursor.fetchone()[0] == 1:
        mycursor.close()
        return True
    mycursor.close()
    return False

def sonden():
    # Datenbank anlegen
    if checkTableExists("sonden"):
        logger.info("Datenbank Sonden Existiert")
    else:
        logger.info("Datenbank Sonden Existiert nicht")
        execute(Databaseconf['sonden'])

def hoehen():
    # Datenbank anlegen
    if checkTableExists("hoehen"):
        logger.info("Datenbank Höhen Existiert")
    else:
        logger.info("Datenbank Höhen Existiert nicht")
        execute(Databaseconf['hoehen'])

def statistiken():
    # Datenbank anlegen
    if checkTableExists("sonden_stats"):
        logger.info("Datenbank Sonden Statistiken Existiert")
    else:
        logger.info("Datenbank Sonden Statistiken Existiert nicht")
        execute(Databaseconf['statistiken'])
    
def startorte():
    # Datenbank anlegen
    if checkTableExists("startorte"):
        logger.info("Datenbank Startorte Existiert")
    else:
        logger.info("Datenbank startorte Existiert nicht")
        execute(Databaseconf['startorte'])
        execute(Databaseconf['startorteData'])


def startort_stats():
    # Datenbank anlegen
    if checkTableExists("startort_stats"):
        logger.info("Datenbank Startorte Statistiken Existiert")
    else:
        logger.info("Datenbank Startorte Statistiken Existiert nicht")
        execute(Databaseconf['startort_stats'])

def prediction():
    # Datenbank anlegen
    if checkTableExists("prediction"):
        logger.info("Datenbank Prediction Existiert")
    else:
        logger.info("Datenbank Prediction Existiert nicht")
        execute(Databaseconf['prediction'])

#TODO nach functions exportieren
def löschen(mydb):
    try:
        mycursor = mydb.cursor()
        payload = "SELECT d1.id FROM sonden d1, sonden d2 WHERE d1.id != d2.id AND d1.sondenid = d2.sondenid AND d1.sondetime = d2.sondetime LIMIT 2000 "
        mycursor.execute(payload)
        sonden = mycursor.fetchall()
        for i in sonden:
            payload = "DELETE FROM sonden WHERE id = " + str(i)[1:-2]
            mycursor.execute(payload)
        mydb.commit()
        mycursor.close()
        logger.info("Datensätze gelöscht Anzahl: " + str(len(sonden)))
    except:
        print("Unexpected error Datenbank doppelte Löchen Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error Datenbank doppelte Löschen Database.py:" + str(sys.exc_info()))


if __name__ == '__main__':
    #Datenbanken anlegen
    try:
        mydb = functions.getDataBaseConnection()
        sonden()
        hoehen()
        statistiken()
        startorte()
        startort_stats()
        prediction()
        #Datenbankverbindung Schließen
        mydb.close()
        print("Datenbanken erstellt")
    except:
        print("Unexpected error main Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error main Database.py:" + str(sys.exc_info()))