class Grid:
    def __init__(self):
        self.top_left = None
        self.top_right = None
        self.bot_right = None
        self.bot_left = None
        self.top_left_color= 'yellow'
        self.top_right_color = 'red'
        self.bot_left_color = 'green'
        self.bot_right_color = 'blue'
        self.width = 193
        self.height = 188.5
        self.calibrationColor = "yellow"
        self.calibrated = True
        self.calibratedLeft = False
        self.calibratedRight = False

        self.detect_point = False
        self.point = [40, 100]
        self.diff_x = 0
        self.diff_y = 0

        self.left = [40, 100]
        self.top = [162, 42]
        self.real_left = []
        self.real_top = []
        self.diff_x = 0
        self.diff_y = 0
        
    # def getCircuitCoords(self, x, y):
    #     x_diff = abs(self.real_left[0] - self.real_top[0]) # tel coords
    #     y_diff = abs(self.real_left[1] - self.real_top[1])
    #     scaleX = x_diff / abs(self.left[0] - self.top[0]) # tel coords / fm coords = size of 1 square
    #     scaleY = y_diff / abs(self.left[1] - self.top[1])
    #     tel_origin = [self.real_left[0] + (200 - self.left[0]) * scaleX , self.real_left[1] - (200 - self.left[1]) * scaleY] # tel coords
    #     tel_origin_fm = [tel_origin[0] / scaleX , tel_origin[1] / scaleY] # fm coords
    #     newX = tel_origin_fm[0] - x / scaleX # fm coords
    #     newY = tel_origin_fm[1] + y / scaleY
    #     return [newX, newY]
    
    def getCircuitCoords(self, x, y):
        new_X = ((self.bot_right[0] - x) / abs(self.bot_right[0] - self.bot_left[0]) * self.width) + self.diff_x
        new_Y = ((y - self.bot_right[1]) / abs(self.bot_right[1] - self.top_right[1]) * self.height) + self.diff_y
        # print(self.bot_right[1], y, self.top_right[1])
        return new_X, new_Y
    
    def setupGrid(self, coordinates):
        coordinates.sort(key= lambda p : (p[1], p[0]))
        top = coordinates[2:]
        top.sort()
        self.top_left, self.top_right = top
        bot = coordinates[0:2]
        bot.sort()
        self.bot_left, self.bot_right = bot
        print(f"Grid Setup, top_left: {self.top_left}, top_right: {self.top_right}, bot_left: {self.bot_left}, bot_right: {self.bot_right}")
