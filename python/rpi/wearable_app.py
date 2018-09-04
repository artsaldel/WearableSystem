import os
import time
import math
import blescan
import threading
import subprocess
from datetime import datetime
from sense_hat import SenseHat

# Global variables
global raspID, lectureFrequency, sensorsFrequency
global neighborsData, senseHatData, sense
global folderAudioName, jsonFile, soundCardNumber

# Initiate the outpit file in order to start witing information into it
def PrepareOutput():
	global raspID, jsonFile
	outputName = '/home/root/output_node%s.json' % (str(raspID))
	jsonFile = open(outputName,"w+")

# Creates a new folder for saving audio ouput files
def PrepareAudio():
	global folderAudioName
	folderAudioName = '/home/root/audio_node%s/%s' % (str(raspID), str(datetime.now()).replace(" ","_")[:-7].replace(":","-"))
	subprocess.Popen('mkdir %s' % ("/home/root/audio_node" + str(raspID)), stdout=subprocess.PIPE, shell=True)
	subprocess.Popen('mkdir %s' % (folderAudioName), stdout=subprocess.PIPE, shell=True)

def RecordAudio(localTime):
	global lectureFrequency, folderAudioName
	fileName = str(localTime).replace(" ", "_").replace(":","-")
	command = 'arecord -D plughw:0,0 -f S16_LE -c1 -r16000 --disable-softvol -d %s %s/%s.wav' % (str(lectureFrequency), folderAudioName, fileName)
	subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

def GetTimeDrift():
	drift = ""
	with open("/var/lib/ntp/ntp.drift", "r") as text:
	    for line in text:
	        drift = line.replace("\n","")
	driftPerSecond = '%s ppm' % (str(drift))
	return driftPerSecond

# Get sensors information using sense hat
def SetSensorData(lock):
	global lectureFrequency, sensorsFrequency, neighborsData
	global senseHatData, localRead, folderAudioName, jsonFile
	# Preparing audio and json files
	PrepareOutput()
	PrepareAudio()
	# Local variables
	outputData = ""
	localCtdr = 0
	#Start adquiring information
	while(True):
		dataTime = []
		dataAccelerometer = []
		dataMagnetometer = []
		dataGyroscope = []
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])

		# Catching audio and sensors data
		for ctdr in range (1, sensorsFrequency + 1):
			#Wait til a second pass
			while( not( int((ctdr - 1)*(1000.0/sensorsFrequency)) <= localMiliseconds < int(ctdr*(1000.0/sensorsFrequency)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass

			# Reading time
			localTime = str(datetime.now()).replace(".",":")[:-3]
			if(ctdr == 1):
				RecordAudio(localTime)

			# Collecting data from the sensors
			dataTime.append(localTime)
			dataGyroscope.append(sense.get_gyroscope_raw())
			dataMagnetometer.append(sense.get_compass_raw())
			dataAccelerometer.append(sense.get_accelerometer_raw())

		# Time drift against NTP server
		timeDrift = GetTimeDrift()

		# Save the information as JSON format
		senseHatData = '"Read time": [%s],\n"Accelerometer" : [%s],\n"Magnetometer" : [%s],\n"Gyroscope" : [%s]\n' % (str(dataTime), str(dataAccelerometer), str(dataMagnetometer), str(dataGyroscope))
		outputData += '{\n"Local time" : "%s",\n"Node id" : %d,\n"NTP time drift" : "%s",\n"Application data" : {\n%s,\n%s}\n},\n' % (str(dataTime[0]), raspID, timeDrift, str(neighborsData), str(senseHatData))
		
		# Write the information into the JSON file every 5 seconds
		localCtdr += 1
		if (localCtdr == 5):
			jsonFile.write(outputData)
			localCtdr = 0
			outputData = ""

# Get neighbors using BLE scanner
def SetNeighbors(lock):
	global neighborsData, lectureFrequency
	while(True):
		neighbors = blescan.GetNearBeacons(lectureFrequency)
		neighborsData = '"Neighbors" : [%s]' % (str(neighbors))

# Updating configuration variables from the API
def ShowId(lock):
	while(True):
		sense.show_message(str(raspID))

# Main of the application
if __name__ == '__main__':
	# Global variables
	global raspID, lectureFrequency,sensorsFrequency, sensorsFrequency
	global neighborsData, senseHatData, sense, soundCardNumber

	# Wearable configuration variables **********************
	configuration = []
	with open("/home/root/configuration.conf", "r") as text:
	    for line in text:
	        value = line.split(":")[1].replace("\n","")
	        configuration.append(value)

	# Initiating global configuration variables
	raspID = int(configuration[0])
	lectureFrequency = int(configuration[1])
	sensorsFrequency = int(configuration[2])
	soundCardNumber = int(configuration[3])
	# Running command for enabling audio
	try:
		command = "amixer -c" + str(soundCardNumber) + ' sset "Mic" 100%+'
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	except:
		print("No microphone available")
	#********************************************************

	# Global variables for information
	neighborsData = '"Neighbors" : []'
	senseHatData = '"Time" : [], "Accelerometer" : [], "Magnetometer" : [], "Gyroscope" : []'

	# Sense hat initialization
	sense = SenseHat();
	sense.set_imu_config(True, True, True)

	# Declaring all the threads
	lock = threading.Lock()
	thread0 = threading.Thread(target = ShowId, name = " 0", args=(lock,))
	thread1 = threading.Thread(target = SetSensorData, name = " 1", args=(lock,))
	thread2 = threading.Thread(target = SetNeighbors, name = " 2", args=(lock,))

	# Starting all the threads
	thread0.start()
	thread1.start()
	thread2.start()

	# Joining all the threads
	thread0.join()
	thread1.join()
	thread2.join()