import mysql.connector
import configparser
import functions
import logging
import sys

from sonden_class import Sonden

sonde = Sonden()

def sonden(mydb):
  try:
    sondenids = functions.sondenids(mydb)
    anzahlids = len(sondenids)
    j = 0


    

    while j <anzahlids:
        sonde.setid(sondenids[j])
        #print(sonde.getgroudhohe())
        #print(type(sonde.getgroudhohe()))
        j = j + 1
  except:
        print("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        logging.error("Unexpected error sonden() verarbeiten.py:" + str(sys.exc_info()))
        return None

