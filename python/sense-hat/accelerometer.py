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

  # Getting accelerometer data
  accelerometerRaw = sense.get_accelerometer_raw()
  accelerometer = sense.get_accelerometer()

  # Printing accelerometer data
  print("Raw data -> " + "x: {x}, y: {y}, z: {z}".format(**accelerometerRaw))
  print("Direct data -> " + "p: {pitch}, r: {roll}, y: {yaw}".format(**accelerometer))

  time.sleep(1/frequency)