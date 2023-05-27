class Car:
  
  def __init__(self, id, id_pu, id_reset, server, colour, x=0, y=0, orientation=0, desired_velocity= 0, ai=True, powerup = 0, rank= 0, color="blue"):
    self.rank = rank
    self.id = id
    self.id_pu = id_pu
    self.id_reset = id_reset
    self.server = server
    self.old_x = None
    self.old_y = None
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
    self.acc = 3
    self.zone = 1
    self.ai = ai
    self.speed = "GREEN"
    self.powerup = powerup
    self.inverted = False
    self.left_circle = None
    self.right_circle = None
    self.colour = colour
    self.color = color
    self.moving = False
    self.count = 0
    self.started = False
    self.new_orientation = 0
    self.cam = True
    self.orientations = []
    self.manette = None
    self.joystick_connected= False
    
RED_C = (255, 0, 0)
BLUE_C = (0, 0, 255)
GREEN_C = (0, 255, 0)
VIOLET_C = (238, 130, 238)
ROSE_C = (255, 29, 206)
BRUN_C = (88, 41, 0)
