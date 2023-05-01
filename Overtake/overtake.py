# xy orientation delta(servo) et xy autres voitures
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge



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


def isInLeftCircle(pos, leftCircle):
  transformed_pos = leftCircle.get_transform().transform(pos)
  return leftCircle.contains_point(transformed_pos)

def isInRightCircle(pos, rightCircle):
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
    pos = c[0]
    leftC = c[1]
    rightC = c[2]    
    distance = math.dist(myPos, pos)
    sensibility = 3 # to test

    if (isInLeftCircle(myPos, leftC)):
      mycar.delta = mycar.delta + distance * sensibility

    if (isInRightCircle(myPos, rightC)):
      mycar.delta = mycar.delta - distance * sensibility





