import sys
import configparser
import os
import functions


logger = functions.initlogger("logs/config.log")

config_version = '1.2'


def create(config):
    logger.info("Config File angelegt")
    config['DEFAULT'] = {
        'dbpfad': 'db',
        'dbuser': 'sondensucher',
        'dbpassword': 'sondensucher',
        'dbname': 'sonden',
        'config_version': config_version,
        # Deaktivierbare Teile
        'getradiosondycsv': '1',
        'getsondehub': '0',
        'gethoehen': '1',
        'mqtt-sondensucher.de': '1',
        'API': '1',
        'server' : '1',
        'serverip' : 'sondensucher.de',
        'wind' : '0',
        'prediction' : '1',
        'aprsAPIkey' : ''
    }

    with open('config/config.ini', 'w') as configfile:
        config.write(configfile)


def config():
    try:

        # Config Datei anlegen und auslesen
        config = configparser.ConfigParser()
        if os.path.isfile("config/config.ini"):
            ("Config File gefunden")
            config.read('config/config.ini')
            conf = config['DEFAULT']
            if conf['config_version'] != config_version:
                os.remove("config/config.ini")
                logger.info("Config gelöscht")
                create(config)
            else:
                logger.info("Config Version ok")
        else:
            create(config)

        config.read('config/config.ini')
        conf = config['DEFAULT']
    except:
        print("Unexpected error Config anlegen Database.py:" + str(sys.exc_info()))
        logger.error(
            "Unexpected error Config anlegen Database.py:" + str(sys.exc_info()))

if __name__ == '__main__':
    config()