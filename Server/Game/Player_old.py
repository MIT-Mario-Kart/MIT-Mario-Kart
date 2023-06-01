
class Player:
    x = 0
    y = 0
    speed = 0
    #power = PowerUp.random
    curr_lap = 0
    last_lap = 0
    best_lap = 0
    lap_count = 0
    on_the_line = False

    def __init__(self, name, ai, rank, car_server, car_list_index):
        self.name = str(name)
        self.ai = bool(ai)
        self.rank = int(rank)
        self.car_server = car_server
        self.car_list_index = car_list_index

    def shuffle(self):
        self.power = choice(PowerUp.list_power)

    def add_lap(self):
        self.on_the_line = True
        self.lap_count += 1
        self.last_lap += self.curr_lap

        if self.curr_lap < self.best_lap:
            self.best_lap = round(self.curr_lap,3)

        elif self.best_lap == 0 and self.lap_count == 2:
            self.best_lap = round(self.curr_lap,3)

        self.curr_lap = 0

    def update(self, second):
        self.curr_lap = second - self.last_lap

    def not_on_the_line(self):
        self.on_the_line = False