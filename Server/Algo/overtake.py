# xy orientation delta(servo) et xy autres voitures
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

# leftCircle has to be claculated with claculateCircles()
def isInLeftCircle(pos, leftCircle):
  transformed_pos = leftCircle.get_transform().transform(pos)
  return leftCircle.contains_point(transformed_pos)

# rightCircle has to be claculated with claculateCircles()
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
    pos = (c.x, c.y)
    leftC = c[1]
    rightC = c[2]    
    distance = math.dist(myPos, pos)
    sensibility = 3 # to test

    derivation = sensibility / distance 
    if derivation > 90 :
      derivation = 90
      
    if (isInLeftCircle(myPos, leftC)):
        if mycar.delta + derivation > 180 :
            mycar.delta = 180
        else :
           mycar.delta = mycar.delta + derivation
    

    if (isInRightCircle(myPos, rightC)):
        if mycar.delta - derivation < 0 :
            mycar.delta = 0
        else :
           mycar.delta = mycar.delta - derivation


def slowDown(mycar, otherCars):


  for c in otherCars:
    if (mycar.id != c.id):

        myPos = (mycar.x, mycar.y)
        pos = (c.x, c.y)

        circles = calculateCircles(c)
        leftC = circles[0]
        rightC = circles[1]

        distance = math.dist(myPos, pos)

        sensibility = 500 # to test
        slowDown = sensibility / distance 
        if mycar.acc - slowDown < 0 :
            mycar.acc = slowDown
        
        if (isInLeftCircle(myPos, leftC) or isInRightCircle(myPos, rightC)):
            mycar.acc -= slowDown
        

           
