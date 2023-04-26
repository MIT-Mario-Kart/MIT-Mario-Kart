# xy orientation delta(servo) et xy autres voitures
import math
import numpy as np
import matplotlib.pyplot as plt


class Car:
  def init(self, name, server, x=0, y=0, interaction_index=0, index=0, move=False):
    self.name = name
    self.server = server
    self.x = x
    self.y = y
    self.interaction_index = interaction_index
    self.index = index # to be incremented every time we reach a given checkpoint
    self.move = move
    self.velocity = 0
    self.orientation = 0
    self.desired_orientation = 0
    self.delta = 0 # steering angle
    self.a = 0 # acceleration


def generate_semicircle(center_x, center_y, radius, stepsize=0.1):
    """
    generates coordinates for a semicircle, centered at center_x, center_y
    """        

    x = np.arange(center_x, center_x+radius+stepsize, stepsize)
    y = np.sqrt(radius**2 - x**2)

    # since each x value has two corresponding y-values, duplicate x-axis.
    # [::-1] is required to have the correct order of elements for plt.plot. 
    x = np.concatenate([x,x[::-1]])

    # concatenate y and flipped y. 
    y = np.concatenate([y,-y[::-1]])

    return x, y + center_y


x,y = generate_semicircle(0,0,10, 0.1)
plt.plot(x, y)
plt.show()

def overtake(mycar, positions, delta):

  radius = 10
  
  rad = math.radians(mycar.orientation)
  v = np.array([math.cos(rad) * radius, math.sin(rad) * radius]) 
  perp_v = np.dot(np.array([[0, -1], [1, 0]]), v)

  x1 = mycar.x - perp_v[0]
  y1 = mycar.y - perp_v[1]

  x2 = mycar.x + perp_v[0]
  y2 = mycar.y + perp_v[1]


  return 0


