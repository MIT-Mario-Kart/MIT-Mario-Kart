import math

from Algo import Car, Control


class GridOccupation:
    busy_grid = []

    def __init__(self, pos_x, pos_y, width, nb_case):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.case_width = width / nb_case
        self.busy_grid2 = [[0] * nb_case] * nb_case

    def addBusy(self, car_x, car_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width

        if self.isGridFree(x_grid, y_grid):
            self.busy_grid.append((x_grid, y_grid))

    def addBusy2(self, car_x, car_y):
        x_grid = int(car_x // self.case_width)
        y_grid = int(car_y // self.case_width)

        if self.isGridFree(x_grid, y_grid):
            self.busy_grid2[x_grid][y_grid] = 1

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


        return self.busy_grid2[x_grid][y_grid] == 0

    def sameGrid(self, car_x, car_y, car2_x, car2_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width
        x2_grid = car2_x // self.case_width
        y2_grid = car2_y // self.case_width

        return x_grid == x2_grid and y_grid == y2_grid

    def setNextPositionOccupy(self, car: Car):

        left = 0
        right = 0

        CAR_SIZE = 25
        BOX_SIZE = 0.55

        CAR_LENGHT = 25
        CAR_WIDTH = 16
        # LONGUEUR VOITURE 14cm
        # LARGEUR VOITURE 9CM

        # OFFSET = 1
        # ALL_TRUE_L = False
        # ALL_TRUE_R = False

        MAX_STEERING_ANGLE = 25
        SEARCH = True

        SCALE = 2.75

        occupation_list = []

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

                c1_l = (carp_x_l * SCALE - BOX_SIZE, carp_y_l * SCALE + CAR_SIZE / 2)
                c2_l = (carp_x_l * SCALE - BOX_SIZE, carp_y_l * SCALE - CAR_SIZE / 2)
                c3_l = (carp_x_l * SCALE + CAR_SIZE / 2, carp_y_l * SCALE - BOX_SIZE)
                c4_l = (carp_x_l * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_l * SCALE - BOX_SIZE)
                c5_l = (carp_x_l * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_l * SCALE + CAR_SIZE / 2)
                c6_l = (carp_x_l * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_l * SCALE + CAR_SIZE + BOX_SIZE)
                c7_l = (carp_x_l * SCALE + CAR_SIZE / 2, carp_y_l * SCALE + CAR_SIZE + BOX_SIZE)
                c8_l = (carp_x_l * SCALE - BOX_SIZE, carp_y_l * SCALE + CAR_SIZE + BOX_SIZE)
                c9_l = (carp_x_l * SCALE + CAR_SIZE / 2, carp_y_l * SCALE - CAR_SIZE / 2)
                c10_l = (carp_x_l * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_l * SCALE - BOX_SIZE)
                c11_l = (carp_x_l * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_l * SCALE + CAR_SIZE / 2)
                c12_l = (carp_x_l * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_l * SCALE + CAR_SIZE + BOX_SIZE)

                c1_r = (carp_x_r * SCALE - BOX_SIZE, carp_y_r * SCALE + CAR_SIZE / 2)
                c2_r = (carp_x_r * SCALE - BOX_SIZE, carp_y_r * SCALE - CAR_SIZE / 2)
                c3_r = (carp_x_r * SCALE + CAR_SIZE / 2, carp_y_r * SCALE - BOX_SIZE)
                c4_r = (carp_x_r * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_r * SCALE - BOX_SIZE)
                c5_r = (carp_x_r * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_r * SCALE + CAR_SIZE / 2)
                c6_r = (carp_x_r * SCALE + CAR_SIZE + 4 * BOX_SIZE, carp_y_r * SCALE + CAR_SIZE + BOX_SIZE)
                c7_r = (carp_x_r * SCALE + CAR_SIZE / 2, carp_y_r * SCALE + CAR_SIZE + BOX_SIZE)
                c8_r = (carp_x_r * SCALE - BOX_SIZE, carp_y_r * SCALE + CAR_SIZE + BOX_SIZE)
                c9_r = (carp_x_r * SCALE + CAR_SIZE / 2, carp_y_r * SCALE - CAR_SIZE / 2)
                c10_r = (carp_x_l * SCALE + CAR_SIZE + 3 * BOX_SIZE, carp_y_l * SCALE - BOX_SIZE)
                c11_r = (carp_x_l * SCALE + CAR_SIZE + 3 * BOX_SIZE, carp_y_l * SCALE + CAR_SIZE / 2)
                c12_r = (carp_x_l * SCALE + CAR_SIZE + 3 * BOX_SIZE, carp_y_l * SCALE + CAR_SIZE + BOX_SIZE)

                if self.isGridFree(c1_l[0], c1_l[1]) and self.isGridFree(c2_l[0], c2_l[1]) and self.isGridFree(c3_l[0],
                                                                                                               c3_l[1]) \
                        and self.isGridFree(c4_l[0], c4_l[1]) and self.isGridFree(c5_l[0], c5_l[1]) \
                        and self.isGridFree(c6_l[0], c6_l[1]) and self.isGridFree(c7_l[0], c7_l[1]) \
                        and self.isGridFree(c8_l[0], c8_l[1]) and self.isGridFree(c9_l[0], c9_l[1]) \
                        and self.isGridFree(c10_l[0], c10_l[1]) and self.isGridFree(c11_l[0], c11_l[1]) \
                        and self.isGridFree(c12_l[0], c12_l[1]):

                    #car.predicted_x = carp_x_l
                    #car.predicted_y = carp_y_l
                    Control.calculateDeltaCar(car.orientation + left)

                    occupation_list.append((c1_l[0], c1_l[1]))
                    occupation_list.append((c2_l[0], c2_l[1]))
                    occupation_list.append((c3_l[0], c3_l[1]))
                    occupation_list.append((c4_l[0], c4_l[1]))
                    occupation_list.append((c5_l[0], c5_l[1]))
                    occupation_list.append((c6_l[0], c6_l[1]))
                    occupation_list.append((c7_l[0], c7_l[1]))
                    occupation_list.append((c8_l[0], c8_l[1]))
                    occupation_list.append((c9_l[0], c9_l[1]))
                    occupation_list.append((c10_l[0], c10_l[1]))
                    occupation_list.append((c11_l[0], c11_l[1]))
                    occupation_list.append((c12_l[0], c12_l[1]))

                    SEARCH = False
                    break

                if self.isGridFree(c1_r[0], c1_r[1]) and self.isGridFree(c2_r[0], c2_r[1]) and self.isGridFree(c3_r[0],
                                                                                                               c3_r[1]) \
                        and self.isGridFree(c4_r[0], c4_r[1]) and self.isGridFree(c5_r[0], c5_r[1]) \
                        and self.isGridFree(c6_r[0], c6_r[1]) and self.isGridFree(c7_r[0], c7_r[1]) \
                        and self.isGridFree(c8_r[0], c8_r[1]) and self.isGridFree(c9_r[0], c9_r[1]) \
                        and self.isGridFree(c10_r[0], c10_r[1]) and self.isGridFree(c11_r[0], c11_r[1]) \
                        and self.isGridFree(c12_r[0], c12_r[1]):
                    # if ALL_TRUE_R:

                    #car.predicted_x = carp_x_r
                    #car.predicted_y = carp_y_r
                    car.pred_orientation = car.orientation + right
                    Control.calculateDeltaCar(car)

                    occupation_list.append((c1_r[0], c1_r[1]))
                    occupation_list.append((c2_r[0], c2_r[1]))
                    occupation_list.append((c3_r[0], c3_r[1]))
                    occupation_list.append((c4_r[0], c4_r[1]))
                    occupation_list.append((c5_r[0], c5_r[1]))
                    occupation_list.append((c6_r[0], c6_r[1]))
                    occupation_list.append((c7_r[0], c7_r[1]))
                    occupation_list.append((c8_r[0], c8_r[1]))
                    occupation_list.append((c9_r[0], c9_r[1]))
                    occupation_list.append((c10_r[0], c10_r[1]))
                    occupation_list.append((c11_r[0], c11_r[1]))
                    occupation_list.append((c12_r[0], c12_r[1]))

                    SEARCH = False
                    break

                left += 1
                right += 1

            if car.velocity > 0.01:
                car.velocity -= 0.01

            left = 0
            right = 0

        for coor in occupation_list:
            self.addBusy(coor[0], coor[1])

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

        CAR_SIZE = 25
        BOX_SIZE = 0.55

        CAR_LENGHT = 25
        CAR_WIDTH = 16
        # LONGUEUR VOITURE 14cm
        # LARGEUR VOITURE 9CM

        # OFFSET = 1
        # ALL_TRUE_L = False
        # ALL_TRUE_R = False

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
                    self.addBusy2(side_l[0][0], side_l[0][1])
                    self.addBusy2(side_l[1][0], side_l[1][1])
                    self.addBusy2(side_l[2][0], side_l[2][1])
                    self.addBusy2(side_l[3][0], side_l[3][1])

                    self.addBusy(side_l[0][0], side_l[0][1])
                    self.addBusy(side_l[1][0], side_l[1][1])
                    self.addBusy(side_l[2][0], side_l[2][1])
                    self.addBusy(side_l[3][0], side_l[3][1])

                    SEARCH = False
                    break

                allFree_r = self.isGridFree2(side_r[0][0], side_r[0][1]) and self.isGridFree2(side_r[1][0],
                                                                                              side_r[1][1]) \
                            and self.isGridFree2(side_r[2][0], side_r[2][1]) and self.isGridFree2(side_r[3][0],
                                                                                                  side_r[3][1])

                if allFree_r:
                    self.addBusy2(side_r[0][0], side_r[0][1])
                    self.addBusy2(side_r[1][0], side_r[1][1])
                    self.addBusy2(side_r[2][0], side_r[2][1])
                    self.addBusy2(side_r[3][0], side_r[3][1])

                    self.addBusy(side_r[0][0], side_r[0][1])
                    self.addBusy(side_r[1][0], side_r[1][1])
                    self.addBusy(side_r[2][0], side_r[2][1])
                    self.addBusy(side_r[3][0], side_r[3][1])

                    SEARCH = False
                    break

                left += 1
                right += 1

            if car.velocity > 0.01:
                car.velocity -= 0.01

            left = 0
            right = 0

            #for b in self.busy_grid2:
            #    print(b)

            print("fin")

    def is_point_inside_quadrilateral(self, A, B, C, D, P):
        AB = {'x': B['x'] - A['x'], 'y': B['y'] - A['y']}
        BC = {'x': C['x'] - B['x'], 'y': C['y'] - B['y']}
        CD = {'x': D['x'] - C['x'], 'y': D['y'] - C['y']}
        DA = {'x': A['x'] - D['x'], 'y': A['y'] - D['y']}
        AP = {'x': P['x'] - A['x'], 'y': P['y'] - A['y']}
        BP = {'x': P['x'] - B['x'], 'y': P['y'] - B['y']}
        CP = {'x': P['x'] - C['x'], 'y': P['y'] - C['y']}
        DP = {'x': P['x'] - D['x'], 'y': P['y'] - D['y']}

        product_AB_AP = AB['x'] * AP['y'] - AB['y'] * AP['x']
        product_BC_BP = BC['x'] * BP['y'] - BC['y'] * BP['x']
        product_CD_CP = CD['x'] * CP['y'] - CD['y'] * CP['x']
        product_DA_DP = DA['x'] * DP['y'] - DA['y'] * DP['x']

        return (product_AB_AP >= 0 and product_BC_BP >= 0 and product_CD_CP >= 0 and product_DA_DP >= 0) or \
            (product_AB_AP <= 0 and product_BC_BP <= 0 and product_CD_CP <= 0 and product_DA_DP <= 0)

    def setNextPositionOccupy3(self, car: Car):
        left = 0
        right = 0

        CAR_SIZE = 25
        BOX_SIZE = 0.55

        CAR_LENGHT = 25
        CAR_WIDTH = 16
        # LONGUEUR VOITURE 14cm
        # LARGEUR VOITURE 9CM

        # OFFSET = 1
        # ALL_TRUE_L = False
        # ALL_TRUE_R = False

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

                side_l = self.get_car_corners(carp_x_l, carp_y_l, car.orientation + left, CAR_LENGHT, CAR_WIDTH)
                side_r = self.get_car_corners(carp_x_r, carp_y_r, car.orientation - right, CAR_LENGHT, CAR_WIDTH)

                A_1 = {'x': side_l[0][0], 'y': side_l[0][1]}
                A_2 = {'x': side_l[1][0], 'y': side_l[1][1]}
                A_3 = {'x': side_l[2][0], 'y': side_l[2][1]}
                A_4 = {'x': side_l[3][0], 'y': side_l[3][1]}

                B = {'x': 5, 'y': 0}
                C = {'x': 5, 'y': 5}
                D = {'x': 0, 'y': 5}
                P = {'x': 2, 'y': 2}

                all_free_l = self.is_point_inside_quadrilateral(A_1, B, C, D, P) and self.is_point_inside_quadrilateral(
                    A_2, B, C, D, P) and self.is_point_inside_quadrilateral(A_3, B, C, D,
                                                                            P) and self.is_point_inside_quadrilateral(
                    A_4, B, C, D, P)
