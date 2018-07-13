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

  # Getting gyroscope data
  gyroscopeRaw = sense.get_gyroscope_raw()
  gyroscope = sense.get_gyroscope()

  # Printing gyroscope data
  print("Raw data -> " + "x: {x}, y: {y}, z: {z}".format(**gyroscopeRaw))
  print("Direct data - > " + "p: {pitch}, r: {roll}, y: {yaw}".format(**gyroscope))

  time.sleep(1/frequency)