###########################################################
# Wearable device - Adquiring non-social signals
# Arturo Salas Delgado
# Collaboration of Tecnologico de Costa Rica and TU Delft
###########################################################

import subprocess

# Set of terminal commands for starting the Bluetooth Low Energy transmission
def StartTransmission(raspID):
	subprocess.call("hciattach /dev/ttyAMA0 bcm43xx 115200 noflow -", shell=True)
	subprocess.call("hciconfig hci0 up", shell=True)
	subprocess.call("hciconfig hci0 leadv 3", shell=True)
	subprocess.call("hciconfig hci0 noscan", shell=True)
	hexID = str(hex(raspID).split('x')[-1]).zfill(4)
	commandBeacon = 'hcitool -i hci0 cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 %s %s c5 00 00 00 00 00 00 00 00 00 00 00 00 00' % (hexID[:2], hexID[2:])
	subprocess.call(commandBeacon, shell=True)
	# "40 01 40 01" for changing the transmission rate. How to on https://goo.gl/BYwCdX
	subprocess.call("hcitool -i hci0 cmd 0x08 0x0006 40 01 40 01 03 00 00 00 00 00 00 00 00 07 00", shell=True)
	subprocess.call("hcitool -i hci0 cmd 0x08 0x000a 01", shell=True)