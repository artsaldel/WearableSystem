
from sense_hat import SenseHat
import time

sense = SenseHat();
sense.set_imu_config(True, True, True)

dataAccelerometer = []
dataMagnetometer = []
dataGyroscope = []


def StartSensorsData(sensorsFrequency):
    global dataAccelerometer
    global dataMagnetometer
    global dataGyroscope
    ctdr = 0
    while (ctdr < sensorsFrequency):
        # Getting magnetometer data
        magnetometerRaw = sense.get_compass_raw()
        
        # Getting gyroscope data
        gyroscopeRaw = sense.get_gyroscope_raw()
        
        # Getting accelerometer data
        accelerometerRaw = sense.get_accelerometer_raw()

        # Appending information to final result
        dataAccelerometer.append(accelerometerRaw)
        dataMagnetometer.append(magnetometerRaw)
        dataGyroscope.append(gyroscopeRaw)
        
        # Sleeping depending on the frequency
        time.sleep(1/sensorsFrequency)

        # Increasing the counter
        ctdr += 1

def GetAccelerometerData():
    return dataAccelerometer

def GetMagnetometerData():
    return dataMagnetometer

def GetGyroscopeData():
    return dataGyroscope

def CleanResults():
    global dataAccelerometer, dataMagnetometer, dataGyroscope
    dataAccelerometer = []
    dataMagnetometer = []
    dataGyroscope = []


