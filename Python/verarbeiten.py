import mysql.connector
import configparser
import functions
import logging
import sys

from sonden_class import Sonden

sonde = Sonden()

def sonden(mydb):
  try:
    sondenids = functions.sondenids(mydb, 30)
    anzahlids = len(sondenids)
    j = 0
    logging.info("verarbeiten.py")   

    while j <anzahlids:
        sonde.setid(sondenids[j])
        sonde.set_stats()
        buffer = sonde.getgroudhohe()
        if sonde.startort() == "unbekannt":
          sonde.updatestartort()
        j = j + 1
  except:
        print("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        logging.error("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        return None

