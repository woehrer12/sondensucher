#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#implementing-our-api
import flask
import json
from flask import request, jsonify
import mysql.connector
import configparser

from sonden_class import Sonden
sonde = Sonden()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Config Datei auslesen
config = configparser.ConfigParser()
config.read('dbconfig.ini')
conf = config['DEFAULT']

#Datenbankverbindung herstellen
mydb = mysql.connector.connect(
    host=conf['dbpfad'],
    user=conf['dbuser'],
    password=conf['dbpassword'],
    database=conf['dbname'],
    auth_plugin='mysql_native_password'
    )
mycursor = mydb.cursor() 

# Create some test data for our catalog in the form of a list of dictionaries.

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Sondensucher API</h1>
<p>Abruf von Sonden in einem bestimmten Zeitraum oder von einer bestimmten ID.</p>'''


@app.route('/api/v1/resources/sonden/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/sonden', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    sonde.setid(id)
    if sonde.isconfirm():
        results = [{'id' :sonde.getid(),
                    'lat' :sonde.getlat(),
                    'lon' :sonde.getlon(),
                    'hoehe' :sonde.gethoehe(),
                    'server' :sonde.getserver(),
                    'vgeschw' :sonde.getvgeschw(),
                    'freq' :sonde.getfreq(),
                    'richtung' :sonde.getrichtung(),
                    'geschw' :sonde.getgeschw(),
                    'time' :sonde.getsondentime(),
                    'vgeschposD' :sonde.getvgeschposD(),
                    'vgeschnegD' :sonde.getvgeschnegD(),
                    'maxhoehe' :sonde.getmaxhoehe()
                    }]
        return jsonify(results)
    else:
         return "Keine Sonde mit der ID gefunden"

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.



app.run()
