from sense_hat import SenseHat

# Change as needed
okColor = (100, 100, 250)

errorColor = (255, 0, 0)
nothing = (0,0,0)

FLAG_OK = True
FLAG_NOT_OK = True

sense = SenseHat()
sense.low_light = True
sense.set_imu_config(True, True, True)

def SetLedsOk():
    global FLAG_OK, FLAG_NOT_OK
    if(FLAG_OK == True):
        G = okColor
        O = nothing
        logo = [
        G, G, O, O, O, O, O, O, 
        O, O, O, G, G, O, O, O, 
        O, O, G, G, G, G, O, O, 
        O, G, G, G, G, G, G, O, 
        O, G, G, G, G, G, G, O, 
        O, O, G, G, G, G, O, O, 
        O, O, O, G, G, O, O, O, 
        O, O, O, O, O, O, O, O, 
        ]
        sense.set_pixels(logo)
        FLAG_OK = False
        FLAG_NOT_OK = True

def SetLedsNotOk():
    global FLAG_OK, FLAG_NOT_OK
    if(FLAG_NOT_OK == True):
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
        FLAG_OK = True
        FLAG_NOT_OK = False