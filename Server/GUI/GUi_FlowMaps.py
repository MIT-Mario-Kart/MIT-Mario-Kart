import pygame
from Server.Algo.FlowMaps.circuit20x20 import directions as vector


class GUI_FlowMaps:
    # Color
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    ARROW = pygame.image.load("../Image/Arrow.png")
    nb_case_flow = 20

    def __init__(self, pos_x_map, pos_y_map, width, screen, nb_case_occupation):
        self.pos_x = pos_x_map
        self.pos_y = pos_y_map
        self.width = width
        self.screen = screen
        self.case_width_flow = width / self.nb_case_flow
        self.case_width_occupation = width / nb_case_occupation
        self.ARROW = pygame.transform.scale(self.ARROW, (self.case_width_flow - 15, self.case_width_flow - 12))
        self.nb_case_flow = self.nb_case_flow
        self.nb_case_occupation = nb_case_occupation

    def drawGridFlow(self):
        for i in range(0, self.nb_case_flow + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x, self.pos_y + i * self.case_width_flow),
                             (self.pos_x + self.width, self.pos_y + i * self.case_width_flow), 2)

        for i in range(0, self.nb_case_flow + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x + i * self.case_width_flow, self.pos_y),
                             (self.pos_x + i * self.case_width_flow, self.pos_y + self.width), 2)

    def drawGridOccupation(self):
        for i in range(0, self.nb_case_occupation + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x, self.pos_y + i * self.case_width_occupation),
                             (self.pos_x + self.width, self.pos_y + i * self.case_width_occupation), 2)

        for i in range(0, self.nb_case_occupation + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x + i * self.case_width_occupation, self.pos_y),
                             (self.pos_x + i * self.case_width_occupation, self.pos_y + self.width), 2)

    def drawVector(self):
        for x in range(0, self.nb_case_flow):
            for y in range(0, self.nb_case_flow):
                rotated_arrow = pygame.transform.rotate(self.ARROW, vector[x][y] - 90)
                self.screen.blit(rotated_arrow, (self.pos_x + self.case_width_flow / 2 - 5 + x * self.case_width_flow,
                                                 self.pos_y + self.case_width_flow / 2 + y * self.case_width_flow - 3))

    def drawBusyGrid(self, busy_list2):
        for busy_grid in busy_list2:
            x = busy_grid[0]
            y = busy_grid[1]

            pygame.draw.rect(self.screen, self.GREEN, (
            self.pos_x + x * self.case_width_occupation, self.pos_y + y * self.case_width_occupation,
            self.case_width_occupation, self.case_width_occupation))
