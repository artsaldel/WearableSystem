import math

def CalculateBeaconDistance(rssi):
    a = 0.252585
    b = -7.119942
    c = -30.520879
    det = math.pow(b,2) - 4.0 * (a) * (c - rssi)
    sol = (-1.0 * b - math.sqrt(det))/(2.0 * a)
    return sol

CalculateBeaconDistance(-43)