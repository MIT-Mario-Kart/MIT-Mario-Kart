class Car:
  def __init__(self, id, id_pu, id_reset, server, x=0, y=0, orientation=0, desired_velocity= 0, ai=True, powerup = 0):
    self.id = id
    self.id_pu = id_pu
    self.id_reset = id_reset
    self.server = server
    self.old_x = x
    self.old_y = y
    self.x = x
    self.y = y
    self.predicted_x = x
    self.predicted_y = y
    self.velocity = 0
    self.desired_velocity = desired_velocity
    self.orientation = orientation
    self.desired_orientation = 0
    self.fm_orientation = 0
    self.old_delta = 90
    self.delta = 90 # steering angle
    self.a = 1 # acceleration
    self.zone = 1
    self.ai = ai
    self.speed = "GREEN"
    self.powerup = powerup
    self.inverted = False