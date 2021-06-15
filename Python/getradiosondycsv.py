import csv 
import requests
import sys
import functions
import time

logger = functions.initlogger("logs/getradiosondy.log")

conf = functions.initconfig()

Sondeframjson = functions.Sondeframjson

#Header fälschen
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

url = "https://radiosondy.info/export/csv_live.php"

#sondenid; lat; lon; hoehe; geschw; vgeschw; richtung; freq; sondetime

def csv():
    try:
        httpx = requests.get(url, headers=headers)

        antwort = httpx.text
        
        logger.info("Radiosondy CSV abgerufen")

        for line in antwort.split('\n'):
            sonde = []
            if len(line) != 0:
                for line in line.split(';'):
                    if len(line) == 0:
                        line = "0"
                    sonde.append(line)
                #Datenbank eintragen
                Sondeframjson['sondenid'] = sonde[0]
                Sondeframjson['lat'] = sonde[1]
                Sondeframjson['lon'] = sonde[2]
                Sondeframjson['hoehe'] = sonde[3]
                Sondeframjson['geschw'] = sonde[4]
                Sondeframjson['vgeschw'] = sonde[5]
                Sondeframjson['richtung'] = sonde[6]
                Sondeframjson['freq'] = sonde[7]
                Sondeframjson['sondetime'] = sonde[8]
                Sondeframjson['server'] = "radiosondy"
                functions.insertSonde(Sondeframjson)

    except:
        print("Unexpected error csv.py:" + str(sys.exc_info()))
        logger.error("Unexpected error getradiosondycsv.py:" + str(sys.exc_info()))

if __name__ == '__main__':
    while True:
        if conf['getradiosondycsv'] == "1":
            csv()
        time.sleep(60)
