class Grid:
    def __init__(self):
        self.top_left = None
        self.top_right = None
        self.bot_right = None
        self.bot_left = None
        self.width = 193 # real life width between the triangles
        self.height = 188.5 # real life height between the triangles
        self.calibrationColor = "yellow"
        self.coeff = 0.05
        self.centerInIOSCoords = [990, 540]

    # Method used to convert the coordinates from the camera to coordinates on the circuit
    # We first use the center in the iOS coordinates system to apply a correction to the original coordinates
    # and then we use the grid saved during the calibration period and the real life width and height between the triangles.
    def getCircuitCoords(self, x, y):
        patchedX = x + (self.centerInIOSCoords[0] - x) * self.coeff
        patchedY = y + (self.centerInIOSCoords[1] - y) * self.coeff
        new_X = ((self.bot_right[0] - patchedX) / abs(self.bot_right[0] - self.bot_left[0]) * self.width) 
        new_Y = ((patchedY - self.bot_right[1]) / abs(self.bot_right[1] - self.top_right[1]) * self.height) 
        return new_X, new_Y
    
    # We set up a grid system based on the information sent by the camera (we save the position of each triangle).
    def setupGrid(self, coordinates):
        coordinates.sort(key= lambda p : (p[1], p[0]))
        top = coordinates[2:]
        top.sort()
        self.top_left, self.top_right = top
        bot = coordinates[0:2]
        bot.sort()
        self.bot_left, self.bot_right = bot
        print(f"Grid Setup, top_left: {self.top_left}, top_right: {self.top_right}, bot_left: {self.bot_left}, bot_right: {self.bot_right}")
