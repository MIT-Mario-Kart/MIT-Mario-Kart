import pygame

from Algo.GridOccupation import GridOccupation
from GUI.GUI import GUI
import Manette

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

    def __init__(self, car_list: list, nb_lap, control):
        self.car_list = car_list
        self.nb_lap = nb_lap
        self.control = control

        pygame.init()
        pygame.joystick.init()



        self.grid_occupation = GridOccupation(GUI.CIRCUIT_POS_X + GUI.MOVE_MAP_X, GUI.CIRCUIT_POS_Y + GUI.MOVE_MAP_Y, 532,
                                         self.NB_CASE_OCCUPATION)

        self.gui = GUI(self.NB_CASE_OCCUPATION, self.nb_lap)



    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN and self.running == False:
                if event.key == pygame.K_SPACE:
                    self.begin = 1
                    self.start_time_depart = pygame.time.get_ticks()
            elif event.type == pygame.JOYDEVICEADDED:
                # print(f"New Manette conneted!")
                for car in self.car_list:
                    if not(car.ai) and not(car.joystick_connected):
                        joystick = pygame.joystick.Joystick(event.device_index)
                        joystick.init()
                        Manette.joysticks.append(joystick)

                        manette = Manette.Manette(joystick)
                        car.manette = manette
                        Manette.manettes.append(manette)
                        print(f"Manette added to {car.id}")
                        car.joystick_connected = True
                        break
            Manette.updateManette()

        if self.running:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.second = round(self.elapsed_time / 1000, 1)


            self.control.updateCarList(self.car_list)

            for car in self.car_list:
               if car.lap_count == self.nb_lap + 1:
                   car.finished = True
               car.update(self.second)
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
        self.rank_update()
        self.gui.gui_update(self.begin, self.second, self.car_list, self.grid_occupation.busy_grid)



        # --- Limit to 60 frames per second
        pygame.time.Clock().tick(60)

    def rank_update(self):
        new_car_list = []
        i = 1
        while len(self.car_list) != 0:
            min = self.car_list[0]
            for car in self.car_list:
                if car.curr_lap < min.curr_lap and car.lap_count >= min.lap_count \
                        or car.lap_count > min.lap_count:
                    min = car

            self.car_list.remove(min)
            new_car_list.append(min)
            min.rank = i

            i += 1

        self.car_list = new_car_list

