###########################################################
# Wearable device - Adquiring non-social signals
# Arturo Salas Delgado
# Collaboration of Tecnologico de Costa Rica and TU Delft
###########################################################

import os
import sys
import struct
import bluetooth._bluetooth as bluez

#Class for iBeacon, for collecting node's id
class Beacon:
    def __init__(self):
        self.mac, self.minor, self.rssi = None, None, None

    def __eq__(self, other):
        return self.mac == other.mac and self.minor == other.minor

    def __repr__(self):
        return '{"Node id": %s, "rssi": %s}' % (str(self.minor), str(self.rssi))

# Int to char function
def ToChar(c, signed=False):
    if type(c) is int:
        return -1 * (256-c) if signed and c > 127 else c
    else:
        return struct.unpack('b' if signed else 'B', c)[0]

# Catching the number of packet and converting to integer
def NumberPacket(packet):
    myInteger = 0
    multiple = 256
    for c in packet:
        myInteger += ToChar(c) * multiple
        multiple = 1
    return myInteger 

# Returning the address in a functional format
def BDAddrToString(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

# Enabling Bluetooth Low Energy transmission
def EnableScan(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01
    bluez.hci_send_cmd(sock, 0x08, 0x000C, struct.pack("<BB", 0x01, 0x00))

# Scan all the Bluettoth Low Energy transmissions
def ScanBeacons(sock, loop_count):
    # Filtering the addresses
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    results = []
    # Looping all the devices
    for i in range(0, loop_count):
        packet = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", packet[:3])
        if(plen == 42):
            if event == 0x3e:
                subevent = ToChar(packet[3])
                packet = packet[4:]
                # Filter by MAC Address
                if(BDAddrToString(packet[3:9]) == "43:45:c0:00:1f:ac"):
                    if subevent == 0x01:
                        le_handle_connection_complete(packet)
                    elif subevent == 0x02:
                        num_reports = ToChar(packet[0])
                        for i in range(0, num_reports):
                            b = Beacon()
                            b.minor = "%i" % NumberPacket(packet[-4:-2])
                            b.mac = BDAddrToString(packet[3:9])
                            b.rssi = "%i" % ToChar(packet[-1], signed=True)
                            # Add the founded devices to the neighbors list
                            if b not in results:
                                results.append(b)
    return results

# Start to scan all the neighbors
def GetNearBeacons(seconds):
    dev_id = 0
    try:
        # Starting beacon scanner
        sock = bluez.hci_open_dev(dev_id)
    except:
        # No access to bluettoth device
        print("No access to bluetooth device")
    EnableScan(sock)
    beaconList = ScanBeacons(sock, seconds * 40)
    return beaconList