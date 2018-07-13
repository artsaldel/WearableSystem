from sense_hat import SenseHat
import time

sense = SenseHat()
sense.low_light = True


yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
nothing = (0,0,0)
pink = (255,105, 180)
white = (255,255,255)

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

while (True):
  sense.set_pixels(figureOk())
  time.sleep(1)
  sense.set_pixels(figureError())
  time.sleep(1)