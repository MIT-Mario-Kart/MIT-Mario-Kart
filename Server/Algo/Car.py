from random import choice
import PowerUp

RED_C = (255, 0, 0)
BLUE_C = (0, 0, 255)
GREEN_C = (0, 255, 0)
VIOLET_C = (238, 130, 238)
ROSE_C = (255, 29, 206)
BRUN_C = (88, 41, 0)

class Car:
    def __init__(self, name, rank, id, colour, color, x=0, y=0, orientation=0, desired_velocity=0, ai=True):
        self.name = name
        self.rank = rank
        self.id = id
        self.ai = ai
        self.colour = colour
        self.curr_lap = 0
        self.last_lap = 0
        self.best_lap = 0
        self.lap_count = 0
        self.powerup = 0
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
        self.delta = 90  # steering angle
        self.a = 1  # acceleration
        self.zone = 1
        self.speed = "GREEN"
        self.inverted = False
        self.left_circle = None
        self.right_circle = None
        self.finished = False
        self.color = color
        self.joystick_connected = False
        self.manette = None
        self.started = False
        self.startTime = -1
        self.acc = 180
        self.checkpoints = []
        self.request = None

    def shuffle(self):
        self.power = choice(PowerUp.list_power)

    def add_lap(self):
        self.on_the_line = True
        self.lap_count += 1
        self.last_lap += self.curr_lap

        if self.curr_lap < self.best_lap:
            self.best_lap = round(self.curr_lap, 3)

        elif self.best_lap == 0 and self.lap_count == 2:
            self.best_lap = round(self.curr_lap, 3)

        self.curr_lap = 0
        self.checkpoints = []

    def update(self, second):
        self.curr_lap = second - self.last_lap

    #def not_on_the_line(self):
      #  self.on_the_line = False
