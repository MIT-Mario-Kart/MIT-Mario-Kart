import pygame

from Server.GUI.GUi_FlowMaps import GUI_FlowMaps
from Server.Algo.GridOccupation import GridOccupation


class GUI:
    # Color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)

    #
    SCALE = 2.75

    CAR_SIZE = 25

    # CIRCUIT_POS_X = 285
    CIRCUIT_POS_X = 256
    CIRCUIT_POS_Y = 203

    MOVE_MAP_X = -100
    MOVE_MAP_Y = 0

    x_feu = 210
    y_feu = 70
    # Image du feu de départ
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

    # Image PowerUp
    random = pygame.image.load("../Image/PowerUp/random.png")
    random = pygame.transform.scale(random, (30, 30))

    stop = pygame.image.load("../Image/PowerUp/stop.png")
    stop = pygame.transform.scale(stop, (30, 30))

    sens = pygame.image.load("../Image/PowerUp/sens.png")
    sens = pygame.transform.scale(sens, (30, 30))

    ralentir = pygame.image.load("../Image/PowerUp/ralentir.jpg")
    ralentir = pygame.transform.scale(ralentir, (30, 30))

    # # Load the image
    image_circuit = pygame.image.load("../../Image/circuit.jpeg")

    fenetre = None
    font = pygame.font.SysFont("Calibri", 28)
    # # Load the image
    image_circuit = pygame.image.load("../../Image/circuit.jpeg")

    screen_info = None
    screen_width = None
    screen_height = None

    def __init__(self):
        self.gui_init()

    def gui_init(self):
        # Get the screen size
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h

        self.fenetre = pygame.display.set_mode((self.screen_width, self.screen_height))

        # # Set the window title
        pygame.display.set_caption("MIT KART")

        # # Get the image size
        image_width = self.image_circuit.get_width()
        image_height = self.image_circuit.get_height()
        # # Set the image position
        image_x = 200  # 400 = screen center
        image_y = 150  # 300 = screen center
        image = pygame.transform.scale(self.image_circuit, (600, 600))

        # # Set up the clock to control the frame rate
        clock = pygame.time.Clock()

        # # Loop until the user clicks the close button
        done = False
        on_the_line = False

        # # Set the initial fullscreen state to False
        # fullscreen = False
        NB_CASE_OCCUPATION = 60

    def gui_update(self, begin, second, cars):
        # Effacement de l'écran
        self.fenetre.fill(self.GREY)

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

        pygame.draw.line(self.fenetre, self.WHITE, (x, y - 20), (self.screen_height - 30, y - 20), 2)

        # Affichage du Temps
        temps_render = self.font.render(str(second), True, self.WHITE)
        self.fenetre.blit(temps_render, (x + 570, y - 70))

        for i, joueur in enumerate(self.player_list):
            # Nom du joueur
            nom_joueur = self.font.render(joueur.name, True, self.WHITE)
            self.fenetre.blit(nom_joueur, (110 + x, y))

            # Position
            position = self.font.render(str(joueur.rank), True, self.WHITE)
            self.fenetre.blit(position, (50 + x, y))
            rect = pygame.Rect(40 + x, y - 5, 640, 40)
            pygame.draw.rect(self.fenetre, self.BLACK, rect, 2)

            # Temps au tour

            temps_tour = self.font.render(str(round(joueur.curr_lap, 3)), True, self.WHITE)
            self.fenetre.blit(temps_tour, (290 + x, y))

            # Meilleure temps
            temps_tour = self.font.render(str(joueur.best_lap), True, self.WHITE)
            self.fenetre.blit(temps_tour, (410 + x, y))

            # Nombre de tours
            tours = self.font.render(str(joueur.lap_count) + "/10", True, self.WHITE)
            self.fenetre.blit(tours, (540 + x, y))

            # PowerUp
            self.fenetre.blit(joueur.power, (635 + x, y))

            y += 50

        for car in cars:
            pygame.draw.rect(self.fenetre, car.colour,
                             (self.MOVE_MAP_X + self.CIRCUIT_POS_X + (car.x) * self.SCALE - self.CAR_SIZE / 2,
                              self.MOVE_MAP_Y + self.CIRCUIT_POS_Y + (car.y) * self.SCALE - self.CAR_SIZE / 2,
                              self.CAR_SIZE,
                              self.CAR_SIZE))

        # --- Go ahead and update the screen
        pygame.display.update()
