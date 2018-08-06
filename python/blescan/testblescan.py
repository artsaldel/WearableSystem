
import blescan
import sys
import bluetooth._bluetooth as bluez
import time


dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")
except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

seconds = 0
while True:
    print("--- Time = " + str(seconds))
    beaconList = blescan.parse_events(sock, 50)
    for beacon in beaconList:
        macAddress = str(beacon.mac)
        rssiValue = int(beacon.rssi)
        if (rssiValue > -55 and macAddress == "43:45:c0:00:1f:ac"):
            id = beacon.minor
            print(id)
    seconds += 1
    time.sleep(1)