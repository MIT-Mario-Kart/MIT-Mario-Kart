import math

from Server.Algo import Car


class GridOccupation:
    busy_grid = []


    def __init__(self, pos_x, pos_y, width, nb_case):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.case_width = width / nb_case
        self.busy_grid2 = [[0]*nb_case]*nb_case
    def addBusy(self, car_x, car_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width

        if self.isGridFree(x_grid, y_grid):
            self.busy_grid.append((x_grid, y_grid))

    def addBusy2(self, car_x, car_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width

        if self.isGridFree(x_grid, y_grid):
            self.busy_grid2[x_grid][y_grid] = 1

    def isGridFree(self, car_x, car_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width

        return not (x_grid, y_grid) in self.busy_grid

    def isGridFree2(self, car_x, car_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width

        return self.busy_grid2[x_grid][y_grid] == 0

    def sameGrid(self, car_x, car_y, car2_x, car2_y):
        x_grid = car_x // self.case_width
        y_grid = car_y // self.case_width
        x2_grid = car2_x // self.case_width
        y2_grid = car2_y // self.case_width

        return x_grid == x2_grid and y_grid == y2_grid

    def setNextPositionOccupy(car: Car, grid, list_prediction: list, occupation_list: list):

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

                list_carp_l = []
                list_carp_r = []

                # x = carp_x_l * SCALE- OFFSET
                # y = carp_y_l  * SCALE- OFFSET
                # while x < carp_x_l * SCALE+ CAR_SIZE + OFFSET:
                #   while y < carp_y_l * SCALE + CAR_SIZE + OFFSET:
                #      list_carp_l.append((x,y))
                #     x += BOX_SIZE
                #    y += BOX_SIZE

                # while x < carp_x_r * SCALE + CAR_SIZE + OFFSET:
                # while y < carp_y_r * SCALE + CAR_SIZE + OFFSET:
                #   list_carp_r.append((x,y))
                #  x += BOX_SIZE
                # y += BOX_SIZE

                # for carp_l in list_carp_l:
                #   if not grid.isGridFree(carp_l[0], carp_l[1]):
                #      break
                # ALL_TRUE_L = True
                # print("l")

                # for carp_x_r in list_carp_r:
                #   if not grid.isGridFree(carp_x_r[0], carp_x_r[1]):
                #      break
                # ALL_TRUE_R = True
                # print("r")

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

                if grid.isGridFree(c1_l[0], c1_l[1]) and grid.isGridFree(c2_l[0], c2_l[1]) and grid.isGridFree(c3_l[0],
                                                                                                               c3_l[1]) \
                        and grid.isGridFree(c4_l[0], c4_l[1]) and grid.isGridFree(c5_l[0], c5_l[1]) \
                        and grid.isGridFree(c6_l[0], c6_l[1]) and grid.isGridFree(c7_l[0], c7_l[1]) \
                        and grid.isGridFree(c8_l[0], c8_l[1]) and grid.isGridFree(c9_l[0], c9_l[1]) \
                        and grid.isGridFree(c10_l[0], c10_l[1]) and grid.isGridFree(c11_l[0], c11_l[1]) \
                        and grid.isGridFree(c12_l[0], c12_l[1]):
                    # if ALL_TRUE_L:

                    list_prediction.append(carp_x_l)
                    list_prediction.append(carp_y_l)

                    car.predicted_x = carp_x_l
                    car.predicted_y = carp_y_l

                    # for carp in list_carp_l:
                    #   occupation_list.append(carp)
                    # print(occupation_list)
                    # print(carp)

                    # print("list")
                    # print(occupation_list)

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

                if grid.isGridFree(c1_r[0], c1_r[1]) and grid.isGridFree(c2_r[0], c2_r[1]) and grid.isGridFree(c3_r[0],
                                                                                                               c3_r[1]) \
                        and grid.isGridFree(c4_r[0], c4_r[1]) and grid.isGridFree(c5_r[0], c5_r[1]) \
                        and grid.isGridFree(c6_r[0], c6_r[1]) and grid.isGridFree(c7_r[0], c7_r[1]) \
                        and grid.isGridFree(c8_r[0], c8_r[1]) and grid.isGridFree(c9_r[0], c9_r[1]) \
                        and grid.isGridFree(c10_r[0], c10_r[1]) and grid.isGridFree(c11_r[0], c11_r[1]) \
                        and grid.isGridFree(c12_r[0], c12_r[1]):
                    # if ALL_TRUE_R:

                    list_prediction.append(carp_x_r)
                    list_prediction.append(carp_y_r)

                    car.predicted_x = carp_x_r
                    car.predicted_y = carp_y_r

                    # for carp in list_carp_r:
                    #   occupation_list.append(carp)
                    # print(occupation_list)
                    # print(carp)

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

        return list_prediction, occupation_list

        def setNextPositionOccupy2(car: Car, grid, list_prediction: list, occupation_list: list):
            a = 0