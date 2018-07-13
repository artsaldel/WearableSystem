from sense_hat import SenseHat
import blescan
import sys
import bluetooth._bluetooth as bluez

sense = SenseHat()
sense.low_light = True

red = (255, 0, 0)
green = (0, 255, 0)
nothing = (0,0,0)

def figureOk():
    G = green
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O, 
    O, O, O, G, G, O, O, O, 
    O, O, G, G, G, G, O, O, 
    O, G, G, G, G, G, G, O, 
    O, G, G, G, G, G, G, O, 
    O, O, G, G, G, G, O, O, 
    O, O, O, G, G, O, O, O, 
    O, O, O, O, O, O, O, O, 
    ]
    return logo
    
    
def figureError():
    R = red
    O = nothing
    logo = [
    R, R, O, O, O, O, R, R,
    R, R, R, O, O, R, R, R,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, R, R, R, R, O, O,
    O, R, R, R, R, R, R, O,
    R, R, R, O, O, R, R, R,
    R, R, O, O, O, O, R, R
    ]
    return logo

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")
except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    returnedList = blescan.parse_events(sock, 1)
    print("----------")
    for beacon in returnedList:
        #print(beacon)
	print("mac: " + beacon.mac)
	print("rssi: " + beacon.rssi)
	rssiValue = int(beacon.rssi)
	if (rssiValue > -55):
		print("Cerca")
		sense.set_pixels(figureOk())
	else:
		print("Lejos")
		sense.set_pixels(figureError())