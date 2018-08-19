from sense_hat import SenseHat

# Change as needed
okColor = (50, 120, 190)

errorColor = (255, 0, 0)
nothing = (0,0,0)

def SetLedsOk():
    sense = SenseHat()
    sense.low_light = True
    sense.set_imu_config(True, True, True)
    G = okColor
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O, 
    O, O, O, G, G, O, O, O, 
    O, O, G, G, G, G, O, O, 
    O, G, G, G, G, G, G, O, 
    O, G, G, G, G, G, G, O, 
    O, O, G, G, G, G, O, O, 
    O, O, O, G, G, O, O, O, 
    O, O, O, O, O, O, O, O, 
    ]
    sense.set_pixels(logo)

def SetLedsNotOk():
    sense = SenseHat()
    sense.low_light = True
    sense.set_imu_config(True, True, True)
    R = errorColor
    O = nothing
    logo = [
    R, R, O, O, O, O, R, R,
    R, R, R, O, O, R, R, R,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, R, R, R, R, O, O,
    O, R, R, R, R, R, R, O,
    R, R, R, O, O, R, R, R,
    R, R, O, O, O, O, R, R
    ]
    sense.set_pixels(logo)