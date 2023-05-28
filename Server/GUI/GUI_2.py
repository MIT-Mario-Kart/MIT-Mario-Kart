import pygame

from Server.GUI.GUi_FlowMaps import GUI_FlowMaps
from Server.Algo.GridOccupation import GridOccupation


class GUI:
    #Color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)

    #
    SCALE = 2.75
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

    fenetre = None
    font = pygame.font.SysFont("Calibri", 28)
    # # Load the image
    image = pygame.image.load("../../Image/circuit.jpeg")

    def __init__(self):
        self.gui_init()




    def gui_init(self):
        # Initialize the window and the joysticks
        pygame.init()
        pygame.joystick.init()

        # Get the screen size
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        self.fenetre = pygame.display.set_mode((screen_width, screen_height))

        # # Set the window title
        pygame.display.set_caption("MIT KART")

        # # Get the image size
        image_width = self.image.get_width()
        image_height = self.image.get_height()
        # # Set the image position
        image_x = 200  # 400 = screen center
        image_y = 150  # 300 = screen center
        image = pygame.transform.scale(self.image, (600, 600))

        # # Set up the clock to control the frame rate
        clock = pygame.time.Clock()

        # # Loop until the user clicks the close button
        done = False
        on_the_line = False

        # # Set the initial fullscreen state to False
        # fullscreen = False
        NB_CASE_OCCUPATION = 60

        drawMap = GUI_FlowMaps(CIRCUIT_POS_X + MOVE_MAP_X, CIRCUIT_POS_Y + MOVE_MAP_Y, 532, screen, NB_CASE_OCCUPATION)

        GriOccupation = GridOccupation(CIRCUIT_POS_X + MOVE_MAP_X, CIRCUIT_POS_Y + MOVE_MAP_Y, 532, NB_CASE_OCCUPATION)

    def gui_update(self):
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN and self.running == False:
                if event.key == pygame.K_SPACE:
                    self.begin = 1
                    self.start_time_depart = pygame.time.get_ticks()

        # Effacement de l'écran
        self.fenetre.fill(self.GRIS_FONCE)

        x_feu = 300
        y_feu = 70

        if self.running:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.second = round(self.elapsed_time / 1000, 1)

        else:
            self.elapsed_time_depart = pygame.time.get_ticks() - self.start_time_depart
            self.seconde_depart = round(self.elapsed_time_depart / 1000, 1)

        if self.begin == 0:
            self.fenetre.blit(self.feu1, (x_feu, y_feu))

        if self.begin == 1:
            self.fenetre.blit(self.feu1, (x_feu, y_feu))
            if self.seconde_depart > 1:
                self.begin = 2

        if self.begin == 2:
            self.fenetre.blit(self.feu2, (x_feu, y_feu))
            if self.seconde_depart > 2:
                self.begin = 3

        if self.begin == 3:
            self.fenetre.blit(self.feu3, (x_feu, y_feu))
            if self.seconde_depart > 3:
                self.begin = 4

        if self.begin == 4:
            self.fenetre.blit(self.feu4, (x_feu, y_feu))
            if self.seconde_depart > 4:
                self.begin = 5
                self.running = True
                self.start_time = pygame.time.get_ticks()

        if self.begin == 5:
            self.fenetre.blit(self.feu5, (x_feu, y_feu))

        # Effacement de l'écran

        # Affichage des joueurs
        x = 700
        y = 130

        # Ligne d'en-tête
        pygame.draw.line(self.fenetre, self.GREY, (30 + x, y - 20), (self.LARGEUR_FENETRE - 30, y - 20), 2)

        pygame.draw.line(self.fenetre, self.GREY, (x, y - 20), (self.LARGEUR_FENETRE - 30, y - 20), 2)

        # Affichage du Temps
        temps_render = self.font.render(str(self.second), True, self.WHITE)
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




