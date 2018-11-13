###########################################################
# Wearable device - Adquiring non-social signals
# Arturo Salas Delgado
# Collaboration of Tecnologico de Costa Rica and TU Delft
###########################################################

from datetime import datetime
import time

configuration = []
with open("/home/root/configuration.conf", "r") as text:
    for line in text:
    	if(line != "\n" and ("#" not in line)):
	        value = line.split(":")[1].replace("\n","")
	        configuration.append(value)
# Initiating global configuration variables
raspID = int(configuration[0])
while(True):
	time.sleep(1)
	print('Node %d = %s UTC' % (raspID, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
