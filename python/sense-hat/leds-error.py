from sense_hat import SenseHat
import time

sense = SenseHat()
sense.low_light = True

red = (255, 0, 0)
nothing = (0,0,0)

def figureError():
    R = red
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
    return logo

sense.set_pixels(figureError())
