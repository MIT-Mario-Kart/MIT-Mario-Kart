import pygame

from Server.Algo.GridOccupation import GridOccupation
from Server.GUI.GUI_2 import GUI
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

        self.player_list = []
        for car in self.car_list:
            self.car_list.append(Player(car.name, car.ai, car.rank, car))

        self.gui = GUI()

        grid_occupation = GridOccupation(GUI.CIRCUIT_POS_X + GUI.MOVE_MAP_X, GUI.CIRCUIT_POS_Y + GUI.MOVE_MAP_Y, 532,
                                         self.NB_CASE_OCCUPATION)

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

        self.gui.gui_update(self.begin, self.second, self.car_list)

