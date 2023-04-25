import math
import numpy as np

# inputs :
coordinates = input()
frequence = 1/10

# data to calculate orientation and speed
currx=coordinates[-1]
curry=coordinates[-1]

prevx=coordinates[-2]
prevy=coordinates[-2]

# code =============================================================================================================================

x = (currx - prevx)
y = (curry - prevy)

# Calculate absolute velocity
velocity = math.sqrt(x*x + y*y) * frequence

# Calculate the orientation angle
theta = math.atan2(y, x)

# Convert radians to degrees
theta_degrees = math.degrees(theta)



