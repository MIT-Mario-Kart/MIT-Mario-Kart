import math
import numpy as np

# inputs :
coordinates = input()
frequence = 1/10

# data to calculate orientation and speed
currx=int(coordinates[-1][0])
curry=int(coordinates[-1][1])

prevx=int(coordinates[-2][0])
prevy=int(coordinates[-2][1])

# code =============================================================================================================================

x = (currx - prevx)
y = (curry - prevy)

# Calculate absolute velocity
velocity = math.sqrt(x*x + y*y) * frequence

# Calculate the orientation angle
theta = math.atan2(y, x)

# Convert radians to degrees
theta_degrees = math.degrees(theta)
