###########################################################
# Wearable device - Adquiring non-social signals
# Arturo Salas Delgado
# Collaboration of Tecnologico de Costa Rica and TU Delft
###########################################################

import time
import blescan
import subprocess
import bletransmit
import multiprocessing
from sensors import Sensors
from datetime import datetime
from sense_hat import SenseHat

# Global variables
global raspID
global folderAudioName, folderJsonName, jsonFile
global accelSampleRate, gyroSampleRate, magnSampleRate

# Running commands for starting one second audio
def RecordAudio(localTime):
	global folderAudioName
	seconds = 1
	fileName = str(localTime).replace(" ", "_").replace(":","-")
	command = 'arecord -f S16_LE -c1 -r16000 -d %s %s/%s.wav' % (str(seconds), folderAudioName, fileName)
	subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

# Getting the time drift from the NTP drift file
def GetTimeDrift():
	drift = ""
	with open("/var/lib/ntp/ntp.drift", "r") as text:
	    for line in text:
	        drift = line.replace("\n","")
	driftPerSecond = '%s ppm' % (str(drift))
	return driftPerSecond

# Setting data from accelerometer
def SetAccelerometerData(dataAccelerometer):
	global accelSampleRate
	sensorCollector = Sensors(accelSampleRate, magnSampleRate)
	rate = sensorCollector.GetAccelGyroFreqByValue(accelSampleRate)
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		# Wait til a second pass
		for ctdr in range (1, int(rate + 1)):
			# Collect information from accelerometer
			while( not( int((ctdr - 1)*(1000.0/rate)) <= localMiliseconds < int(ctdr*(1000.0/rate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			if(ctdr == 1):
				del dataAccelerometer[:]
			dataAccelerometer.append(sensorCollector.ReadAccelerometer())

# Setting data from gyroscope
def SetGyroscopeData(dataGyroscope):
	global gyroSampleRate
	sensorCollector = Sensors(gyroSampleRate, magnSampleRate)
	rate = sensorCollector.GetAccelGyroFreqByValue(gyroSampleRate)
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		# Wait til a second pass
		for ctdr in range (1, int(rate + 1)):
			# Collect information from gyroscope
			while( not( int((ctdr - 1)*(1000.0/rate)) <= localMiliseconds < int(ctdr*(1000.0/rate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			if(ctdr == 1):
				del dataGyroscope[:]
			dataGyroscope.append(sensorCollector.ReadGyroscope())

# Setting data from magnetometer
def SetMagnetometerData(dataMagnetometer):
	global magnSampleRate
	sensorCollector = Sensors(accelSampleRate, magnSampleRate)
	rate = sensorCollector.GetMagnByValue(magnSampleRate)
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		# Wait til a second pass
		for ctdr in range (1, int(rate + 1)):
			# Collect information from magnetometer
			while( not( int((ctdr - 1)*(1000.0/rate)) <= localMiliseconds < int(ctdr*(1000.0/rate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			if(ctdr == 1):
				del dataMagnetometer[:]
			dataMagnetometer.append(sensorCollector.ReadMagnetometer())

# Get sensors information using sense hat
def SetSensorData(dataNeighbors, dataAccelerometer, dataGyroscope, dataMagnetometer):
	global folderJsonName, jsonFile
	# Local variables
	outputData = "["
	localCtdr = 0
	globalCtdr = 1
	localSample = 50
	#Start adquiring information
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		firstTime = str(datetime.now()).replace(".",":")[:-3]

		# Catching audio and sensors data
		for ctdr in range (1, localSample):
			#Wait til a second pass
			while( not( int((ctdr - 1)*(1000.0/localSample)) <= localMiliseconds < int(ctdr*(1000.0/localSample)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			# Time for saving lecture
			if(ctdr == 1):
				firstTime = str(datetime.now()).replace(".",":")[:-3] + " UTC"
		if(globalCtdr > 2):
			# Time drift against NTP server
			timeDrift = GetTimeDrift()
			# Save the information as JSON format
			senseHatData = '"Accelerometer" : [%s],\n"Gyroscope" : [%s],\n"Magnetometer" : [%s]' % (str(dataAccelerometer).replace("'",""), str(dataGyroscope).replace("'",""), str(dataMagnetometer).replace("'",""))
			outputData += '{\n"Local time" : "%s",\n"Node id" : %d,\n"NTP time drift" : "%s",\n"Application data" : {\n%s,\n%s}\n},\n\n\n' % (firstTime, raspID, timeDrift, str(dataNeighbors['neighbors']), str(senseHatData))
			# Cleaning data
			dataAccelerometer[:] = [] 
			dataGyroscope[:] = [] 
			dataMagnetometer[:] = [] 
			# Write the information into the JSON file every 5 seconds
			localCtdr += 1
			if (localCtdr == 5):
				jsonFile = open('%s/json_node%s.json' % (folderJsonName ,str(raspID)),"a")
				jsonFile.write(outputData)
				jsonFile.close()
				localCtdr = 0
				outputData = ""
		globalCtdr += 1

# Create a new 1 second audio file
def SetAudio():
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		localSample = 2
		# Catching audio and sensors data
		for ctdr in range (1, localSample + 1):
			#Wait til a second pass
			while( not( int((ctdr - 1)*(1000.0/localSample)) <= localMiliseconds < int(ctdr*(1000.0/localSample)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			# Recording audio
			if(ctdr == 1):
				firstTime = str(datetime.now()).replace(".",":")[:-3]
				RecordAudio(firstTime)


# Get neighbors using BLE scanner
def SetNeighbors(dataNeighbors):
	seconds = 2
	while(True):
		neighbors = blescan.GetNearBeacons(seconds)
		dataNeighbors['neighbors'] = '"Neighbors" : [%s]' % (str(neighbors))

# Updating configuration variables from the API
def ShowId():
	sense = SenseHat()
	sense.low_light = True
	while(True):
		sense.show_message(str(raspID), text_colour=[100, 100, 190])

# Running commands for enabling audio
def EnableAudio():
	try:
		command = 'amixer -c0 sset "Mic" 100%+'
		subprocess.call(command, shell=True)
	except:
		print("No microphone available")

# Running commands for enabling Bluetooth Low Energy transmission
def EnableBeacon():
	global raspID
	try:
		bletransmit.StartTransmission(raspID)
	except:
		print("No BLE device")

# Starting global variable collected from the configuration file
def SetConfigurationProperties():
	global raspID, sensorsSampleRate
	global accelSampleRate, gyroSampleRate, magnSampleRate
	configuration = []
	with open("/home/root/configuration.conf", "r") as text:
	    for line in text:
	    	if(line != "\n" and ("#" not in line)):
		        value = line.split(":")[1].replace("\n","")
		        configuration.append(value)
	# Initiating global configuration variables
	raspID = int(configuration[0])
	accelSampleRate = int(configuration[1])
	gyroSampleRate = accelSampleRate
	magnSampleRate = int(configuration[2])

# Start necessary variables for the collecting process
def PrepareOutputs():
	global raspID, jsonFile, folderAudioName, folderJsonName
	# Cleaning old outputs
	subprocess.call('rm -rf /home/root/outputs_node%s' % (str(raspID)), shell=True)
	subprocess.call('mkdir /home/root/outputs_node%s' % (str(raspID)), shell=True)
	subprocess.call('mkdir /home/root/outputs_node%s/audio_node%s' % (str(raspID), str(raspID)), shell=True)
	# Creates new folder for audio and JSON
	folderAudioName = '/home/root/outputs_node%s/audio_node%s' % (str(raspID), str(raspID))
	folderJsonName = '/home/root/outputs_node%s' % (str(raspID))
	# Opening JSON file
	outputName = '/home/root/outputs_node%s/json_node%s.json' % (str(raspID), str(raspID))
	jsonFile = open(outputName,"w+")

# Starting multiprocessing for multiple data collection
def StartProcesses():
	# Share variable between processes
	dataNeighbors = multiprocessing.Manager().dict()
	dataNeighbors['neighbors'] = '"Neighbors" : []'
	dataAccelerometer = multiprocessing.Manager().list()
	dataGyroscope = multiprocessing.Manager().list()
	dataMagnetometer = multiprocessing.Manager().list()
	# Enabling multiprocessing
	process1 = multiprocessing.Process(target=ShowId)
	process2 = multiprocessing.Process(target=SetAudio)
	process3 = multiprocessing.Process(target=SetNeighbors, args = [dataNeighbors])
	process4 = multiprocessing.Process(target=SetAccelerometerData, args = [dataAccelerometer])
	process5 = multiprocessing.Process(target=SetGyroscopeData, args = [dataGyroscope])
	process6 = multiprocessing.Process(target=SetMagnetometerData, args = [dataMagnetometer])
	process7 = multiprocessing.Process(target=SetSensorData, args = [dataNeighbors, dataAccelerometer, dataGyroscope, dataMagnetometer])
	# Starting all the processes
	process1.start()
	process2.start()
	process3.start()
	process4.start()
	process5.start()
	process6.start()
	process7.start()
	# Joining all the processes
	process1.join()
	process2.join()
	process3.join()
	process4.join()
	process5.join()
	process6.join()
	process7.join()

# Main of the application
if __name__ == '__main__':
	SetConfigurationProperties()	# Wearable configuration variables 
	EnableAudio()					# Running commands for enabling audio 
	EnableBeacon()					# Enabling BLE beacon transmission
	PrepareOutputs()				# Preparing audio and json files
	StartProcesses()				# Starting processes