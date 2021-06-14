import mysql.connector
import configparser
import logging
import sys




# Datenbankverbindung herstellen
mydb = mysql.connector.connect(
    host='localhost',
    user='sondensucher',
    password='sondensucher',
    database='sonden',
    auth_plugin='mysql_native_password'
)
mycursor = mydb.cursor()


payload = "SELECT d1.id FROM sonden d1, sonden d2 WHERE d1.id != d2.id AND d1.sondenid = d2.sondenid AND d1.sondetime = d2.sondetime LIMIT 2000 "

mycursor.execute(payload)
sonden = mycursor.fetchall()
print(str(sonden[1])[1:-2])

string = ""
for i in sonden:
    payload = "DELETE FROM sonden WHERE id = " + str(i)[1:-2]
    print(payload)
    mycursor.execute(payload)
mydb.commit()
logging.info("Datensätze gelöscht Anzahl: " + len(sonden))
