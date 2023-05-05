class Car:
  def __init__(self, id, server, x=0, y=0, index=0):
    self.id = id
    self.server = server
    self.x = x
    self.y = y
    self.index = index # to be incremented every time we reach a given checkpoint
    self.velocity = 0
    self.orientation = 0
    self.desired_orientation = 0
    self.delta = 0 # steering angle
    self.a = 0 # acceleration
    self.player # true (player) or false (AI)
    self.inverted = 0


def isPlayer(car):
  return car.player