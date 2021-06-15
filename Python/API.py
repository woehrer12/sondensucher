# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#implementing-our-api
import flask
import json
from flask import request, jsonify
import mysql.connector
import configparser
import sys
import functions
import time

logger = functions.initlogger("logs/API.log")

app = flask.Flask(__name__)

@app.route('/')
def home():
    apiStatsJson = functions.APIStats()
    #TODO Übergabe an Template
    return flask.render_template('index.html',  APIStatsJson=apiStatsJson)


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


@app.route('/sonden')
def sonden():
    minute = 30
    if 'min' in request.args:
        minute = int(request.args['min'])
    Liste = []
    Liste = functions.sondenids(minute)
    Text = []
    return flask.render_template('sonden.html', Liste=Liste, Text=Text)


@app.route('/sonden/id', methods=['GET'])
def sonden_id():
    if 'id' in request.args:
        id = request.args['id']
        logger.info("Sonde abgerufen" + id)
        if functions.getSonde(id) == False:
            return "Error: No id field provided. Please specify an id."
        else:
            return flask.render_template('sondenid.html',   data=functions.getSonde(id))

    return "Error: No id field provided. Please specify an id."
    


@app.route('/startorte')
def startorte():
    mydbconnect()
    mycursor.execute(
        "SELECT startort FROM `startort_stats` WHERE anzahl_sonden_72h > 0 ")
    Liste = mycursor.fetchall()
    Text = []
    i = 0
    mydb.close()
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
        mydbconnect()
        name = request.args['name']
        logger.info("Startort abgerufen" + name)
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
        mydb.close()
    else:
        return "Error: No id field provided. Please specify an id."

    return flask.render_template('startortename.html', name=name,
                                 anzahl_sonden_72h=anzahl_sonden_72h,
                                 vgeschposD=vgeschposD,
                                 vgeschnegD=vgeschnegD,
                                 maxhoeheD=maxhoeheD,
                                 lat=lat,
                                 lon=lon)

@app.route('/empfaenger')
def empfaenger():
    mydbconnect()
    Liste = []
    Liste2 = []
    mycursor.execute("SELECT server FROM sonden WHERE lat!='0' AND sondenid <>'' GROUP BY server ")
    Liste = mycursor.fetchall()
    mydb.close()
    for i in Liste:
        Liste2.append(str(i)[2:-3])
    return flask.render_template('empfaenger.html', Liste=Liste2)


@app.route('/empfaenger/name')
def empfaengername():
    if 'name' in request.args:
        mydbconnect()
        name = request.args['name']
        Liste = []
        mycursor.execute("SELECT * FROM `sonden` WHERE server = '" + name + "' ORDER BY `sonden`.`sondetime` DESC LIMIT 100 ")
        Liste = mycursor.fetchall()
        mydb.close()
        return flask.render_template('empfaengername.html', Liste=Liste)
    else:    
        return "Kein Name eigegeben"



# API

@app.route('/api/v1/resources/sonden/all', methods=['GET'])
def api_all():
    minute = 30
    if 'min' in request.args:
        minute = int(request.args['min'])
    results = []
    sondenids = functions.sondenids(minute)
    if sondenids != [] and sondenids != None:
        logger.info("Alle Sonde abgerufen")
        results = functions.getSondelist(sondenids)
        return jsonify(results)
    return "0"

@app.route('/api/v1/resources/sonden/list', methods=['GET'])
def api_list():
    minute = 30
    if 'min' in request.args:
        minute = int(request.args['min'])
    results = []
    sondenids = functions.sondenids(minute)
    if sondenids != [] and sondenids != None:
        results = results + sondenids
        return jsonify(results)
    return "0"


@app.route('/api/v1/resources/sonden', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    logger.info("Sonde abgerufen" + id)
    if functions.getSonde(id) == False:
        return "Keine Sonde mit der ID gefunden"
    else:
        results = functions.getSonde(id)
        return (results)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run(host='0.0.0.0', debug=True, port=5000)
