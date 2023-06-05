# List of all the joysticks associated to the controllers
joysticks = []

# List of all the controllers
controllers = []

# Controller class
class Controller:
    def __init__(self, joystick):
        self.joystick = joystick
        self.forward = 0
        self.horiz_move = 0
        self.backward = 0
    def update(self):
        # Gets the horizontal angle on the joystick
        self.horiz_move = -self.joystick.get_axis(0)

        if abs(self.horiz_move) > 0.05:
            pass

        if self.joystick.get_button(1) == 1:
            self.forward = 1
        else :
            self.forward = 0

        if self.joystick.get_button(0) == 1:
            self.backward = 1
        else : 
            self.backward = 0
            
# Method used to update all the controllers
def updateController():
    for controller in controllers:
        controller.update()
