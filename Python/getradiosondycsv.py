import csv 
import requests
import sys
import functions

logger = functions.initlogger("logs/getradiosondy.log")

conf = functions.initconfig()

sondeFrameJson = functions.sondeFrameJson

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
                sondeFrameJson['sondenid'] = sonde[0]
                sondeFrameJson['lat'] = sonde[1]
                sondeFrameJson['lon'] = sonde[2]
                sondeFrameJson['hoehe'] = sonde[3]
                sondeFrameJson['geschw'] = sonde[4]
                sondeFrameJson['vgeschw'] = sonde[5]
                sondeFrameJson['richtung'] = sonde[6]
                sondeFrameJson['freq'] = sonde[7]
                sondeFrameJson['sondetime'] = sonde[8]
                sondeFrameJson['server'] = "radiosondy"
                functions.insertSonde(sondeFrameJson)

    except:
        print("Unexpected error csv.py:" + str(sys.exc_info()))
        logger.error("Unexpected error getradiosondycsv.py:" + str(sys.exc_info()))

if __name__ == '__main__':
    if conf['getradiosondycsv'] == "1":
        csv()
