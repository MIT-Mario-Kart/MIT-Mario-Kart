import pygame

from Server.GUI.GUI_2 import GUI
from Server.Game.Player


class Game:
    def __init__(self, car_list : list):
        self.car_list = car_list

        pygame.init()
        pygame.joystick.init()

        self.player_list = []
        for cars in self.car_list:
            from Server.Game.Player import Player
            self.player_list.append(Player(cars.name, ))

        self.gui = GUI()




