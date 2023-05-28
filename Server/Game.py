import pygame
from random import *
#import Algo.Control








class Game:
    finish_car = 0

    # Couleurs
    NOIR = (0, 0, 0)
    GRIS_FONCE = (120, 120, 120)
    GRIS_CLAIR = (220, 220, 220)
    JAUNE = (255, 255, 254)

    # Taille de la fenêtre
    LARGEUR_FENETRE = 1500
    HAUTEUR_FENETRE = 900


    running = False
    begin = 0
    start_time = 0
    elapsed_time = 0
    second = 0
    seconde_depart = 0
    start_time_depart = 0
    elapsed_time_depart = 0
    checkpoint_list = []

    def __init__(self, player_list):
        self.player_list = list(player_list)

    # def car_calibration(self, player_list):
    #   for car in player_list:






    def player_update(self):
        for player in self.player_list:
            player.update(self.second)


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
        fenetre.fill(self.GRIS_FONCE)

        x_feu = 300
        y_feu = 70

        if self.running:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.second = round(self.elapsed_time / 1000, 1)

        else:
            self.elapsed_time_depart = pygame.time.get_ticks() - self.start_time_depart
            self.seconde_depart = round(self.elapsed_time_depart / 1000, 1)

        if self.begin == 0:
            fenetre.blit(self.feu1, (x_feu, y_feu))

        if self.begin == 1:
            fenetre.blit(self.feu1, (x_feu, y_feu))
            if self.seconde_depart > 1:
                self.begin = 2

        if self.begin == 2:
            fenetre.blit(self.feu2, (x_feu, y_feu))
            if self.seconde_depart > 2:
                self.begin = 3
                
        if self.begin == 3:
            fenetre.blit(self.feu3, (x_feu, y_feu))
            if self.seconde_depart > 3:
                self.begin = 4

        if self.begin == 4:
            fenetre.blit(self.feu4, (x_feu, y_feu))
            if self.seconde_depart > 4:
                self.begin = 5
                self.running = True
                self.start_time = pygame.time.get_ticks()

        if self.begin == 5:
            fenetre.blit(self.feu5, (x_feu, y_feu))

        # Effacement de l'écran

        # Affichage des joueurs
        x = 700
        y = 130

        # Ligne d'en-tête
        pygame.draw.line(fenetre, self.GRIS_CLAIR, (30 + x, y - 20), (self.LARGEUR_FENETRE - 30, y - 20), 2)
        
        pygame.draw.line(fenetre, self.GRIS_CLAIR, (x, y - 20), (self.LARGEUR_FENETRE - 30, y - 20), 2)    

        # Affichage du Temps
        temps_render = font.render(str(self.second), True, self.NOIR)
        fenetre.blit(temps_render, (x + 570, y - 70))

        for i, joueur in enumerate(self.player_list):
            # Nom du joueur
            nom_joueur = font.render(joueur.name, True, self.JAUNE)
            fenetre.blit(nom_joueur, (110 + x, y))

            # Position
            position = font.render(str(joueur.rank), True, self.JAUNE)
            fenetre.blit(position, (50 + x, y))
            rect = pygame.Rect(40 + x, y - 5, 640, 40)
            pygame.draw.rect(fenetre, self.NOIR, rect, 2)

            # Temps au tour

            temps_tour = font.render(str(round(joueur.curr_lap, 3)), True, self.JAUNE)
            fenetre.blit(temps_tour, (290 + x, y))


            # Meilleure temps
            temps_tour = font.render(str(joueur.best_lap), True, self.JAUNE)
            fenetre.blit(temps_tour, (410 + x, y))

            # Nombre de tours
            tours = font.render(str(joueur.lap_count) + "/10", True, self.JAUNE)
            fenetre.blit(tours, (540 + x, y))

            # PowerUp
            fenetre.blit(joueur.power, (635 + x, y))


            y += 50


    def begin_game(self):
        global time
        time = 0

        self.gui_init()

        while self.finish_car < len(self.player_list):

            for player in self.player_list:
                player.update(self.second)

            self.gui_update()

            time += 0.001
            
            print("FIN de la game")
            
            
    def get_window(self):
        return fenetre

    def rank_update(self):
        new_player_list = []
        new_car_list = []
        i = 1
        while len(self.player_list) != 0:
            min : Player = self.player_list[0]
            for player in self.player_list:
                if player.curr_lap < min.curr_lap and player.lap_count > min.lap_count \
                        or player.lap_count > min.lap_count:
                    min = player

            self.player_list.remove(min)
            new_player_list.append(min)
            new_car_list.append(min.car_server)
            min.rank = i

            i += 1

        self.player_list = new_player_list

        return




