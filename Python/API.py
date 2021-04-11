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
    logger.error("Unexpected error Datenbankverbindung API.py:" + str(sys.exc_info()))


@app.route('/')
def home():
    mycursor.execute("SELECT COUNT(id) FROM `sonden`")
    anzahlsonden = mycursor.fetchone()
    mycursor.execute("SELECT COUNT(id) FROM `hoehen`")
    anzahlhoehen = mycursor.fetchone()
    return flask.render_template('index.html',anzahlsonden = str(anzahlsonden)[1:-2], anzahlhoehen = str(anzahlhoehen)[1:-2])


@app.route('/sonden')
def sonden():
    Liste = functions.sondenids(mydb,30)
    Text = []
    for i in Liste:
        sonde.setid(i)
        Text.append([(i ,"  Startort: " + sonde.getstartort())])
    return flask.render_template('sonden.html',Liste = Liste, Text = Text)

@app.route('/map')
def map():

    return flask.render_template('map.html')        

@app.route('/sonden/id', methods=['GET'])
def sonden_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    logging.info("Sonde abgerufen" + id)

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    sonde.setid(id)
    if sonde.isconfirm():
        return flask.render_template('sondenid.html',   id = sonde.getid(), 
                                                        lat = sonde.getlat(), 
                                                        lon = sonde.getlon(), 
                                                        hoehe = sonde.gethoehe(),
                                                        server = sonde.getserver(),
                                                        vgeschw = sonde.getvgeschw(),
                                                        freq = sonde.getfreq(),
                                                        richtung = sonde.getrichtung(),
                                                        geschw = sonde.getgeschw(),
                                                        time = sonde.getsondentime(),
                                                        vgeschposD = sonde.getvgeschposD(),
                                                        vgeschnegD = sonde.getvgeschnegD(),
                                                        maxhoehe = sonde.getmaxhoehe(),
                                                        startort = sonde.getstartort()
                                                        )
    else:
        return "Keine Sonde mit der ID gefunden"

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.




@app.route('/api/v1/resources/sonden/all', methods=['GET'])
def api_all():
    results = []
    sondenids = functions.sondenids(mydb,30)  #TODO Minuten in Abfrage einbauen
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
                      'startort' : sond.getstartort(),
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
                    'startort' : sonde.getstartort(),
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
