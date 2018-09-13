import sensors
import blescan
import threading
import subprocess
from datetime import datetime
from sense_hat import SenseHat

# Global variables
global raspID, lectureFrequency, sensorsSampleRate
global neighborsData, senseHatData, sense
global folderAudioName, folderJsonName, jsonFile

# Creates a new folder for saving audio ouput files
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

	
def RecordAudio(localTime):
	global lectureFrequency, folderAudioName
	fileName = str(localTime).replace(" ", "_").replace(":","-")
	command = 'arecord -f S16_LE -c1 -r16000 -d %s %s/%s.wav' % (str(lectureFrequency), folderAudioName, fileName)
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
	global sensorsSampleRate, neighborsData
	global senseHatData, folderJsonName, jsonFile
	# Preparing audio and json files
	PrepareOutputs()
	# Local variables
	outputData = "["
	localCtdr = 0
	globalCtdr = 0
	#Start adquiring information
	while(True):
		dataTime = []
		dataAccelerometer = []
		dataMagnetometer = []
		dataGyroscope = []
		localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
		firstTime = str(datetime.now()).replace(".",":")[:-3]

		# Catching audio and sensors data
		for ctdr in range (1, sensorsSampleRate + 1):
			#Wait til a second pass
			while( not( int((ctdr - 1)*(1000.0/sensorsSampleRate)) <= localMiliseconds < int(ctdr*(1000.0/sensorsSampleRate)) ) ):
				try:
					localMiliseconds = int(str(datetime.now()).replace(".",":")[:-3][-3:])
				except:
					pass

			# Recording audio
			if(ctdr == 1):
				firstTime = str(datetime.now()).replace(".",":")[:-3]
				RecordAudio(firstTime)

			# Collecting data from the sensors
			dataGyroscope.append(sensors.readGyro())
			dataAccelerometer.append(sensors.readAccel())
			dataMagnetometer.append(sensors.readMagn())

		# Time drift against NTP server
		timeDrift = GetTimeDrift()

		# Save the information as JSON format
		senseHatData = '"Accelerometer" : [%s],\n"Magnetometer" : [%s],\n"Gyroscope" : [%s]' % (str(dataAccelerometer).replace("'",""), str(dataMagnetometer).replace("'",""), str(dataGyroscope).replace("'",""))
		outputData += '{\n"Local time" : "%s",\n"Node id" : %d,\n"NTP time drift" : "%s",\n"Application data" : {\n%s,\n%s}\n},\n\n\n' % (firstTime, raspID, timeDrift, str(neighborsData), str(senseHatData))

		# Write the information into the JSON file every 5 seconds
		localCtdr += 1
		globalCtdr += 1
		if (localCtdr == 5):
			jsonFile = open('%s/json_node%s.json' % (folderJsonName ,str(raspID)),"a")
			jsonFile.write(outputData)
			jsonFile.close()
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

def EnableAudio():
	# Running command for enabling audio
	try:
		command = 'amixer -c0 sset "Mic" 100%+'
		subprocess.call(command, shell=True)
		subprocess.call("clear", shell=True)
	except:
		print("No microphone available")

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

def SetConfigurationProperties():
	global raspID, lectureFrequency,sensorsSampleRate
	configuration = []
	with open("/home/root/configuration.conf", "r") as text:
	    for line in text:
	    	if(line != "\n"):
		        value = line.split(":")[1].replace("\n","")
		        configuration.append(value)

	# Initiating global configuration variables
	raspID = int(configuration[0])
	sensorsSampleRate = int(configuration[1])
	lectureFrequency = 1

# Main of the application
if __name__ == '__main__':
	# Global variables
	global neighborsData, senseHatData, sense

	# Wearable configuration variables 
	SetConfigurationProperties()	

	#Running commands for enabling audio and beacon transmission
	EnableAudio()
	EnableBeacon()

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