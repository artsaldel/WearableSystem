import os
import time
import math
import blescan
import threading
from sense_hat import SenseHat

# Wearable configuration variables **********************
# Change as needed
raspID = 0
globalFrequency = 1 #Hz
sensorsFrequency = 2 #Hz
#********************************************************

# Global variables for information
neighborsData = '"Neighbors" : []'
senseHatData = '"Accelerometer" : [], "Magnetometer" : [], "Gyroscope" : []'

# Raspberry local time
localTime = 0

# Get sensors information using sense hat
def SetSensorData(lock):
	sense = SenseHat();
	sense.set_imu_config(True, True, True)
	while(True):
		global senseHatData
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
	while(True):
		global neighborsData
		neighbors = blescan.GetNearBeacons(globalFrequency)
		neighborsData = '"Neighbors" : [%s]' % (str(neighbors))

# Get audio file using Alsa
def SetAudioData(lock):
	while(True):
		# Execute audio command
		with lock:
			audio = True
		time.sleep(float(1.0/globalFrequency))

# Start the wearable to adquire information
def SetOutput(lock):
	jsonData = open("output.json","w+")
	while(True):
		time.sleep(float(1.0/globalFrequency))
		global neighborsData, senseHatData, localTime
		with lock:
			if(localTime != 0):
				outputData = '{"Local time" : %d, "Node id" : %d, "Application data" : {%s,%s} }' % (localTime, raspID, str(neighborsData), str(senseHatData))
				jsonData.write(outputData + ",")
			localTime += 1

# Declaring all the threads
lock = threading.Lock()
thread1 = threading.Thread(target = SetOutput, name = " 1", args=(lock,))
thread2 = threading.Thread(target = SetSensorData, name = " 2", args=(lock,))
thread3 = threading.Thread(target = SetNeighbors, name = " 3", args=(lock,))
thread4 = threading.Thread(target = SetAudioData, name = " 4", args=(lock,))

# Starting all the threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# Joining all the threads
thread1.join()
thread2.join()
thread3.join()
thread4.join()