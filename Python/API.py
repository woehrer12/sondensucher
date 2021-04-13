# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#implementing-our-api
import flask
import json
from flask import request, jsonify
import mysql.connector
import configparser
import logging
import sys
import functions

from sonden_class import Sonden

sonde = Sonden()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/API.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

app = flask.Flask(__name__)
app.config["DEBUG"] = False
try:
    # Config Datei auslesen
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    conf = config['DEFAULT']
except:
    print("Unexpected error Config lesen API.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Config lesen API.py:" + str(sys.exc_info()))

try:
    # Datenbankverbindung herstellen
    mydb = mysql.connector.connect(
        host=conf['dbpfad'],
        user=conf['dbuser'],
        password=conf['dbpassword'],
        database=conf['dbname'],
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
except:
    print("Unexpected error Datenbankverbindung API.py:" + str(sys.exc_info()))
    logger.error("Unexpected error Datenbankverbindung API.py:" +
                 str(sys.exc_info()))


@app.route('/')
def home():
    mycursor.execute("SELECT COUNT(id) FROM `sonden`")
    anzahlsonden = mycursor.fetchone()
    mycursor.execute("SELECT COUNT(id) FROM `hoehen`")
    anzahlhoehen = mycursor.fetchone()
    mycursor.execute("SELECT COUNT(id) FROM `sonden_stats`")
    anzahlsonden_stats = mycursor.fetchone()
    mycursor.execute("SELECT COUNT(id) FROM `startorte`")
    anzahlstartorte = mycursor.fetchone()
    mycursor.execute("SELECT COUNT(id) FROM `startort_stats`")
    anzahlstartort_stats = mycursor.fetchone()
    return flask.render_template('index.html',  anzahlsonden=str(anzahlsonden)[1:-2],
                                 anzahlhoehen=str(anzahlhoehen)[1:-2],
                                 anzahlsonden_stats=str(
                                     anzahlsonden_stats)[1:-2],
                                 anzahlstartorte=str(anzahlstartorte)[1:-2],
                                 anzahlstartort_stats=str(
                                     anzahlstartort_stats)[1:-2],
                                 )


@app.route('/sonden')
def sonden():
    minute = 30
    if 'min' in request.args:
        minute = int(request.args['min'])
    Liste = []
    Liste = functions.sondenids(mydb, minute)
    Text = []
    for i in Liste:
        sonde.setid(i)
        Text.append([(i, "  Startort: " + sonde.getstartort())])
    return flask.render_template('sonden.html', Liste=Liste, Text=Text)


@app.route('/map')
def map():
    lat = 48.82823584499739
    lon = 9.200133373540973
    latpredict = 48.82823584499739
    lonpredict = 9.200133373540973
    if 'lat' in request.args:
        lat = request.args['lat']
    if 'lon' in request.args:
        lon = request.args['lon']
    if 'latpredict' in request.args:
        latpredict = request.args['latpredict']
    if 'lonpredict' in request.args:
        lonpredict = request.args['lonpredict']

    return flask.render_template('leaflet.html', latsonde=lat, lonsonde=lon, latpredict=latpredict, lonpredict=lonpredict)


@app.route('/sonden/id', methods=['GET'])
def sonden_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
        sonde.setid(id)
        if sonde.isconfirm():
            (latpredict, lonpredict, timepredict) = sonde.prediction_landing()
            return flask.render_template('sondenid.html',   id=sonde.getid(),
                                         lat=sonde.getlat(),
                                         lon=sonde.getlon(),
                                         hoehe=sonde.gethoehe(),
                                         hoeheoverground=(
                                             sonde.gethoehe() - sonde.getgroudhohe()).__round__(2),
                                         server=sonde.getserver(),
                                         vgeschw=sonde.getvgeschw(),
                                         freq=sonde.getfreq(),
                                         richtung=sonde.getrichtung(),
                                         geschw=sonde.getgeschw(),
                                         time=sonde.getsondentime(),
                                         vgeschposD=sonde.getvgeschposD().__round__(2),
                                         vgeschnegD=sonde.getvgeschnegD().__round__(2),
                                         maxhoehe=sonde.getmaxhoehe(),
                                         startort=sonde.getstartort(),
                                         latpredict=latpredict.__round__(2),
                                         lonpredict=lonpredict.__round__(2),
                                         timepredict=timepredict
                                         )

    return "Error: No id field provided. Please specify an id."
    logging.info("Sonde abgerufen" + id)


@app.route('/startorte')
def startorte():
    mycursor.execute(
        "SELECT startort FROM `startort_stats` WHERE anzahl_sonden_72h > 0 ")
    Liste = mycursor.fetchall()
    Text = []
    i = 0
    while i < len(Liste):
        Text.append(str(Liste[i])[2:-3])
        i = i + 1
    return flask.render_template('startorte.html', Liste=Text)


@app.route('/startorte/name', methods=['GET'])
def startorte_name():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'name' in request.args:
        name = request.args['name']
        logging.info("Startort abgerufen" + name)
        mycursor.execute(
            "SELECT * FROM `startort_stats` WHERE startort = '" + name + "' ")
        Liste = mycursor.fetchall()
        Liste = Liste[0]
        name = Liste[1]
        anzahl_sonden_72h = Liste[2]
        vgeschposD = Liste[3]
        vgeschnegD = Liste[4]
        maxhoeheD = Liste[5]

        mycursor.execute(
            "SELECT Lat, Lon FROM `startorte` WHERE name = '" + name + "' ")
        startortlatlon = mycursor.fetchall()
        startortlatlon = startortlatlon[0]
        lat = startortlatlon[0]
        lon = startortlatlon[1]

    else:
        return "Error: No id field provided. Please specify an id."

    return flask.render_template('startortename.html', name=name,
                                 anzahl_sonden_72h=anzahl_sonden_72h,
                                 vgeschposD=vgeschposD,
                                 vgeschnegD=vgeschnegD,
                                 maxhoeheD=maxhoeheD,
                                 lat=lat,
                                 lon=lon)


# API

@app.route('/api/v1/resources/sonden/all', methods=['GET'])
def api_all():
    minute = 30
    if 'min' in request.args:
        minute = int(request.args['min'])
    results = []
    sondenids = functions.sondenids(mydb, minute)
    logging.info("Alle Sonde abgerufen")
    for id in sondenids:
        sonde.setid(id)
        sondejson = [{'id': sonde.getid(),
                      'lat': sonde.getlat(),
                      'lon': sonde.getlon(),
                      'hoehe': sonde.gethoehe(),
                      'server': sonde.getserver(),
                      'vgeschw': sonde.getvgeschw(),
                      'freq': sonde.getfreq(),
                      'richtung': sonde.getrichtung(),
                      'geschw': sonde.getgeschw(),
                      'time': sonde.getsondentime(),
                      'vgeschposD': sonde.getvgeschposD(),
                      'vgeschnegD': sonde.getvgeschnegD(),
                      'maxhoehe': sonde.getmaxhoehe(),
                      'startort': sond.getstartort(),
                      }]
        results = results + sondejson
    return jsonify(results)


@app.route('/api/v1/resources/sonden', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    logging.info("Sonde abgerufen" + id)
    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    sonde.setid(id)
    if sonde.isconfirm():
        results = [{'id': sonde.getid(),
                    'lat': sonde.getlat(),
                    'lon': sonde.getlon(),
                    'hoehe': sonde.gethoehe(),
                    'server': sonde.getserver(),
                    'vgeschw': sonde.getvgeschw(),
                    'freq': sonde.getfreq(),
                    'richtung': sonde.getrichtung(),
                    'geschw': sonde.getgeschw(),
                    'time': sonde.getsondentime(),
                    'vgeschposD': sonde.getvgeschposD(),
                    'vgeschnegD': sonde.getvgeschnegD(),
                    'maxhoehe': sonde.getmaxhoehe(),
                    'startort': sonde.getstartort(),
                    }]
        return jsonify(results)
    else:
        return "Keine Sonde mit der ID gefunden"

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run(host='0.0.0.0', debug=True, port=5000)
