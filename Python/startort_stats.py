import functions
import sys
import logging
import time


def stats(mydb):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM startorte")
        startorte = mycursor.fetchall()
        now = int(time.time())
        stunden = 72
        minuten = stunden * 60
        sekunden = minuten * 60
        for i in startorte:
            startort = str(i[0])
            # Zähle Sonden von diesem Startort
            query = "SELECT COUNT(startort) FROM `sonden_stats` WHERE `startort` LIKE '" + \
                startort + "' "
            mycursor.execute(query)
            anzahl_sonden_72h = mycursor.fetchall()[0]
            # Durchschnitts Aufstief bestimmen
            query = "SELECT Avg (vgeschposD) FROM `sonden_stats` WHERE startort = '" + \
                startort + "' AND " + \
                    " sondetime>(" + str(now) + " - " + str(sekunden) + ")"
            mycursor.execute(query)
            vgeschposD = mycursor.fetchall()[0]
            # Durchschnitts Fall bestimmen
            query = "SELECT Avg (vgeschnegD) FROM `sonden_stats` WHERE startort = '" + \
                startort + "' AND " + \
                    " sondetime>(" + str(now) + " - " + str(sekunden) + ")"
            mycursor.execute(query)
            vgeschnegD = mycursor.fetchall()[0]
            # Durchschnitts Fall bestimmen
            query = "SELECT Avg (max_hoehe) FROM `sonden_stats` WHERE startort = '" + \
                startort + "' AND " + \
                    " sondetime>(" + str(now) + " - " + str(sekunden) + ")"
            mycursor.execute(query)
            maxhoeheD = mycursor.fetchall()[0]

            if anzahl_sonden_72h[0] != None and vgeschposD[0] != None and vgeschnegD[0] != None and maxhoeheD[0] != None:
                # Prüfen ob schon in Datenbank vorhanden
                query = "SELECT * FROM startort_stats WHERE startort LIKE '" + startort + "'"
                mycursor.execute(query)
                request = mycursor.fetchall()
                if request != []:
                    mycursor.execute("UPDATE startort_stats SET anzahl_sonden_72h = " + str(anzahl_sonden_72h[0]) + ", vgeschposD = '" + str(
                        vgeschposD[0]) + "', vgeschnegD = '" + str(vgeschnegD[0]) + "', maxhoeheD = '" + str(maxhoeheD[0]) + "' WHERE startort = '" + startort + "'")
                    mydb.commit()
                else:
                    payload = "INSERT INTO startort_stats (startort, anzahl_sonden_72h, vgeschposD, vgeschnegD, maxhoeheD) VALUES ('" + startort + "', " + str(
                        anzahl_sonden_72h[0]) + ", " + str(vgeschposD[0]) + "," + str(vgeschnegD[0]) + "," + str(maxhoeheD[0]) + ")"
                    print(payload)
                    mycursor.execute(payload)
                    mydb.commit()

    except:
        print("Unexpected error stats() startort_stats.py:" + str(sys.exc_info()))
        logging.error(
            "Unexpected error stats() startort_stats.py:" + str(sys.exc_info()))
        return None
