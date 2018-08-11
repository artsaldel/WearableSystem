import os
import time
import math
import sense_hat_data
import threading

# Wearable configuration variables
raspID = 0
globalFrequency = 1 #Hz
sensorsFrequency = 20 #Hz

# Global variables for information
accelerometerData = ""
magnetometerData = ""
gyroscopeData = ""
neighbors = []

# Read from the flask API
def IsWearableEnabled():
	return True

# Get neighbors using BLE scanner
def SetNeighbors():
	global neighbors
	neighbors = "[1,2,3,4]"

# Get sensors information using sense hat
def SetSensorData():
	global accelerometerData, magnetometerData, gyroscopeData
	
	# Start getting information from sensors
	sense_hat_data.StartSensorsData(sensorsFrequency)
	accelerometerData = sense_hat_data.GetAccelerometerData()
	magnetometerData = sense_hat_data.GetMagnetometerData()
	gyroscopeData = sense_hat_data.GetGyroscopeData()
	sense_hat_data.CleanResults()

# Get audio from microphone
def SetAudio():
	audio = False

# Start the wearable to adquire information
def StartWearable():
	global neighbors, accelerometerData, magnetometerData, gyroscopeData
	
	# Raspberry local time
	localTime = 0

	# Opening the file where the information will be saved
	jsonData = open("output.json","w+")

	while(True):
		if (IsWearableEnabled()):
			# Start getting information from sensors and iBeacons
			SetNeighbors()
			SetSensorData()
			SetAudio()
			
			# Format the information as JSON
			applicationData = '"Neighbors" : %s, "Accelerometer" : [%s], "Magnetometer" : [%s], "Gyroscope" : [%s]' % (str(neighbors), str(accelerometerData), str(magnetometerData), str(gyroscopeData))
			data = '{"Local time" : %d, "Node id" : %d, "Application data" : {%s} }' % (localTime, raspID, applicationData)

			# Save the information into a JSON file
			jsonData.write(data + ",")
		else:
			#Reset everything
			print("Reseting everything")
			jsonData.close() 

		localTime += 1
		time.sleep(1/globalFrequency)

StartWearable()