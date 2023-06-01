import pygame

pygame.init()

# Initialise le module joystick
pygame.joystick.init()

# Définit la taille de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Joysticks")

# Définit la police
font_size = 30
font = pygame.font.SysFont("Futura", font_size)

# Crée une horloge pour définir la fréquence d'images du jeu
clock = pygame.time.Clock()
FPS = 60

# Crée une liste vide pour stocker les manettes
joysticks = []

# Crée une liste de carrés pour chaque manette
squares = []

# Couleurs des carrés
colors = ["royalblue", "crimson", "fuchsia", "forestgreen"]

# Classe représentant un carré contrôlé par une manette
class Square:
    def __init__(self, joystick, color):
        self.joystick = joystick
        self.color = color
        self.rect = pygame.Rect(0, 0, 100, 100)

    def update(self):
        # Déplace le carré en fonction des entrées de la manette
        horiz_move = self.joystick.get_axis(0)
        vert_move = self.joystick.get_axis(1)

        if abs(horiz_move) > 0.05:
            self.rect.x += int(horiz_move * 5)
            print(horiz_move)
        if abs(vert_move) > 0.05:
            self.rect.y += int(vert_move * 5)

    def draw(self, surface):
        # Dessine le carré sur l'écran
        pygame.draw.rect(surface, pygame.Color(self.color), self.rect)

# Boucle principale du jeu
run = True
while run:
    clock.tick(FPS)

    # Met à jour l'arrière-plan
    screen.fill(pygame.Color("midnightblue"))

    # Gère les événements
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(event.device_index)
            joystick.init()
            joysticks.append(joystick)
            squares.append(Square(joystick, colors[len(joysticks) - 1]))

        elif event.type == pygame.QUIT:
            run = False

    # Met à jour les carrés et les dessine à l'écran
    for square in squares:
        square.update()
        square.draw(screen)

    # Met à jour l'affichage
    pygame.display.flip()

pygame.quit()
