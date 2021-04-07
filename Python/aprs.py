#https://github.com/rossengeorgiev/aprs-python
#TODO mal schauen was hiermit anfangen
import aprslib
import logging

logging.basicConfig(level=logging.DEBUG) # level=10

AIS = aprslib.IS("N0CALL")
AIS.connect()
AIS.consumer(lambda x: None, raw=True)