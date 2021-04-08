import sys
import logging
import configparser
import os

def config():
    try:
        # Config Datei anlegen und auslesen
        config = configparser.ConfigParser()
        if os.path.isfile("config/config.ini"):
            ("Config File gefunden")
        else:
            print("Config File angelegt")
            config['DEFAULT'] = {
                            'dbpfad': 'db',
                            'dbuser': 'sondensucher',
                            'dbpassword': 'sondensucher',
                            'dbname': 'sonden',
                            #Deaktivierbare Teile
                            'getradiosondycsv': '1',
                            'getsondehub': '1',
                            'gethoehen': '1',
                            'mqtt-sondensucher.de': '1',
                            'API': '1',
                            }

            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)

        config.read('config/config.ini')
        conf = config['DEFAULT']
    except:
        print("Unexpected error Config anlegen Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error Config anlegen Database.py:" + str(sys.exc_info()))
