# *************************************************************************
# Arturo Salas Delgado
# Tecnologico de Costa Rica - TU Delft
# Sense hat data collecting
# *************************************************************************

from sense_hat import SenseHat
import time

# Initializing the sense hat
sense = SenseHat();
frequency = 1 #Hz


while (True):
  
  print("******************************************************")

  # Enabling Magnetometer (compass), Gyroscope and Accelerometer
  sense.set_imu_config(True, True, True)

   # Getting magnetometer data
  magnetometerRaw = sense.get_compass_raw()
  magnetometerNorth = sense.get_compass()

  # Printing magnetometer data
  print("Raw data -> " + "x: {x}, y: {y}, z: {z}".format(**magnetometerRaw))
  print("North: %s" % magnetometerNorth)

  time.sleep(1/frequency)