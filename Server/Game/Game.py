import pygame

from Server.Algo.Control import updateCarMovement, updateCarList
from Server.Algo.GridOccupation import GridOccupation
from Server.GUI.GUI import GUI
from Server.Game.Player import Player


class Game:
    running = False
    begin = 0
    start_time = 0
    elapsed_time = 0
    second = 0
    seconde_depart = 0
    start_time_depart = 0
    elapsed_time_depart = 0

    NB_CASE_OCCUPATION = 60

    def __init__(self, car_list: list):
        self.car_list = car_list

        pygame.init()
        pygame.joystick.init()



        self.grid_occupation = GridOccupation(GUI.CIRCUIT_POS_X + GUI.MOVE_MAP_X, GUI.CIRCUIT_POS_Y + GUI.MOVE_MAP_Y, 532,
                                         self.NB_CASE_OCCUPATION)

        self.gui = GUI(self.NB_CASE_OCCUPATION)



    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN and self.running == False:
                if event.key == pygame.K_SPACE:
                    self.begin = 1
                    self.start_time_depart = pygame.time.get_ticks()

        if self.running:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.second = round(self.elapsed_time / 1000, 1)

            updateCarList(self.car_list)
            #updateCarMovement()

        else:
            self.elapsed_time_depart = pygame.time.get_ticks() - self.start_time_depart
            self.seconde_depart = round(self.elapsed_time_depart / 1000, 1)

        if self.begin == 1:
            if self.seconde_depart > 1:
                self.begin = 2

        elif self.begin == 2:
            if self.seconde_depart > 2:
                self.begin = 3

        elif self.begin == 3:
            if self.seconde_depart > 3:
                self.begin = 4

        elif self.begin == 4:
            if self.seconde_depart > 4:
                self.begin = 5
                self.running = True
                self.start_time = pygame.time.get_ticks()

        # --- Limit to 60 frames per second
        pygame.time.Clock().tick(60)

        y = 47
        for x in range(15, 30):
            self.grid_occupation.busy_grid.append((x, y))

        x = 12
        for y in range(17, 45):
            self.grid_occupation.busy_grid.append((x, y))

        y = 12
        for x in range(13, 49):
            self.grid_occupation.busy_grid.append((x, y))

        x = 2
        for y in range(0, 60):
            self.grid_occupation.busy_grid.append((x, y))

        x = 57
        for y in range(0, 60):
            self.grid_occupation.busy_grid.append((x, y))

        y = 2
        for x in range(0, 60):
            self.grid_occupation.busy_grid.append((x, y))

        y = 57
        for x in range(0, 60):
            self.grid_occupation.busy_grid.append((x, y))


        #self.grid_occupation.resetBusy()
        self.gui.gui_update(self.begin, self.second, self.car_list, self.grid_occupation.busy_grid)
        self.rank_update()



    def rank_update(self):
        new_car_list = []
        i = 1
        while len(self.car_list) != 0:
            min : Player = self.car_list[0]
            for car in self.car_list:
                if car.curr_lap < min.curr_lap and car.lap_count > min.lap_count \
                        or car.lap_count > min.lap_count:
                    min = car

            self.car_list.remove(min)
            new_car_list.append(min)
            min.rank = i

            i += 1

        self.car_list = new_car_list


        return