class Car:
  def __init__(self, id, server, x=0, y=0, desired_velocity= 0, ai=True):
    self.id = id
    self.server = server
    self.old_x = x
    self.old_y = y
    self.x = x
    self.y = y
    self.predicted_x = x
    self.predicted_y = y
    self.velocity = 0
    self.desired_velocity = desired_velocity
    self.orientation = 0
    self.desired_orientation = 0
    self.delta = 0 # steering angle
    self.a = 0 # acceleration
    self.ai = ai