# xy orientation delta(servo) et xy autres voitures
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

# leftCircle has to be claculated with claculateCircles()
def isInLeftCircle(pos, leftCircle: Wedge):
  transformed_pos = leftCircle.get_transform().transform(pos)
  return leftCircle.contains_point(transformed_pos)

# rightCircle has to be claculated with claculateCircles()
def isInRightCircle(pos, rightCircle: Wedge):
  transformed_pos = rightCircle.get_transform().transform(pos)
  return rightCircle.contains_point(transformed_pos)



def calculateCircles(mycar):
  radius = 10
  dir = mycar.orientation
  myPos = (mycar.x, mycar.y)
  theta1, theta2 = dir + 90, dir - 90

  semi_circle_left = Wedge(myPos, radius, theta1, dir, fc='black', edgecolor='black')
  semi_circle_right = Wedge(myPos, radius, dir, theta2, fc='white', edgecolor='white')
  plt.gca().add_patch(semi_circle_left)
  plt.gca().add_patch(semi_circle_right)

  return([semi_circle_left, semi_circle_right])

  
# input otherCars : list of [position, leftCircle, rightCircle]
def overtake(mycar, otherCars):

  myPos = (mycar.x, mycar.y)

  for c in otherCars:
    if mycar != c:
      pos = (c.x, c.y)
      leftC = c.left_circle
      rightC = c.right_circle   
      distance = math.dist(myPos, pos)
      sensibility = 4 # to test

      if (isInLeftCircle(myPos, leftC)):
        mycar.delta = mycar.delta + distance * sensibility
        mycar.orientation = mycar.delta + distance * sensibility

      if (isInRightCircle(myPos, rightC)):
        mycar.delta = mycar.delta - distance * sensibility
        mycar.orientation = mycar.delta - distance * sensibility

    


