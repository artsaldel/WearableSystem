import smbus

bus = smbus.SMBus(1)

def readGyro():
    gyr_l = bus.read_byte_data(0x6a, 0x18)
    gyr_h = bus.read_byte_data(0x6a, 0x19)
    gyr_combined = (gyr_l | gyr_h << 8)
    xValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 0.00875, 4)

    gyr_l = bus.read_byte_data(0x6a, 0x1a)
    gyr_h = bus.read_byte_data(0x6a, 0x1b)
    gyr_combined = (gyr_l | gyr_h << 8)
    yValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 0.00875, 4)

    gyr_l = bus.read_byte_data(0x6a, 0x1c)
    gyr_h = bus.read_byte_data(0x6a, 0x1d)
    gyr_combined = (gyr_l | gyr_h << 8)
    zValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 0.00875, 4)

    return '{"x" : %s, "y" : %s, "z" : %s}' % (str(xValue), str(yValue), str(zValue))


def readAccel():
    acc_l = bus.read_byte_data(0x6a, 0x28)
    acc_h = bus.read_byte_data(0x6a, 0x29)
    acc_combined = (acc_l | acc_h << 8)
    xValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 0.00875, 4)

    acc_l = bus.read_byte_data(0x6a, 0x2a)
    acc_h = bus.read_byte_data(0x6a, 0x2b)
    acc_combined = (acc_l | acc_h << 8)
    yValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 0.00875, 4)

    acc_l = bus.read_byte_data(0x6a, 0x2c)
    acc_h = bus.read_byte_data(0x6a, 0x2d)
    acc_combined = (acc_l | acc_h << 8)
    zValue = round((acc_combined  if acc_combined < 32768 else acc_combined - 65536) * 0.00875, 4)

    return '{"x" : %s, "y" : %s, "z" : %s}' % (str(xValue), str(yValue), str(zValue))


def readMagn():
    gyr_l = bus.read_byte_data(0x1c, 0x28)
    gyr_h = bus.read_byte_data(0x1c, 0x29)
    gyr_combined = (gyr_l | gyr_h << 8)
    xValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 0.00875, 4)

    gyr_l = bus.read_byte_data(0x1c, 0x2a)
    gyr_h = bus.read_byte_data(0x1c, 0x2b)
    gyr_combined = (gyr_l | gyr_h << 8)
    yValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 0.00875, 4)

    gyr_l = bus.read_byte_data(0x1c, 0x2c)
    gyr_h = bus.read_byte_data(0x1c, 0x2d)
    gyr_combined = (gyr_l | gyr_h << 8)
    zValue = round((gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536) * 0.00875, 4)

    return '{"x" : %s, "y" : %s, "z" : %s}' % (str(xValue), str(yValue), str(zValue))
