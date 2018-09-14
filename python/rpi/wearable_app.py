import sensors
import blescan
import subprocess
import multiprocessing
from ctypes import c_char_p
from datetime import datetime
from sense_hat import SenseHat

# Global variables
global raspID, sense
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
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		# Wait til a second pass
		for ctdr in range (1, accelSampleRate + 1):
			# Collect information from accelerometer
			while( not( int((ctdr - 1)*(1000.0/accelSampleRate)) <= localMiliseconds < int(ctdr*(1000.0/accelSampleRate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			if(ctdr == 1):
				del dataAccelerometer[:]
			dataAccelerometer.append(sensors.ReadAccelerometer())

# Setting data from gyroscope
def SetGyroscopeData(dataGyroscope):
	global gyroSampleRate
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		# Wait til a second pass
		for ctdr in range (1, gyroSampleRate + 1):
			# Collect information from gyroscope
			while( not( int((ctdr - 1)*(1000.0/gyroSampleRate)) <= localMiliseconds < int(ctdr*(1000.0/gyroSampleRate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			if(ctdr == 1):
				del dataGyroscope[:]
			dataGyroscope.append(sensors.ReadGyroscope())

# Setting data from magnetometer
def SetMagnetometerData(dataMagnetometer):
	global magnSampleRate
	while(True):
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		# Wait til a second pass
		for ctdr in range (1, magnSampleRate + 1):
			# Collect information from magnetometer
			while( not( int((ctdr - 1)*(1000.0/magnSampleRate)) <= localMiliseconds < int(ctdr*(1000.0/magnSampleRate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass
			if(ctdr == 1):
				del dataMagnetometer[:]
			dataMagnetometer.append(sensors.ReadMagnetometer())

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
				firstTime = str(datetime.now()).replace(".",":")[:-3]
		if(globalCtdr > 2):
			# Time drift against NTP server
			timeDrift = GetTimeDrift()
			# Save the information as JSON format
			senseHatData = '"Accelerometer" : [%s],\n"Gyroscope" : [%s],\n"Magnetometer" : [%s]' % (str(dataAccelerometer).replace("'",""), str(dataGyroscope).replace("'",""), str(dataMagnetometer).replace("'",""))
			outputData += '{\n"Local time" : "%s",\n"Node id" : %d,\n"NTP time drift" : "%s",\n"Application data" : {\n%s,\n%s}\n},\n\n\n' % (firstTime, raspID, timeDrift, str(dataNeighbors['neighbors']), str(senseHatData))
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
	seconds = 1
	while(True):
		neighbors = blescan.GetNearBeacons(seconds)
		dataNeighbors['neighbors'] = '"Neighbors" : [%s]' % (str(neighbors))

# Updating configuration variables from the API
def ShowId():
	while(True):
		sense.show_message(str(raspID))

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
		subprocess.call("hciattach /dev/ttyAMA0 bcm43xx 115200 noflow -", shell=True)
		subprocess.call("hciconfig hci0 up", shell=True)
		subprocess.call("hciconfig hci0 leadv 3", shell=True)
		subprocess.call("hciconfig hci0 noscan", shell=True)
		hexID = str(hex(raspID).split('x')[-1]).zfill(4)
		commandBeacon = 'hcitool -i hci0 cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 %s %s c5 00 00 00 00 00 00 00 00 00 00 00 00 00' % (hexID[:2], hexID[2:])
		subprocess.call(commandBeacon, shell=True)
		subprocess.call("hcitool -i hci0 cmd 0x08 0x0006 40 01 40 01 03 00 00 00 00 00 00 00 00 07 00", shell=True)
		subprocess.call("hcitool -i hci0 cmd 0x08 0x000a 01", shell=True)
	except:
		print("No BLE device")

# Starting global variable collected from the configuration file
def SetConfigurationProperties():
	global raspID, sensorsSampleRate
	global accelSampleRate, gyroSampleRate, magnSampleRate
	configuration = []
	with open("/home/root/configuration.conf", "r") as text:
	    for line in text:
	    	if(line != "\n"):
		        value = line.split(":")[1].replace("\n","")
		        configuration.append(value)
	# Initiating global configuration variables
	raspID = int(configuration[0])
	accelSampleRate = int(configuration[1])
	gyroSampleRate = int(configuration[2])
	magnSampleRate = int(configuration[3])

# Start necessary variables for the collecting process
def PrepareOutputs():
	global raspID, jsonFile, folderAudioName, folderJsonName, sense
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
	
	# Sense hat initialization
	sense = SenseHat();
	sense.set_imu_config(True, True, True)

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
	process3 = multiprocessing.Process(target=SetNeighbors, args = (dataNeighbors,))
	process4 = multiprocessing.Process(target=SetAccelerometerData, args = (dataAccelerometer,))
	process5 = multiprocessing.Process(target=SetGyroscopeData, args = (dataGyroscope,))
	process6 = multiprocessing.Process(target=SetMagnetometerData, args = (dataMagnetometer,))
	process7 = multiprocessing.Process(target=SetSensorData, args = (dataNeighbors, dataAccelerometer, dataGyroscope, dataMagnetometer,))
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
	# Wearable configuration variables 
	SetConfigurationProperties()	
	#Running commands for enabling audio and beacon transmission
	EnableAudio()
	EnableBeacon()
	# Preparing audio and json files
	PrepareOutputs()	
	# Starting processes
	StartProcesses()	