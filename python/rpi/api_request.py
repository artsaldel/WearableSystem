import sys
import requests

url = "http://artsaldel.pythonanywhere.com/"

def GetActiveValue():
	try:
		req = requests.get(url + "getActive/")
	except:
		print("No connection to the API")
		sys.exit(1)
	return req.content

def GetLectureFrequencyValue():
	try:
		req = requests.get(url + "getLectureFrequency/")
	except:
		print("No connection to the API")
		sys.exit(1)
	return req.content

def GetSensorsFrequencyValue():
	try:
		req = requests.get(url + "getSensorsFrequency/")
	except:
		print("No connection to the API")
		sys.exit(1)
	return req.content

def GetLocalIpValue():
	try:
		req = requests.get(url + "getLocalIp/")
	except:
		print("No connection to the API")
		sys.exit(1)
	return req.content

def GetLocalUsernameValue():
	try:
		req = requests.get(url + "getLocalUsername/")
	except:
		print("No connection to the API")
		sys.exit(1)
	return req.content

def GetLocalPasswordValue():
	try:
		req = requests.get(url + "getLocalPassword/")
	except:
		print("No connection to the API")
		sys.exit(1)
	return req.content