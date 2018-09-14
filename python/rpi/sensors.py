import smbus
from datetime import datetime

bus = smbus.SMBus(1)

# Sensors addresses
GYRO_ADDR = 0x6a
ACCL_ADDR = 0x6a
MAGN_ADDR = 0x1c
CTRL_REG1_G = 0x10

def setGyroAccelSampleRate():
	bus.write_byte_data(GYRO_ADDR, CTRL_REG1_G, 0x2)
	bus.write_byte_data(ACCL_ADDR, CTRL_REG1_G, 0x2)


def ReadAccelerometer():
    acc_l = bus.read_byte_data(ACCL_ADDR, 0x28)
    acc_h = bus.read_byte_data(ACCL_ADDR, 0x29)
    acc_combined = (acc_l | acc_h << 8)
    xValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 1, 6)

    acc_l = bus.read_byte_data(ACCL_ADDR, 0x2a)
    acc_h = bus.read_byte_data(ACCL_ADDR, 0x2b)
    acc_combined = (acc_l | acc_h << 8)
    yValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 1, 6)

    acc_l = bus.read_byte_data(ACCL_ADDR, 0x2c)
    acc_h = bus.read_byte_data(ACCL_ADDR, 0x2d)
    acc_combined = (acc_l | acc_h << 8)
    zValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 1, 6)

    localTime = str(datetime.now()).replace(".",":")[:-3]

    return '{"Time": "%s", "x" : %s, "y" : %s, "z" : %s}' % (localTime, str(xValue), str(yValue), str(zValue))

def ReadGyroscope():
    gyr_l = bus.read_byte_data(GYRO_ADDR, 0x18)
    gyr_h = bus.read_byte_data(GYRO_ADDR, 0x19)
    gyr_combined = (gyr_l | gyr_h << 8)
    xValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

    gyr_l = bus.read_byte_data(GYRO_ADDR, 0x1a)
    gyr_h = bus.read_byte_data(GYRO_ADDR, 0x1b)
    gyr_combined = (gyr_l | gyr_h << 8)
    yValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

    gyr_l = bus.read_byte_data(GYRO_ADDR, 0x1c)
    gyr_h = bus.read_byte_data(GYRO_ADDR, 0x1d)
    gyr_combined = (gyr_l | gyr_h << 8)
    zValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

    localTime = str(datetime.now()).replace(".",":")[:-3]

    return '{"Time": "%s", "x" : %s, "y" : %s, "z" : %s}' % (localTime, str(xValue), str(yValue), str(zValue))

def ReadMagnetometer():
    gyr_l = bus.read_byte_data(MAGN_ADDR, 0x28)
    gyr_h = bus.read_byte_data(MAGN_ADDR, 0x29)
    gyr_combined = (gyr_l | gyr_h << 8)
    xValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

    gyr_l = bus.read_byte_data(MAGN_ADDR, 0x2a)
    gyr_h = bus.read_byte_data(MAGN_ADDR, 0x2b)
    gyr_combined = (gyr_l | gyr_h << 8)
    yValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

    gyr_l = bus.read_byte_data(MAGN_ADDR, 0x2c)
    gyr_h = bus.read_byte_data(MAGN_ADDR, 0x2d)
    gyr_combined = (gyr_l | gyr_h << 8)
    zValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

    localTime = str(datetime.now()).replace(".",":")[:-3]

    return '{"Time": "%s", "x" : %s, "y" : %s, "z" : %s}' % (localTime, str(xValue), str(yValue), str(zValue))
