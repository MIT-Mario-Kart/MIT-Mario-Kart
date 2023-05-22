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
        self.width = 190
        self.height = 185

    def getCircuitCoords(self, x, y):
        new_X = ((self.bot_right[0] - x) / abs(self.bot_right[0] - self.bot_left[0]) * self.width) + 5
        new_Y = ((y - self.bot_right[1]) / abs(self.bot_right[1] - self.top_right[1]) * self.height) + 5
        print(self.bot_right[1], y, self.top_right[1])
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
