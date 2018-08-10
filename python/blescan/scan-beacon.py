import blescan
import sys
import bluetooth._bluetooth as bluez
import time
import math

def CalculateBeaconDistance(txPower, rssi):
    ratio_db = float(txPower - rssi)
    ratio_linear = float(math.pow(10, float(ratio_db/10)))
    distance = float(math.sqrt(ratio_linear))
    return distance


dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("Starting beacon scanner")
except:
    print("Error: no access to bluetooth device")
    sys.exit(1)

blescan.SetScanParameters(sock)
blescan.EnableScan(sock)

seconds = 0
while True:
    print("------------ Time = " + str(seconds) + " ---------")
    beaconList = blescan.GetNearBeacons(sock, 50)
    for beacon in beaconList:
        macAddress = str(beacon.mac)
        rssiValue = int(beacon.rssi)
        id = beacon.minor
        near = True
        if (CalculateBeaconDistance(-45, rssiValue) > 2.0):
            near = False
        print(id + "->" + str(rssiValue) + " --- Cerca = " + str(near))
    seconds += 1

