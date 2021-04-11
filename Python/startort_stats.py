import functions

def stats(mydb):
  try:
    mycursor = mydb.cursor() 
    mycursor.execute("SELECT name FROM startorte")
    startorte = mycursor.fetchall()
    for i in startorte:
        mycursor.execute("SELECT COUNT(startort) FROM `sonden_stats` WHERE `startort` LIKE '" + i + "' ")
        anzahl = mycursor.fetchall()
        print(anzahl)

#TODO hier weiter machen
  except:
        print("Unexpected error stats() startort_stats.py:" + str(sys.exc_info()))
        logging.error("Unexpected error stats() startort_stats.py:" + str(sys.exc_info()))
        return None
