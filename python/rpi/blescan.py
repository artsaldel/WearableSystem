import os
import sys
import time
import math
import struct
import bluetooth._bluetooth as bluez

LE_META_EVENT = 0x3e
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_ENABLE=0x000C
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
TX_POWER=-50
MAC_ADDR_FILTER="43:45:c0:00:1f:ac"


class Beacon:
    def __init__(self):
        self.uuid, self.major, self.minor = None, None, None
        self.mac, self.unknown, self.rssi = None, None, None
    
    def __eq__(self, other):
        return self.mac == other.mac and self.uuid == other.uuid and self.major == other.major and self.minor == other.minor
    
    def __hash__(self): 
        return hash('{}{}{}{}'.format(self.mac, self.uuid, self.major, self.minor))
    
    def __repr__(self):
        return '{"Node id": %s, "RSSI": %s}' % (str(self.minor), str(self.rssi))

def ToChar(c, signed=False):
    if type(c) is int:
        return -1 * (256-c) if signed and c > 127 else c
    else:
        return struct.unpack('b' if signed else 'B', c)[0]

def NumberPacket(packet):
    myInteger = 0
    multiple = 256
    for c in packet:
        myInteger += ToChar(c) * multiple
        multiple = 1
    return myInteger 

def StringPacket(packet):
    myString = "";
    for c in packet:
        myString +=  "%02x" % ToChar(c)
    return myString 

def BDAddrToString(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def EnableScan(sock):
    ToggleScan(sock, 0x01)

def DisableScan(sock):
    ToggleScan(sock, 0x00)

def ToggleScan(sock, enable):
    cmd_packet = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_packet)

def SetScanParameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01

def ScanBeacons(sock, ctdr):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    results = []
    for i in range(0, ctdr):
        packet = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", packet[:3])
        
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI: i = 0
        elif event == bluez.EVT_NUM_COMP_PKTS: i = 0 
        elif event == bluez.EVT_DISCONN_COMPLETE: i = 0 
        if event == LE_META_EVENT:
            subevent = ToChar(packet[3])
            packet = packet[4:]
            if subevent == EVT_LE_CONN_COMPLETE:
                le_handle_connection_complete(packet)
            elif subevent == EVT_LE_ADVERTISING_REPORT:
                num_reports = ToChar(packet[0])
                report_packet_offset = 0
                for i in range(0, num_reports):
                    b = Beacon()
                    uuid = StringPacket(packet[report_packet_offset -22: report_packet_offset - 6]).upper()
                    b.uuid = '{}-{}-{}-{}-{}'.format(uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:])
                    b.major = "%i" % NumberPacket(packet[report_packet_offset -6: report_packet_offset - 4])
                    b.minor = "%i" % NumberPacket(packet[report_packet_offset -4: report_packet_offset - 2])
                    b.mac = BDAddrToString(packet[report_packet_offset + 3:report_packet_offset + 9])
                    b.unknown = "%i" % ToChar(packet[report_packet_offset -2], signed=True)
                    b.rssi = "%i" % ToChar(packet[report_packet_offset -1], signed=True)
                    if (b.mac == MAC_ADDR_FILTER):
                        if b in results:
                            ob = results[results.index(b)]
                            ob.unknown = b.unknown
                            ob.rssi = b.rssi
                        else:
                            results.append(b)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return results

def GetNearBeacons(seconds):
    dev_id = 0
    try:
        # Starting beacon scanner
        sock = bluez.hci_open_dev(dev_id)
    except:
        # No access to bluettoth device
        sys.exit(1)
    SetScanParameters(sock)
    EnableScan(sock)
    results = []
    beaconList = ScanBeacons(sock, seconds * 50)
    return beaconList