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
    beaconList = blescan.GetNearBeacons(sock, 70)
    for beacon in beaconList:
        minor = beacon.minor
        rssiValue = int(beacon.rssi)
        print("Id : " + str(minor) + ", RSSI : " + str(rssiValue) + ", Aproximate distance = " + str(CalculateBeaconDistance(-55, rssiValue)) + "m")
    seconds += 1

