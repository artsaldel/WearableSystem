# *************************************************************************
# Arturo Salas Delgado
# Tecnologico de Costa Rica - TU Delft
# Sense hat data collecting
# *************************************************************************

from sense_hat import SenseHat

# Initializing the sense hat
sense = SenseHat();
import time

while (True):
  
  print("************************ 1 second pass ******************************")

  # Enabling Magnetometer (compass), Gyroscope and Accelerometer
  sense.set_imu_config(True, True, True)
  
  # Getting orientation data
  orientation = sense.get_orientation()
  orientationRadians = sense.get_orientation_radians()
  orientationDegrees = sense.get_orientation_degrees()
  
  # Getting magnetometer data
  magnetometerRaw = sense.get_compass_raw()
  magnetometerNorth = sense.get_compass()
  
  # Getting gyroscope data
  gyroscopeRaw = sense.get_gyroscope_raw()
  gyroscope = sense.get_gyroscope()
  
  # Getting accelerometer data
  accelerometerRaw = sense.get_accelerometer_raw()
  accelerometer = sense.get_accelerometer()
  
  # Printing orientation data
  print("**************** ORIENTATION DATA ***********************")
  print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
  print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientationRadians))
  print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientationDegrees))
  
  # Printing magnetometer data
  print("**************** MAGNETOMETER DATA **********************")
  print("Raw data -> " + "x: {x}, y: {y}, z: {z}".format(**magnetometerRaw))
  print("North: %s" % magnetometerNorth)
  
  # Printing gyroscope data
  print("**************** GYROSCOPE DATA *************************")
  print("Raw data -> " + "x: {x}, y: {y}, z: {z}".format(**gyroscopeRaw))
  print("Direct data - > " + "p: {pitch}, r: {roll}, y: {yaw}".format(**gyroscope))
  
  # Printing accelerometer data
  print("************** ACCELEROMETER DATA **********************")
  print("Raw data -> " + "x: {x}, y: {y}, z: {z}".format(**accelerometerRaw))
  print("Direct data -> " + "p: {pitch}, r: {roll}, y: {yaw}".format(**accelerometer))
  
  time.sleep(1)