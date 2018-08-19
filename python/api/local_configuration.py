import requests

# Variables initial values: rpi configuration
active = False
lectureFrequency = 1
sensorsFrequency = 10

# Variables initial values: local PC configuration
localIp = "192.168.0.110"
localUsername = "arturo"
localPassword = "amandayguitarra1"

# Flask API URL
url = "http://artsaldel.pythonanywhere.com/"

# Configuration requests
req = requests.get(url + "setActive/" + str(active))
print("HTTP request status: " + str(req.status_code))

req = requests.get(url + "setLectureFrequency/" + str(lectureFrequency))
print("HTTP request status: " + str(req.status_code))

req = requests.get(url + "setSensorsFrequency/" + str(sensorsFrequency))
print("HTTP request status: " + str(req.status_code))

req = requests.get(url + "setLocalIp/" + str(localIp))
print("HTTP request status: " + str(req.status_code))

req = requests.get(url + "setLocalUsername/" + str(localUsername))
print("HTTP request status: " + str(req.status_code))

req = requests.get(url + "setLocalPassword/" + str(localPassword))
