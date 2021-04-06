import sys
import logging
import configparser
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/config.log")
formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)



def config():
    try:
        # Config Datei anlegen und auslesen
        config = configparser.ConfigParser()
        if os.path.isfile("config.ini"):
            ("Config File gefunden")
        else:
            print("Config File angelegt")
            config['DEFAULT'] = {'dbpfad': 'db',
                            'dbuser': 'sondensucher',
                            'dbpassword': 'sondensucher',
                            'dbname': 'sonden'}

            with open('config.ini', 'w') as configfile:
                config.write(configfile)

        config.read('config.ini')
        conf = config['DEFAULT']
    except:
        print("Unexpected error Config anlegen Database.py:" + str(sys.exc_info()))
        logger.error("Unexpected error Config anlegen Database.py:" + str(sys.exc_info()))

config()