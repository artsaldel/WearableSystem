from sense_hat import SenseHat
import time

sense = SenseHat()
sense.low_light = True

green = (0, 255, 0)
nothing = (0,0,0)

def figureOk():
    G = green
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
    return logo

sense.set_pixels(figureOk())
