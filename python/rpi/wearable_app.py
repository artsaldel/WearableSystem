import os
import time
import math
import blescan
import threading
import subprocess
import leds_configuration
from sense_hat import SenseHat

# Wearable configuration variables **********************
configuration = []
with open("/home/root/configuration.conf", "r") as text:
    for line in text:
    	value = line.split(":")[1].replace("\n","")
        configuration.append(value)

raspID = int(configuration[0])
lectureFrequency = int(configuration[1])
sensorsFrequency = int(configuration[2])
isRpiActive = configuration[3]
#********************************************************

# Global variables for information
neighborsData = '"Neighbors" : []'
senseHatData = '"Accelerometer" : [], "Magnetometer" : [], "Gyroscope" : []'

# Sense hat initialization
sense = SenseHat();
sense.set_imu_config(True, True, True)

# Raspberry local time
localRead = 0

# Updating configuration variables from the API
def ShowTime(lock):
	while(True):
		localTime = str(subprocess.Popen("date", stdout=subprocess.PIPE, shell=True).communicate()[0].replace("\n","").split(" ")[3].split(":")[2])
		#print(localTime)
		sense.show_message(localTime)
		#time.sleep(1)



# Get sensors information using sense hat
def SetSensorData(lock):
	global senseHatData, sensorsFrequency
	while(True):
		dataAccelerometer = []
		dataMagnetometer = []
		dataGyroscope = []
		for ctdr in range (0, sensorsFrequency):
			dataGyroscope.append(sense.get_gyroscope_raw())
			dataMagnetometer.append(sense.get_compass_raw())
			dataAccelerometer.append(sense.get_accelerometer_raw())
        	time.sleep(float(1.0/sensorsFrequency))
		senseHatData = '"Accelerometer" : [%s], "Magnetometer" : [%s], "Gyroscope" : [%s]' % (str(dataAccelerometer), str(dataMagnetometer), str(dataGyroscope))
		
# Get neighbors using BLE scanner
def SetNeighbors(lock):
	global neighborsData, lectureFrequency
	while(True):
		neighbors = blescan.GetNearBeacons(lectureFrequency)
		neighborsData = '"Neighbors" : [%s]' % (str(neighbors))

# Get audio file using Alsa
def SetAudioData(lock):
	global lectureFrequency
	while(True):
		# Execute audio command
		with lock:
			audio = True
		time.sleep(float(1.0/lectureFrequency))

# Start the wearable to adquire information
def SetOutput(lock):
	global lectureFrequency, neighborsData, senseHatData, localRead, isRpiActive
	outputName = "output_node" + str(raspID) + ".json"
	jsonData = open(outputName,"w+")
	while(True):
		if(isRpiActive == "False"):
			i=0
			#leds_configuration.SetLedsNotOk()
		else:
			#leds_configuration.SetLedsOk()
			time.sleep(float(1.0/lectureFrequency))
			with lock:
				if(localRead != 0):
					localTime = str(subprocess.Popen("date", stdout=subprocess.PIPE, shell=True).communicate()[0].replace("\n",""))
					outputData = '{"Local time" : "%s", "Node id" : %d, "Application data" : {%s,%s} }' % (localTime, raspID, str(neighborsData), str(senseHatData))
					jsonData.write(outputData + ",")
				localRead += 1

# Declaring all the threads
lock = threading.Lock()
thread0 = threading.Thread(target = ShowTime, name = " 0", args=(lock,))
thread1 = threading.Thread(target = SetOutput, name = " 1", args=(lock,))
thread2 = threading.Thread(target = SetSensorData, name = " 2", args=(lock,))
thread3 = threading.Thread(target = SetNeighbors, name = " 3", args=(lock,))
thread4 = threading.Thread(target = SetAudioData, name = " 4", args=(lock,))

# Starting all the threads
thread0.start()
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# Joining all the threads
thread0.join()
thread1.join()
thread2.join()
thread3.join()
thread4.join()