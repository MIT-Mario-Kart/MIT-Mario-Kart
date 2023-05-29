import pygame
from random import *
#import Algo.Control








class Game:
    finish_car = 0


    # Taille de la fenêtre
    LARGEUR_FENETRE = 1500
    HAUTEUR_FENETRE = 900





    def feu_start(self):
        if self.begin == 1:
            fenetre.blit(self.feu1, (x_feu, y_feu))
            if self.seconde_depart > 1:
                self.begin = 2

        elif self.begin == 2:
            fenetre.blit(self.feu2, (x_feu, y_feu))
            if self.seconde_depart > 2:
                self.begin = 3

        elif self.begin == 3:
            fenetre.blit(self.feu3, (x_feu, y_feu))
            if self.seconde_depart > 3:
                self.begin = 4

        elif self.begin == 4:
            fenetre.blit(self.feu4, (x_feu, y_feu))
            if self.seconde_depart > 4:
                self.begin = 5
                self.running = True
                self.start_time = pygame.time.get_ticks()

        elif self.begin == 5:
            fenetre.blit(self.feu5, (x_feu, y_feu))




    def gui_update(self):


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




