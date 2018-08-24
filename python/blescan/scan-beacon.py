import blescan
import sys
import bluetooth._bluetooth as bluez
import time
import math
import subprocess

print("Starting beacon scanner")
dev_id = 0
sock = bluez.hci_open_dev(dev_id)
blescan.EnableScan(sock)

while True:
    localTime = str(subprocess.Popen("date", stdout=subprocess.PIPE, shell=True).communicate()[0].replace("\n","").split(" ")[3])
    print("------------ Time = " + str(localTime) + " ---------")
    beaconList = blescan.GetNearBeacons(sock, 25)
    for beacon in beaconList:
        minor = beacon.minor
        rssiValue = int(beacon.rssi)
        print("Id : " + str(minor) + ", RSSI : " + str(rssiValue))

