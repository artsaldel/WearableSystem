import smbus
from datetime import datetime


# Class for collecting sensors' information
class Sensors:

    def __init__(self):
        self.i2cBus = smbus.SMBus(1)
        # Sensors addresses
        self.GYRO_ADDR = 0x6a
        self.ACCL_ADDR = 0x6a
        self.MAGN_ADDR = 0x1c

    # Reading a byte from the accelerometer by address
    def ReadAccelerometer(self):
        acc_l = self.i2cBus.read_byte_data(self.ACCL_ADDR, 0x28)
        acc_h = self.i2cBus.read_byte_data(self.ACCL_ADDR, 0x29)
        acc_combined = (acc_l | acc_h << 8)
        xValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 1, 6)

        acc_l = self.i2cBus.read_byte_data(self.ACCL_ADDR, 0x2a)
        acc_h = self.i2cBus.read_byte_data(self.ACCL_ADDR, 0x2b)
        acc_combined = (acc_l | acc_h << 8)
        yValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 1, 6)

        acc_l = self.i2cBus.read_byte_data(self.ACCL_ADDR, 0x2c)
        acc_h = self.i2cBus.read_byte_data(self.ACCL_ADDR, 0x2d)
        acc_combined = (acc_l | acc_h << 8)
        zValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 1, 6)

        localTime = str(datetime.now()).replace(".",":")[:-3]

        return '{"Time": "%s", "x" : %s, "y" : %s, "z" : %s}' % (localTime, str(xValue), str(yValue), str(zValue))

    # Reading a byte from the gyroscope by address
    def ReadGyroscope(self):
        gyr_l = self.i2cBus.read_byte_data(self.GYRO_ADDR, 0x18)
        gyr_h = self.i2cBus.read_byte_data(self.GYRO_ADDR, 0x19)
        gyr_combined = (gyr_l | gyr_h << 8)
        xValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

        gyr_l = self.i2cBus.read_byte_data(self.GYRO_ADDR, 0x1a)
        gyr_h = self.i2cBus.read_byte_data(self.GYRO_ADDR, 0x1b)
        gyr_combined = (gyr_l | gyr_h << 8)
        yValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

        gyr_l = self.i2cBus.read_byte_data(self.GYRO_ADDR, 0x1c)
        gyr_h = self.i2cBus.read_byte_data(self.GYRO_ADDR, 0x1d)
        gyr_combined = (gyr_l | gyr_h << 8)
        zValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 1, 6)

        localTime = str(datetime.now()).replace(".",":")[:-3]

        return '{"Time": "%s", "x" : %s, "y" : %s, "z" : %s}' % (localTime, str(xValue), str(yValue), str(zValue))

    # Reading a byte from the magnetometer by address
    def ReadMagnetometer(self):
        mag_l = self.i2cBus.read_byte_data(self.MAGN_ADDR, 0x28)
        mag_h = self.i2cBus.read_byte_data(self.MAGN_ADDR, 0x29)
        mag_combined = (mag_l | mag_h << 8)
        xValue = round((mag_combined  if mag_combined < 32768 else mag_combined - 65536) * 1, 6)

        mag_l = self.i2cBus.read_byte_data(self.MAGN_ADDR, 0x2a)
        mag_h = self.i2cBus.read_byte_data(self.MAGN_ADDR, 0x2b)
        mag_combined = (mag_l | mag_h << 8)
        yValue = round((mag_combined  if mag_combined < 32768 else mag_combined - 65536) * 1, 6)

        mag_l = self.i2cBus.read_byte_data(self.MAGN_ADDR, 0x2c)
        mag_h = self.i2cBus.read_byte_data(self.MAGN_ADDR, 0x2d)
        mag_combined = (mag_l | mag_h << 8)
        zValue = round((mag_combined  if mag_combined < 32768 else mag_combined - 65536) * 1, 6)

        localTime = str(datetime.now()).replace(".",":")[:-3]

        return '{"Time": "%s", "x" : %s, "y" : %s, "z" : %s}' % (localTime, str(xValue), str(yValue), str(zValue))
