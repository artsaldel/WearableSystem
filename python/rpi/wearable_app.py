import os
import time
import math
import blescan
import threading
import leds_configuration
from sense_hat import SenseHat

# Wearable configuration variables **********************
configuration = []
with open("configuration.conf", "r") as text:
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
localTime = 0

# Updating configuration variables from the API
def SetLocalConfiguration(lock):
	global lectureFrequency, sensorsFrequency, isRpiActive
	while(True):
		configuration = []
		with open("configuration.conf", "r") as text:
		    for line in text:
		    	value = line.split(":")[1].replace("\n","")
		        configuration.append(value)
		raspID = int(configuration[0])
		lectureFrequency = int(configuration[1])
		sensorsFrequency = int(configuration[2])
		isRpiActive = configuration[3]
		time.sleep(0.2)


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
	global lectureFrequency, neighborsData, senseHatData, localTime, isRpiActive
	outputName = "output_node" + str(raspID) + ".json"
	jsonData = open(outputName,"w+")
	while(True):
		if(isRpiActive == "False"):
			leds_configuration.SetLedsNotOk()
		else:
			leds_configuration.SetLedsOk()
			time.sleep(float(1.0/lectureFrequency))
			with lock:
				if(localTime != 0):
					outputData = '{"Local time" : %d, "Node id" : %d, "Application data" : {%s,%s} }' % (localTime, raspID, str(neighborsData), str(senseHatData))
					jsonData.write(outputData + ",")
				localTime += 1

# Declaring all the threads
lock = threading.Lock()
thread0 = threading.Thread(target = SetLocalConfiguration, name = " 0", args=(lock,))
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