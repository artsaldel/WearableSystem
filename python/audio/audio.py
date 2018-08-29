from datetime import datetime
import subprocess
import time

seconds = 1
while(True):
	localTime = str(datetime.now())
	command = "arecord -d" + str(seconds) + " /home/arturo/Escritorio/WearableSystem/python/audio/outputs/" + str(localTime).replace(" ", "_") + ".wav"
	subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	time.sleep(seconds)

	