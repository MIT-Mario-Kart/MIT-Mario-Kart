import pygame

# pygame.init()

# Initialise le module joystick
# pygame.joystick.init()



# Crée une liste vide pour stocker les manettes
joysticks = []

# Crée une liste de carrés pour chaque manette
manettes = []

# Crée une horloge pour définir la fréquence d'images du jeu
# clock = pygame.time.Clock()
# FPS = 60

# Classe représentant un carré contrôlé par une manette
class Manette:
    def __init__(self, joystick):
        self.joystick = joystick
        self.forward = 0
        self.horiz_move = 0
        self.backward = 0
    def update(self):
        # Déplace le carré en fonction des entrées de la manette
        self.horiz_move = -self.joystick.get_axis(0)
        # x_button = self.joystick.get_axis(4)

        if abs(self.horiz_move) > 0.05:
            # print(horiz_move)
            pass

        if self.joystick.get_button(1) == 1:
            #print("a")
            self.forward = 1
        else :
            self.forward = 0

        if self.joystick.get_button(0) == 1:
            #print("b")
            self.backward = 1
        else : 
            self.backward = 0





def updateManette():

    # Met à jour les carrés et les dessine à l'écran
    for manette in manettes:
        # print("Updated manette")
        manette.update()
