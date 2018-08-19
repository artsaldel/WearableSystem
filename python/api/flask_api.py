
from flask import Flask
import json

app = Flask(__name__)

# Global variables: raspberry pi configuration
global lectureFrequency
global sensorsFrequency
global active

# Global variables: local PC configuration
global localIp
global localUsername
global localPassword

# Variables initial values: rpi configuration
lectureFrequency = 1
sensorsFrequency = 10
active = False

# Variables initial values: local PC configuration
localIp = "192.168.0.110"
localUsername = "arturo"
localPassword = "none"

@app.route('/')
def getData():
    global active, lectureFrequency, sensorsFrequency, localIp, localUsername, localPassword
    return json.dumps({'active' : active, 'lectureFrequency':lectureFrequency, 'sensorsFrequency':sensorsFrequency, 'localIp':localIp, 'localUsername':localUsername, 'localPassword':localPassword})

# *************************** ACTIVE VARIABLE ***************************
@app.route('/setActive/<value>')
def setActive(value):
    global active
    active = value
    return active

@app.route('/getActive/')
def getActive():
    global active
    return active

# *************************** LECTURE FREQUENCY VARIABLE ***************************
@app.route('/setLectureFrequency/<frequency>')
def setLectureFrequency(frequency):
    global lectureFrequency
    lectureFrequency = frequency
    return lectureFrequency

@app.route('/getLectureFrequency/')
def getLectureFrequency():
    global lectureFrequency
    return lectureFrequency

# *************************** SENSORS FREQUENCY VARIABLE ***************************
@app.route('/setSensorsFrequency/<frequency>')
def setSensorsFrequency(frequency):
    global sensorsFrequency
    sensorsFrequency = frequency
    return sensorsFrequency

@app.route('/getSensorsFrequency/')
def getSensorsFrequency():
    global sensorsFrequency
    return sensorsFrequency

# *************************** LOCAL IP VARIABLE ***************************
@app.route('/setLocalIp/<ip>')
def setLocalIp(ip):
    global localIp
    localIp = ip
    return localIp

@app.route('/getLocalIp/')
def getLocalIp():
    global localIp
    return localIp

# *************************** LOCAL USERNAME VARIABLE ***************************
@app.route('/setLocalUsername/<username>')
def setLocalUsername(username):
    global localUsername
    localUsername = username
    return localUsername

@app.route('/getLocalUsername/')
def getLocalUsername():
    global localUsername
    return localUsername

# *************************** LOCAL PASSWORD VARIABLE ***************************
@app.route('/setLocalPassword/<password>')
def setLocalPassword(password):
    global localPassword
    localPassword = password
    return localPassword

@app.route('/getLocalPassword/')
def getLocalPassword():
    global localPassword
    return localPassword
