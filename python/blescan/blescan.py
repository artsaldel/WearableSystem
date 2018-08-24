import os
import sys
import struct
import bluetooth._bluetooth as bluez

class Beacon:
    def __init__(self):
        self.mac, self.minor, self.rssi = None, None, None

    def __eq__(self, other):
        return self.mac == other.mac and self.minor == other.minor

    def __repr__(self):
        return 'minor: {}; mac: {}; rssi: {}'.format(self.minor, self.mac, self.rssi)

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

def BDAddrToString(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def EnableScan(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01
    bluez.hci_send_cmd(sock, 0x08, 0x000C, struct.pack("<BB", 0x01, 0x00))

def GetNearBeacons(sock, loop_count):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    results = []
    for i in range(0, loop_count):
        packet = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", packet[:3])
        
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI: i = 0
        elif event == bluez.EVT_NUM_COMP_PKTS: i = 0 
        elif event == bluez.EVT_DISCONN_COMPLETE: i = 0 
        if event == 0x3e:
            subevent = ToChar(packet[3])
            packet = packet[4:]
            if subevent == 0x01:
                le_handle_connection_complete(packet)
            elif subevent == 0x02:
                num_reports = ToChar(packet[0])
                report_packet_offset = 0
                for i in range(0, num_reports):
                    b = Beacon()
                    b.minor = "%i" % NumberPacket(packet[report_packet_offset -4: report_packet_offset - 2])
                    b.mac = BDAddrToString(packet[report_packet_offset + 3:report_packet_offset + 9])
                    b.rssi = "%i" % ToChar(packet[report_packet_offset -1], signed=True)
                    if (b.mac == "43:45:c0:00:1f:ac"):
                        if b not in results:
                            results.append(b)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return results