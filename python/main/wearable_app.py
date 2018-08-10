import os
import time
import math
import sense_hat_data

raspID = 0
globalFrequency = 1 #Hz
sensorsFrequency = 20 #Hz

# Read from the flask API
def ReadStart():
	return True

def GetNeighbors():
	return "[1,4,5]"

def StartSensors():
	sense_hat_data.StartSensorsData(sensorsFrequency)

def CleanSensorsData():
	sense_hat_data.CleanResults()

def GetAccelerometer():
	return sense_hat_data.GetAccelerometerData()

def GetMagnetometer():
	return sense_hat_data.GetMagnetometerData()

def GetGyroscope():
	return sense_hat_data.GetGyroscopeData()

def GetAudio():
	return False

# Raspberry local time
localTime = 0

# Opening the file where the information will be saved
jsonData = open("output.json","w+")

while(True):
	if (ReadStart()):
		# Start getting information from sensors
		StartSensors()
		neighbors = GetNeighbors()
		accelerometerData = GetAccelerometer()
		magnetometerData = GetMagnetometer()
		gyroscopeData = GetGyroscope()
		CleanSensorsData()
		
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