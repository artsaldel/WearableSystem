agent on 
default-agent
power on
scan on

scp BCM4345C0.hcd root@192.168.0.30:/lib/firmware/brcm
hciattach /dev/ttyAMA0 bcm43xx 115200 noflow -
hciconfig hci0 up
hcitool scan

#iBeacon
python -c 'import sys,uuid;sys.stdout.write(uuid.uuid4().hex);print("")'
python -c 'import sys,uuid;sys.stdout.write(uuid.uuid4().hex)'|pbcopy && pbpaste && echo
sudo hciconfig hci0 up
sudo hciconfig hci0 leadv 3

sudo hciconfig hci0 noscan
#or
sudo hciconfig hci0 piscan

sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 63 6F 3F 8F 64 91 4B EE 95 F7 D8 CC 64 A8 63 B5 00 00 00 00 C8

#Connect
hcitool scan
rfcomm connect 0 70:77:81:76:33:66 10 >/dev/null &
hcitool rssi 70:77:81:76:33:66
watch -n 1 hcitool rssi 70:77:81:76:33:66

#Without pairing
hcitool dev
l2ping -c 2 70:77:81:76:33:66

#init.d
sudo /etc/init.d/bluetooth status
sudo /etc/init.d/bluetooth start

#UUID
blkid


# Dependencies
sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev
sudo apt-get install libical-dev
sudo apt-get install libreadline-dev
sudo apt-get install python-bluez
sudo apt-get install python-pip
sudo pip install bluepy

#WORKINGGGGGGGGGGGGGG
sudo sh start-beacon.sh
sudo python testscan.py


#DEFINITIVE for daemon
hciattach /dev/ttyAMA0 bcm43xx 115200 noflow -
hciconfig hci0 up
hciconfig hci0 leadv 3
hciconfig hci0 noscan
hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 63 6F 3F 8F 64 91 4B EE 95 F7 D8 CC 64 A8 63 B5 00 00 00 00 C8
hcitool -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00
hcitool -i hci0 cmd 0x08 0x000a 01