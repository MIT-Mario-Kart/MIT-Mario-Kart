import pygame

from GUI.GUi_FlowMaps import GUI_FlowMaps
from Algo.GridOccupation import GridOccupation


class GUI:
    # Color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (120, 120, 120)

    SCALE = 2.75

    # Size of the car on the GUI
    CAR_SIZE = 25

    # Position of the circuit
    CIRCUIT_POS_X = 256
    CIRCUIT_POS_Y = 203

    # Map coordinate offset
    MOVE_MAP_X = -100 - 30
    MOVE_MAP_Y = 0

    # Coordinates of the start light
    x_feu = 210
    y_feu = 70
    # Load the images of the start light
    feu1 = pygame.image.load("../Image/Feu_Depart/Feu_1.png")
    feu1 = pygame.transform.scale(feu1, (x_feu, y_feu))
    feu2 = pygame.image.load("../Image/Feu_Depart/Feu_2.png")
    feu2 = pygame.transform.scale(feu2, (x_feu, y_feu))
    feu3 = pygame.image.load("../Image/Feu_Depart/Feu_3.png")
    feu3 = pygame.transform.scale(feu3, (x_feu, y_feu))
    feu4 = pygame.image.load("../Image/Feu_Depart/Feu_4.png")
    feu4 = pygame.transform.scale(feu4, (x_feu, y_feu))
    feu5 = pygame.image.load("../Image/Feu_Depart/Feu_5.png")
    feu5 = pygame.transform.scale(feu5, (x_feu, y_feu))

    # Load the images of the PowerUp
    random = pygame.image.load("../Image/PowerUp/random.png")
    random = pygame.transform.scale(random, (30, 30))

    stop = pygame.image.load("../Image/PowerUp/stop.png")
    stop = pygame.transform.scale(stop, (30, 30))

    sens = pygame.image.load("../Image/PowerUp/sens.png")
    sens = pygame.transform.scale(sens, (30, 30))

    ralentir = pygame.image.load("../Image/PowerUp/ralentir.jpg")
    ralentir = pygame.transform.scale(ralentir, (30, 30))

    speedup = pygame.image.load("../Image/PowerUp/speedup.jpg")
    speedup = pygame.transform.scale(speedup, (30, 30))

    fenetre = None
    font = None

    # Load the image of the circuit (image_circuit is used for debugging)
    #image_circuit = pygame.image.load("../Image/circuit.jpeg")
    image_circuit_2 = pygame.image.load("../Image/circuit_2.png")

    image_x = 200  # 400 = screen center
    image_y = 150  # 300 = screen center

    #image_circuit = pygame.transform.scale(image_circuit, (600, 600))
    image_circuit_2 = pygame.transform.scale(image_circuit_2, (515, 515))

    screen_info = None
    screen_width = None
    screen_height = None

    # Load the image of the end flag
    image_flag = pygame.image.load("../Image/drapeau.jpeg")
    image_flag = pygame.transform.scale(image_flag, (50, 30))

    # Load the background image
    image_fond = pygame.image.load("../Image/image_fond.jpg")

    def __init__(self, nb_case_occupation, nb_lap):
        self.gui_init(nb_case_occupation)
        self.nb_lap = nb_lap

    def gui_init(self, nb_case_occupation):
        # Get the screen size
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h

        self.fenetre = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont("Calibri", 28)

        # # Set the window title
        pygame.display.set_caption("MIT KART")

        self.image_fond = pygame.transform.scale(self.image_fond, (self.screen_width, self.screen_height))

        self.drawMap = GUI_FlowMaps(self.CIRCUIT_POS_X + self.MOVE_MAP_X, self.CIRCUIT_POS_Y + self.MOVE_MAP_Y, 532, self.fenetre, nb_case_occupation)

    def gui_update(self, begin, second, cars, busy_grid):

        # Effacement de l'écran
        #self.fenetre.fill(self.GREY)
        self.fenetre.blit(self.image_fond, (0, 0))

        # Display the image on the screen
        #self.fenetre.blit(self.image_circuit, (self.image_x + self.MOVE_MAP_X, self.image_y + self.MOVE_MAP_Y))
        self.fenetre.blit(self.image_circuit_2, (self.image_x + self.MOVE_MAP_X + 70, self.image_y + self.MOVE_MAP_Y + 60))

        # Affichage du feu de départ
        x_feu = 300
        y_feu = 70

        if begin == 0:
            self.fenetre.blit(self.feu1, (x_feu, y_feu))

        elif begin == 1:
            self.fenetre.blit(self.feu1, (x_feu, y_feu))

        elif begin == 2:
            self.fenetre.blit(self.feu2, (x_feu, y_feu))

        elif begin == 3:
            self.fenetre.blit(self.feu3, (x_feu, y_feu))

        elif begin == 4:
            self.fenetre.blit(self.feu4, (x_feu, y_feu))

        elif begin == 5:
            self.fenetre.blit(self.feu5, (x_feu, y_feu))

        # Affichage des joueurs
        x = 700
        y = 130

        # Ligne d'en-tête
        pygame.draw.line(self.fenetre, self.WHITE, (30 + x, y - 20), (self.screen_width - 30, y - 20), 2)

        # Draw the START line
        # rect = pygame.Rect(350, 230, 20, 80)
        # pygame.draw.rect(self.fenetre, self.BLACK, rect)

        # Affichage du Temps
        temps_render = self.font.render(str(second), True, self.BLACK)
        self.fenetre.blit(temps_render, (x + 570, y - 70))

        for i, car in enumerate(cars):
            # Nom du joueur
            nom_joueur = self.font.render(car.name, True, self.BLACK)
            self.fenetre.blit(nom_joueur, (110 + x, y))

            # Position
            position = self.font.render(str(car.rank), True, self.BLACK)
            self.fenetre.blit(position, (50 + x, y))
            rect = pygame.Rect(40 + x, y - 5, 640, 40)
            pygame.draw.rect(self.fenetre, self.BLACK, rect, 2)

            # Temps au tour
            temps_tour = self.font.render(str(round(car.curr_lap, 1)), True, self.BLACK)
            self.fenetre.blit(temps_tour, (290 + x, y))

            # Meilleure temps
            temps_tour = self.font.render(str(round(car.best_lap, 1)), True, self.BLACK)
            self.fenetre.blit(temps_tour, (410 + x, y))

            # Nombre de tours
            tours = self.font.render(str(car.lap_count) + "/" + str(self.nb_lap), True, self.BLACK)
            self.fenetre.blit(tours, (540 + x, y))

            # PowerUp
            #self.fenetre.blit(car.power, (635 + x, y))

            if car.finished:
                self.fenetre.blit(self.image_flag, (690 + x, y))
            elif car.powerup == "slow":
                self.fenetre.blit(self.ralentir, (635 + x, y))
            elif car.powerup == "fast":
                self.fenetre.blit(self.speedup, (635 + x, y))
            elif car.powerup == "stop":
                self.fenetre.blit(self.stop, (635 + x, y))



            y += 50

        for car in cars:
            pygame.draw.rect(self.fenetre, car.colour,
                             (self.MOVE_MAP_X + self.CIRCUIT_POS_X + (car.x) * self.SCALE - self.CAR_SIZE / 2,
                              self.MOVE_MAP_Y + self.CIRCUIT_POS_Y + (car.y) * self.SCALE - self.CAR_SIZE / 2,
                              self.CAR_SIZE,
                              self.CAR_SIZE))


        #GridOccupation.resetBusy()
        #self.drawMap.drawGridFlow()
        #self.drawMap.drawGridFlow_2()
        #self.drawMap.drawVector()
        #self.drawMap.drawVector_40()
        #self.drawMap.drawGridOccupation()
        #self.drawMap.drawBusyGrid(busy_grid)
        #self.drawMap.drawCarOrientation(cars)

        # --- Go ahead and update the screen
        pygame.display.update()

