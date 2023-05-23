import math
import numpy as np

def calcOrientation(coordinates, delta=1/10):
    frequence = delta
    delta_diff =1e-1

    # data to calculate orientation and speed

    currx=coordinates[-1][0]
    curry=coordinates[-1][1]

    if (coordinates[-2][0] == None or coordinates[-2][1] == None):
        return 0
    
    prevx=coordinates[-2][0]
    prevy=coordinates[-2][1]

    # code =============================================================================================================================

    x = (currx - prevx)
    y = (curry - prevy)
    if (y <= delta_diff and x <= delta_diff):
        return 0
    # Calculate absolute velocity
    # velocity = math.sqrt(x*x + y*y) * frequence

    # Calculate the orientation angle
    theta = math.atan2(y, x)

    # Convert radians to degrees
    theta_degrees = (math.degrees(theta) + 360) % 360
    
    return theta_degrees
