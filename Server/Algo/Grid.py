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
        self.width = 200
        self.height = 200

    def setupGrid(self, top_left, top_right, bot_left, bot_right):
        self.top_left = top_left
        self.top_right = top_right
        self.bot_left = bot_left
        self.bot_right = bot_right


        print(f"Grid Setup, top_left: {top_left}, top_right: {top_right}, bot_left: {bot_left}, bot_right: {bot_right}")

    def getCircuitCoords(self, x, y):
        new_X = (x - self.top_left[0]) / abs((self.top_right[0]) - self.top_left[0]) * self.width
        new_Y = (y - self.top_left[1]) / (abs(self.bot_left[1] - self.top_left[1])) * self.height
        return new_X, new_Y