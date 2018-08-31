import os
import time
import math
import blescan
import threading
import subprocess
from datetime import datetime
from sense_hat import SenseHat

# Global variables
global raspID, lectureFrequency,sensorsFrequency, sensorsFrequency
global neighborsData, senseHatData, sense


# Updating configuration variables from the API
def ShowId(lock):
	while(True):
		localTime = str(datetime.now()).replace(".",":")[:-3]
		#print(localTime)
		sense.show_message(str(raspID))
		#time.sleep(1)

# Get sensors information using sense hat
def SetSensorData(lock):
	global lectureFrequency, sensorsFrequency, neighborsData, senseHatData, localRead, isRpiActive
	outputName = "/home/root/output_node" + str(raspID) + ".json"
	jsonData = open(outputName,"w+")
	outputData = ""
	localCtdr = 0
	folderAudioName = "/home/root/audio_node" + str(raspID) + "/" +str(datetime.now()).replace(" ","_")[:-7].replace(":","-")
	subprocess.Popen('mkdir %s' % ("/home/root/audio_node" + str(raspID)), stdout=subprocess.PIPE, shell=True)
	subprocess.Popen('mkdir %s' % (folderAudioName), stdout=subprocess.PIPE, shell=True)
	while(True):
		dataTime = []
		dataAccelerometer = []
		dataMagnetometer = []
		dataGyroscope = []
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		for ctdr in range (1, sensorsFrequency + 1):
			while( not( int((ctdr - 1)*(1000.0/sensorsFrequency)) <= localMiliseconds < int(ctdr*(1000.0/sensorsFrequency)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			localTime = str(datetime.now()).replace(".",":")[:-3]
			if(ctdr == 1):
				#arecord -D plughw:1,0 -d 5 -f S16_LE -c1 -r16000 --disable-softvol ~/audio/test.wav
				command = 'arecord -D plughw:1,0 -f S16_LE -c1 -r16000 --disable-softvol -d %s %s/%s.wav' % (str(lectureFrequency), folderAudioName, str(localTime).replace(" ", "_").replace(":","-"))
				subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
				print(command)
			dataTime.append(localTime)
			dataGyroscope.append(sense.get_gyroscope_raw())
			dataMagnetometer.append(sense.get_compass_raw())
			dataAccelerometer.append(sense.get_accelerometer_raw())
			senseHatData = '"Accelerometer" : [%s],\n"Magnetometer" : [%s],\n"Gyroscope" : [%s]\n' % (str(dataAccelerometer), str(dataMagnetometer), str(dataGyroscope))
		outputData += '{\n"Local time" : "%s",\n"Node id" : %d,\n"Application data" : {\n%s,\n%s}\n},\n' % (str(dataTime[0]), raspID, str(neighborsData), str(senseHatData))
		localCtdr += 1
		if (localCtdr == 5):
			jsonData.write(outputData)
			localCtdr = 0
			outputData = ""

		
# Get neighbors using BLE scanner
def SetNeighbors(lock):
	global neighborsData, lectureFrequency
	while(True):
		neighbors = blescan.GetNearBeacons(lectureFrequency)
		neighborsData = '"Neighbors" : [%s]' % (str(neighbors))

# Main of the application
if __name__ == '__main__':
	# Global variables
	global raspID, lectureFrequency,sensorsFrequency, sensorsFrequency
	global neighborsData, senseHatData, sense
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
	isRpiActive = configuration[3]

	# Running command for enabling audio
	try:
		subprocess.Popen('amixer -c1 sset "Mic" 100%+', stdout=subprocess.PIPE, shell=True)
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