import functions
import requests
import sys
import time

logger = functions.initlogger("logs/getaprs.log")

conf = functions.initconfig()

sondeFrameJson = functions.sondeFrameJson

#Header fälschen
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}
conf['aprsAPIkey']

#https://api.aprs.fi/api/get?name=OH7RDA,OH7AA&what=loc&apikey=APIKEY&format=json
urlfront = "https://api.aprs.fi/api/get?name="
urlend = "&what=loc&apikey=" + conf['aprsAPIkey'] + "&format=json"

#TODO alle mit Typ Balloon


def getwithids():
    try:
        ids = functions.sondenids(60)
        idsstring = ""
        for i in ids:
            idsstring = idsstring + str(i) + ","
        url = urlfront + idsstring + urlend
        print(url)
        response = requests.get(url,headers=headers,  timeout=60)
        if response.status_code == 200:
            rjson = response.json()
            for i in rjson['entries']:
                print(i['name'])
                comment = i['comment']
                print(comment[comment.find("40"):comment.find("MHz")])
                sondeFrameJson['sondenid'] = i['name']
                sondeFrameJson['lat'] = i['lat']
                sondeFrameJson['lon'] = i['lng']
                sondeFrameJson['hoehe'] = str(int(i['altitude']))
                sondeFrameJson['geschw'] = str(i['speed'])
                sondeFrameJson['vgeschw'] = comment[comment.find("Clb=")+4:comment.find("m/s")]
                sondeFrameJson['richtung'] = str(i['course'])
                sondeFrameJson['freq'] = str(comment[comment.find("40"):comment.find("MHz")])
                sondeFrameJson['sondetime'] = i['lasttime']
                sondeFrameJson['server'] = "aprs.fi"
                sondeFrameJson['empfaenger'] = i['srccall']
                #TODO Type, Temperatur, batt, 
                functions.insertSonde(sondeFrameJson)


        logger.info("APRS API abgerufen")

    except:
        print("Unexpected error getaprs.py:" + str(sys.exc_info()))
        logger.error("Unexpected error getaprs.py:" + str(sys.exc_info()))

if __name__ == '__main__':
    while True:
        if conf['getAPRS'] == "1":
            getwithids()
        time.sleep(int(conf['aprsRequestTime']))
    getwithids()