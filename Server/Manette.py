import pygame

pygame.init()

# Initialise le module joystick
pygame.joystick.init()

# Crée une liste vide pour stocker les manettes
joysticks = []

# Crée une liste de carrés pour chaque manette
squares = []

# Crée une horloge pour définir la fréquence d'images du jeu
clock = pygame.time.Clock()
FPS = 60

# Classe représentant un carré contrôlé par une manette
class Manette:
    def __init__(self, joystick):
        self.joystick = joystick

    def update(self):
        # Déplace le carré en fonction des entrées de la manette
        horiz_move = self.joystick.get_axis(0)
        x_button = self.joystick.get_axis(4)

        if abs(horiz_move) > 0.05:
            print(horiz_move)

        if self.joystick.get_button(0) == 1:
            print("a")

        if self.joystick.get_button(1) == 1:
            print("b")




# Boucle principale du jeu
run = True
while run:

    clock.tick(FPS)

    # Gère les événements
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(event.device_index)
            joystick.init()
            joysticks.append(joystick)
            squares.append(Manette(joystick))

        elif event.type == pygame.QUIT:
            run = False

    # Met à jour les carrés et les dessine à l'écran
    for square in squares:
        square.update()

pygame.quit()
