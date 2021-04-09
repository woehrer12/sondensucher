#https://github.com/rossengeorgiev/aprs-python
#TODO mal schauen was hiermit anfangen
import aprslib

def callback(packet):
    print(packet)

AIS = aprslib.IS("N0CALL")
AIS.connect()
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback, raw=True)