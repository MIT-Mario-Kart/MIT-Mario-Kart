import math

from Server.Algo import Car, Control


class GridOccupation:
    busy_grid = []
    busy_grid2 = []
    old_busy_grid = []


    def __init__(self, pos_x, pos_y, width, nb_case):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.nb_case = nb_case
        self.case_width = width / nb_case
        self.old_busy_grid2 = [[0 for _ in range(nb_case)] for _ in range(nb_case)]

        y = 47
        for x in range(15,30):
            self.old_busy_grid2[x][y] = 1

        x = 12
        for y in range(17, 45):
            self.old_busy_grid2[x][y] = 1

        y = 12
        for x in range(13, 49):
            self.old_busy_grid2[x][y] = 1



    def addBusy(self, car_x, car_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width

        if self.isGridFree(x_grid, y_grid):
            self.busy_grid.append((x_grid, y_grid))

    def resetBusy(self):
        self.old_busy_grid2 = [[0 for _ in range(self.nb_case)] for _ in range(self.nb_case)]

        y = 47
        for x in range(15, 30):
            self.old_busy_grid2[x][y] = 1

        x = 12
        for y in range(17, 45):
            self.old_busy_grid2[x][y] = 1

        y = 12
        for x in range(13, 49):
            self.old_busy_grid2[x][y] = 1

        x = 57
        for y in range(0, 60):
            self.old_busy_grid2[x][y] = 1

        y = 2
        for x in range(0, 60):
            self.old_busy_grid2[x][y] = 1

        y = 57
        for x in range(0, 60):
            self.old_busy_grid2[x][y] = 1


    def addBusy2(self, car_x, car_y):
        x_grid = int(car_x // self.case_width)
        y_grid = int(car_y // self.case_width)

        if self.isGridFree2(x_grid, y_grid):
            self.old_busy_grid2[x_grid][y_grid] = 1

    def isGridFree(self, car_x, car_y):
        x_grid = int(car_x // self.case_width)
        y_grid = int(car_y // self.case_width)
        #print(x_grid)
        #print(y_grid)

        return not (x_grid, y_grid) in self.busy_grid

    def isGridFree2(self, car_x, car_y):
        x_grid = int(car_x // self.case_width)
        y_grid = int(car_y // self.case_width)
        #print(x_grid)
        #print(y_grid)


        return self.old_busy_grid2[x_grid][y_grid] == 0

    def sameGrid(self, car_x, car_y, car2_x, car2_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width
        x2_grid = car2_x // self.case_width
        y2_grid = car2_y // self.case_width

        return x_grid == x2_grid and y_grid == y2_grid

    def get_car_corners(self, center_x, center_y, angle, length, width):
        half_length = length / 2
        half_width = width / 2

        # Convert the angle from degrees to radians
        angle_rad = math.radians(angle)

        # Calculate the cosine and sine of the angle
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        # Calculate the coordinates of the four corners
        top_left = (center_x - half_length * cos_angle + half_width * sin_angle,
                    center_y - half_length * sin_angle - half_width * cos_angle)
        top_right = (center_x + half_length * cos_angle + half_width * sin_angle,
                     center_y + half_length * sin_angle - half_width * cos_angle)
        bottom_right = (center_x + half_length * cos_angle - half_width * sin_angle,
                        center_y + half_length * sin_angle + half_width * cos_angle)
        bottom_left = (center_x - half_length * cos_angle - half_width * sin_angle,
                       center_y - half_length * sin_angle + half_width * cos_angle)

        return top_left, top_right, bottom_right, bottom_left

    def setNextPositionOccupy2(self, car: Car):
        left = 0
        right = 0

        CAR_LENGHT = 30
        CAR_WIDTH = 16
        # LONGUEUR VOITURE 14cm
        # LARGEUR VOITURE 9CM

        MAX_STEERING_ANGLE = 25
        SEARCH = True

        SCALE = 2.75

        while SEARCH:
            while left < MAX_STEERING_ANGLE:
                carp_x_l = car.predicted_x
                carp_y_l = car.predicted_y
                carp_x_r = car.predicted_x
                carp_y_r = car.predicted_y

                carp_x_l += car.velocity * math.cos(math.radians(car.orientation + left))
                carp_y_l -= car.velocity * math.sin(math.radians(car.orientation + left))

                carp_x_r += car.velocity * math.cos(math.radians(car.orientation - right))
                carp_y_r -= car.velocity * math.sin(math.radians(car.orientation - right))

                side_l = self.get_car_corners(carp_x_l * SCALE, carp_y_l * SCALE, car.orientation + left, CAR_LENGHT, CAR_WIDTH)
                side_r = self.get_car_corners(carp_x_r * SCALE, carp_y_r * SCALE, car.orientation - right, CAR_LENGHT, CAR_WIDTH)

                allFree_l = self.isGridFree2(side_l[0][0], side_l[0][1]) and self.isGridFree2(side_l[1][0],
                                                                                              side_l[1][1]) \
                            and self.isGridFree2(side_l[2][0], side_l[2][1]) and self.isGridFree2(side_l[3][0],
                                                                                                  side_l[3][1])

                if allFree_l:

                    self.addBusy2(carp_x_l * SCALE, carp_y_l * SCALE)
                    self.addBusy2(side_l[0][0], side_l[0][1])
                    self.addBusy2(side_l[1][0], side_l[1][1])
                    self.addBusy2(side_l[2][0], side_l[2][1])
                    self.addBusy2(side_l[3][0], side_l[3][1])

                    self.addBusy(carp_x_l * SCALE, carp_y_l * SCALE)
                    self.addBusy(side_l[0][0], side_l[0][1])
                    self.addBusy(side_l[1][0], side_l[1][1])
                    self.addBusy(side_l[2][0], side_l[2][1])
                    self.addBusy(side_l[3][0], side_l[3][1])

                    car.predicted_x = carp_x_l
                    car.predicted_y = carp_y_l

                    list = self.get_rectangle_coordinates(carp_x_l * SCALE, carp_y_l * SCALE, CAR_WIDTH, CAR_LENGHT, car.orientation + left)

                    for l in list:
                        self.addBusy2(l[0], l[1])
                        self.addBusy(l[0], l[1])

                    SEARCH = False
                    break

                allFree_r = self.isGridFree2(side_r[0][0], side_r[0][1]) and self.isGridFree2(side_r[1][0],
                                                                                              side_r[1][1]) \
                            and self.isGridFree2(side_r[2][0], side_r[2][1]) and self.isGridFree2(side_r[3][0],
                                                                                                  side_r[3][1])

                if allFree_r:

                    self.addBusy2(carp_x_r * SCALE, carp_y_r * SCALE)
                    self.addBusy2(side_r[0][0], side_r[0][1])
                    self.addBusy2(side_r[1][0], side_r[1][1])
                    self.addBusy2(side_r[2][0], side_r[2][1])
                    self.addBusy2(side_r[3][0], side_r[3][1])

                    self.addBusy(carp_x_r * SCALE, carp_y_r * SCALE)
                    self.addBusy(side_r[0][0], side_r[0][1])
                    self.addBusy(side_r[1][0], side_r[1][1])
                    self.addBusy(side_r[2][0], side_r[2][1])
                    self.addBusy(side_r[3][0], side_r[3][1])

                    car.predicted_x = carp_x_r
                    car.predicted_y = carp_y_r

                    list = self.get_rectangle_coordinates(carp_x_r * SCALE, carp_y_r * SCALE, CAR_WIDTH, CAR_LENGHT,
                                                          car.orientation -right)

                    for l in list:
                        self.addBusy2(l[0], l[1])
                        self.addBusy(l[0], l[1])

                    SEARCH = False
                    break

                left += 1
                right += 1

            if car.velocity > 0.01:
                car.velocity -= 0.01

            left = 0
            right = 0





    def get_rectangle_coordinates(self, center_x, center_y, width, length, direction):
        # Calculer les coordonnées des coins du rectangle en fonction de sa taille
        half_width = width / 2
        half_length = length / 2

        # Calculer les angles de rotation en radians
        angle_rad = math.radians(direction)

        # Calculer les coordonnées des coins en fonction du centre et de l'angle de rotation
        top_left_x = center_x - half_width * math.cos(angle_rad) - half_length * math.sin(angle_rad)
        top_left_y = center_y - half_length * math.cos(angle_rad) + half_width * math.sin(angle_rad)
        top_right_x = center_x + half_width * math.cos(angle_rad) - half_length * math.sin(angle_rad)
        top_right_y = center_y - half_length * math.cos(angle_rad) - half_width * math.sin(angle_rad)
        bottom_left_x = center_x - half_width * math.cos(angle_rad) + half_length * math.sin(angle_rad)
        bottom_left_y = center_y + half_length * math.cos(angle_rad) + half_width * math.sin(angle_rad)
        bottom_right_x = center_x + half_width * math.cos(angle_rad) + half_length * math.sin(angle_rad)
        bottom_right_y = center_y + half_length * math.cos(angle_rad) - half_width * math.sin(angle_rad)

        # Arrondir les coordonnées pour obtenir des valeurs entières
        top_left_x = round(top_left_x)
        top_left_y = round(top_left_y)
        top_right_x = round(top_right_x)
        top_right_y = round(top_right_y)
        bottom_left_x = round(bottom_left_x)
        bottom_left_y = round(bottom_left_y)
        bottom_right_x = round(bottom_right_x)
        bottom_right_y = round(bottom_right_y)

        # Générer toutes les coordonnées occupées par le rectangle
        coordinates = []
        for x in range(min(top_left_x, top_right_x, bottom_left_x, bottom_right_x),
                       max(top_left_x, top_right_x, bottom_left_x, bottom_right_x) + 1):
            for y in range(min(top_left_y, top_right_y, bottom_left_y, bottom_right_y),
                           max(top_left_y, top_right_y, bottom_left_y, bottom_right_y) + 1):
                coordinates.append((x, y))

        return coordinates


