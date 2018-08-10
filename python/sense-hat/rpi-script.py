
from sense_hat import SenseHat
import time
import json

sense = SenseHat();
sense.set_imu_config(True, True, True)
data = []

def GetSensorsData(sensorsFrequency):
  while (True):  
    # Getting magnetometer data
    magnetometerRaw = sense.get_compass_raw()
    magnetometerX = "{x}".format(**magnetometerRaw)
    magnetometerY = "{y}".format(**magnetometerRaw)
    magnetometerZ = "{z}".format(**magnetometerRaw)
    
    # Getting gyroscope data
    gyroscopeRaw = sense.get_gyroscope_raw()
    gyroscopeX = "{x}".format(**gyroscopeRaw)
    gyroscopeY = "{y}".format(**gyroscopeRaw)
    gyroscopeZ = "{z}".format(**gyroscopeRaw)
    
    # Getting accelerometer data
    accelerometerRaw = sense.get_accelerometer_raw()
    accelerometerX = "{x}".format(**accelerometerRaw)
    accelerometerY = "{y}".format(**accelerometerRaw)
    accelerometerZ = "{z}".format(**accelerometerRaw)
    
    data.append(
      {
        "magnetometer" : {
          "x" : magnetometerX,
          "y" : magnetometerY,
          "z" : magnetometerZ
        },
        "gyroscope" : {
          "x" : gyroscopeX,
          "y" : gyroscopeY,
          "z" : gyroscopeZ
        },
        "accelererometer" : {
          "x" : accelerometerX,
          "y" : accelerometerY,
          "z" : accelerometerZ
        }
      }
    )
    time.sleep(1/frequency)