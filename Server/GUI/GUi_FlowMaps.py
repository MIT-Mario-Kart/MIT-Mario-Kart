import pygame
from Algo.FlowMaps.NewFlowMap import directions as vector


class GUI_FlowMaps:
    # Color
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    ARROW = pygame.image.load("../Image/Arrow.png")
    nb_case_flow = 20
    nb_case_flow_2 = 40


    def __init__(self, pos_x_map, pos_y_map, width, screen, nb_case_occupation):
        self.pos_x = pos_x_map
        self.pos_y = pos_y_map
        self.width = width
        self.screen = screen
        self.case_width_flow = width / self.nb_case_flow
        self.case_width_flow_2 = width / self.nb_case_flow_2
        self.case_width_occupation = width / nb_case_occupation
        self.ARROW = pygame.transform.scale(self.ARROW, (self.case_width_flow - 15, self.case_width_flow - 16))
        # self.ARROW = pygame.transform.scale(self.ARROW, (1, 1))
        # self.nb_case_flow = self.nb_case_flow
        self.nb_case_occupation = nb_case_occupation

    def drawGridFlow(self):
        for i in range(0, self.nb_case_flow + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x, self.pos_y + i * self.case_width_flow),
                             (self.pos_x + self.width, self.pos_y + i * self.case_width_flow), 2)

        for i in range(0, self.nb_case_flow + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x + i * self.case_width_flow, self.pos_y),
                             (self.pos_x + i * self.case_width_flow, self.pos_y + self.width), 2)

    def drawGridFlow_2(self):
        for i in range(0, self.nb_case_flow_2 + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x, self.pos_y + i * self.case_width_flow_2),
                             (self.pos_x + self.width, self.pos_y + i * self.case_width_flow_2), 2)

        for i in range(0, self.nb_case_flow_2 + 1):
            pygame.draw.line(self.screen, self.BLACK, (self.pos_x + i * self.case_width_flow_2, self.pos_y),
                             (self.pos_x + i * self.case_width_flow_2, self.pos_y + self.width), 2)

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
                rotated_arrow = pygame.transform.rotate(self.ARROW, vector[10*x][10*y] - 90)
                self.screen.blit(rotated_arrow, (self.pos_x + self.case_width_flow / 2 - 5 + x * self.case_width_flow,
                                                 self.pos_y + self.case_width_flow / 2 + y * self.case_width_flow - 3))
    def drawVector_40(self):
        for x in range(0, self.nb_case_flow_2):
            for y in range(0, self.nb_case_flow_2):
                rotated_arrow = pygame.transform.rotate(self.ARROW, vector[5*x][5*y] - 90)
                self.screen.blit(rotated_arrow, (self.pos_x + self.case_width_flow_2 / 2 - 5 + x * self.case_width_flow_2,
                                                 self.pos_y + self.case_width_flow_2 / 2 + y * self.case_width_flow_2 - 3))

    def drawBusyGrid(self, busy_list2):
        for busy_grid in busy_list2:
            x = busy_grid[0]
            y = busy_grid[1]

            pygame.draw.rect(self.screen, self.GREEN, (
            self.pos_x + x * self.case_width_occupation, self.pos_y + y * self.case_width_occupation,
            self.case_width_occupation, self.case_width_occupation))

    def drawCarOrientation(self, car_list):
        for car in car_list:
            rotated_arrow = pygame.transform.rotate(self.ARROW,  car.orientation - 90)
            self.screen.blit(rotated_arrow, (self.pos_x + car.x * 2.75 - 10,
                                             self.pos_y + car.y * 2.75 - 6))
