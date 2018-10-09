import array
import smbus
from datetime import datetime


# Class for collecting sensors' information
class Sensors:

    def __init__(self, accelGyroSampleRate, magnSampleRate):
        self.i2cBus = smbus.SMBus(1)
        # Sensors addresses
        self.GYRO_ADDR = 0x6a
        self.ACCL_ADDR = 0x6a
        self.MAGN_ADDR = 0x1c

        self.SAMPLE_RATE_ACCL_GYRO = 5
        self.SAMPLE_RATE_MAGN = 1

        self.scratch = array.array('B',[0,0,0,0,0,0])
        self.scratchInt = array.array('h',[0,0,0])

        self.SCALE_GYRO = [(245,0),(500,1),(2000,3)]
        self.SCALE_ACCEL = [(2,0),(4,2),(8,3),(16,1)]

        self.CTRL_REG1_G = 0x10
        self.CTRL_REG4_G = 0x1e
        self.CTRL_REG1_M = 0x20

        self.FIFO_CTRL_REG = 0x2e
        self.FIFO_SRC = 0x2f

        self.OUT_ACCL = 0x28
        self.OUT_GYRO = 0x18 
        self.OUT_MAGN = 0x28

        self.InitAccelGyro(6)
        self.InitMagnetometer(6)

    """ 
    Initalizes Gyro and Accelerator:
        - sampleRate: 0-6 (off, 14.9Hz, 59.5Hz, 119Hz, 238Hz, 476Hz, 952Hz)
        - scaleGyro: 0-2 (245dps, 500dps, 2000dps ) 
        - scaleAccel: 0-3 (+/-2g, +/-4g, +/-8g, +-16g)
    """
    def InitAccelGyro(self, sampleRate = 6):
        
        scaleAccel =0
        scaleGyro = 0
        assert sampleRate <= 6, 'Invalid sampling rate for accel and gyro: %d' % sample_rate
        mv = self.scratch

        mv[0] = ((sampleRate & 0x07) << 5) | ((self.SCALE_GYRO[scaleGyro][1] & 0x3) << 3) 
        mv[1:4] = array.array('B', b'\x00\x00\x00') 

        self.i2cBus.write_i2c_block_data(self.GYRO_ADDR, self.CTRL_REG1_G, mv[:5].tolist())

        mv[0] = mv[1] = 0x38
        mv[2] = ((sampleRate & 7) << 5) | ((self.SCALE_ACCEL[scaleAccel][1] & 0x3) << 3)
        mv[3] = 0x00
        mv[4] = 0x4
        mv[5] = 0x2

        self.i2cBus.write_i2c_block_data(self.ACCL_ADDR, self.CTRL_REG4_G, mv[:6].tolist())

        # Fifo: continous mode (overwrite old data if overflow)
        self.i2cBus.write_byte_data(self.GYRO_ADDR, self.FIFO_CTRL_REG, 0x00)
        self.i2cBus.write_byte_data(self.ACCL_ADDR, self.FIFO_CTRL_REG, 0xC0)

        self.scaleGyro = 32768 / self.SCALE_GYRO[scaleGyro][0]
        self.scaleAccel = 32768 / self.SCALE_ACCEL[scaleAccel][0]


    """ 
    Initalizes Magnetometer:
        - sample rates = 0-7 (0.625, 1.25, 2.5, 5, 10, 20, 40, 80Hz)
        - scaling = 0-3 (+/-4, +/-8, +/-12, +/-16 Gauss)
    """
    def InitMagnetometer(self, sampleRate = 7):
        scaleMagnet = 0
        assert sampleRate < 8, "invalid sample rate: %d (0-7)" % sample_rate
        mv = self.scratch

        mv[0] = 0x40 | (sampleRate << 2)    # Ctrl1: high performance mode
        mv[1] = scaleMagnet << 5            # Ctrl2: scale, normal mode, no reset
        mv[2] = 0x00                        # Ctrl3: continous conversion, no low power, I2C
        mv[3] = 0x08                        # Ctrl4: high performance z-axis
        mv[4] = 0x00                        # Ctrl5: no fast read, no block update

        self.i2cBus.write_i2c_block_data(self.MAGN_ADDR, self.CTRL_REG1_M, mv[:5].tolist())
        self.scaleFactorMagnet = 32768 / ((scaleMagnet+1) * 4 )

    # Return one single accelerometer value
    def ReadSingleAccelerometer(self):
        # Returns acceleration vector in gravity units (9.81m/s^2)
        factor = self.scaleAccel
        mv = self.i2cBus.read_i2c_block_data(self.ACCL_ADDR, self.OUT_ACCL | 0x80, 16)
        return (mv[0]/factor, mv[1]/factor, mv[2]/factor)

    # Return one single gyroscope value
    def ReadSingleGyroscope(self):
        # Returns gyroscope vector in degrees/sec
        factor = self.scaleGyro
        mv = self.i2cBus.read_i2c_block_data(self.GYRO_ADDR, self.OUT_GYRO | 0x80, 16)
        return (mv[0]/factor, mv[1]/factor, mv[2]/factor)

    # Return accelerometer and gyroscope fifo data
    def ReadFifo(self):
        while(True):
            fifoState = self.i2cBus.read_i2c_block_data(self.ACCL_ADDR, self.FIFO_SRC, 1)[0]
            print(fifoState)
            if(fifoState & 0x3f):
                yield self.ReadSingleGyroscope(),self.ReadSingleAccelerometer()
                print("Available samples = %d" % (fifo_state & 0x1f))
            else:
                break

    # Return one single magnetometer value
    def ReadSingleMagnetometer(self):
        # Returns magnetometer vector in gauss. Raw_values: if True, the non-scaled adc values are returned
        factor = self.scaleFactorMagnet
        mv = self.i2cBus.read_i2c_block_data(self.MAGN_ADDR, self.OUT_MAGN | 0x80, 16)
        return (mv[0]/factor, mv[1]/factor, mv[2]/factor)

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

        return '{"x" : %s, "y" : %s, "z" : %s}' % (str(xValue), str(yValue), str(zValue))

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

        return '{"x" : %s, "y" : %s, "z" : %s}' % (str(xValue), str(yValue), str(zValue))

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

        return '{"x" : %s, "y" : %s, "z" : %s}' % (str(xValue), str(yValue), str(zValue))

    # Get the frequency of the accelerometer and gyroscope by the value
    def GetAccelGyroFreqByValue(self, value):
        rate = 14.9
        if(value == 1): rate = 14.9
        elif(value == 2): rate = 59.5
        elif(value == 3): rate = 119.0
        elif(value == 4): rate = 238.0
        elif(value == 5): rate = 476.0
        elif(value == 6): rate = 952.0
        else: rate = 14.9 # Default Value
        return rate

    # Get the frequency of the magnetometer by the value
    def GetMagnByValue(self, value):    
        rate = 0.625
        if(value == 0): rate = 0.625
        elif(value == 1): rate = 1.25
        elif(value == 2): rate = 2.5
        elif(value == 3): rate = 5.0
        elif(value == 4): rate = 10.0
        elif(value == 5): rate = 20.0
        elif(value == 6): rate = 40.0
        elif(value == 7): rate = 80.0
        else: rate = 20.0 # Default value
        return rate