import pygame

from Server.GUI.GUI_2 import GUI
from Server.Game.Player import Player


class Game:
    def __init__(self, car_list : list):
        self.car_list = car_list

        pygame.init()
        pygame.joystick.init()

        self.player_list = []
        for car in self.car_list:
            self.player_list.append(Player(car.name, car.ai, car.rank, car))

        self.gui = GUI()




