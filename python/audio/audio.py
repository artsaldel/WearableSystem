from datetime import datetime
import subprocess
import time

seconds = 1
while(True):
	localTime = str(datetime.now())
	#command = "arecord -d" + str(seconds) + " /home/arturo/Escritorio/WearableSystem/python/audio/outputs/" + str(localTime).replace(" ", "_") + ".wav"
	command = 'arecord -D plughw:2,0 -f S16_LE -c2 -r16000 --disable-softvol -d %s %s/%s.wav' % (str(seconds), " /home/arturo/Escritorio/WearableSystem/python/audio/outputs", localTime)
	subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	time.sleep(seconds)

	