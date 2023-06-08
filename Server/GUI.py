import random

import pygame
import Game

from Algo.Car import Car
from Algo.FlowMaps.circuit20x20 import directions as fmdir
# from Algo.Control import moveCar
import Algo.UpdateMovements as updateMov
from Algo.Control import cars
#from Algo.Control import rank_list
from Algo.Control import updateCarMovement
from Algo.Overtake.overtake import *
from Server.Algo import UpdateMovements
from Server.Algo.FlowMaps.GUi_FlowMaps import GUI_FlowMaps
from Server.Algo.GridOccupation import GridOccupation

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = Game.Game.GRIS_CLAIR

CAR_SIZE = 25

player1 = Game.Player("BLUE", False, 1, cars[0], 0)
player2 = Game.Player("RED", False, 2, cars[1], 1)
player3 = Game.Player("GREEN", False, 3, cars[2], 2)
#player4 = Game.Player("VIOLET", False, 4, cars[3],3)
#player5 = Game.Player("ROSE", False, 5, cars[4],4)
#player6 = Game.Player("BRUN", False, 6, cars[5],5)

players = [player1, player2, player3]

gameStarted = False
game = Game.Game(players)
game.gui_init()
screen = game.get_window()

SCALE = 2.75
# CIRCUIT_POS_X = 285
CIRCUIT_POS_X = 256
CIRCUIT_POS_Y = 203

MOVE_MAP_X = -100
MOVE_MAP_Y = 0

# # Set the window title
pygame.display.set_caption("Car Information")

# # Create a font for the text
font = pygame.font.Font(None, 36)

# # Load the image
image = pygame.image.load("../Image/circuit.jpeg")
# # Get the image size
image_width = image.get_width()
image_height = image.get_height()
# # Set the image position
image_x = 200  # 400 = screen center
image_y = 150  # 300 = screen center
image = pygame.transform.scale(image, (600, 600))

# # Set up the clock to control the frame rate
clock = pygame.time.Clock()

# # Loop until the user clicks the close button
done = False
on_the_line = False

# # Set the initial fullscreen state to False
# fullscreen = False
NB_CASE_OCCUPATION = 60

drawMap = GUI_FlowMaps(CIRCUIT_POS_X + MOVE_MAP_X, CIRCUIT_POS_Y + MOVE_MAP_Y, 532, screen, NB_CASE_OCCUPATION)

GridOccupation = GridOccupation(CIRCUIT_POS_X + MOVE_MAP_X, CIRCUIT_POS_Y + MOVE_MAP_Y, 532, NB_CASE_OCCUPATION)

while not done:

    for player in players:
        player.update(Game.Game.second)

    if game.running == True and gameStarted == False:
        gameStarted = True
        updateCarMovement()

    game.player_update()
    game.gui_update()

    # Update local variable guiCars
    guiCars = cars

    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Toggle fullscreen mode when the user presses the 'f' key
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(size)

    # --- Game logic should go here

    # --- Drawing code should go here
    # rect = pygame.Rect(0, 0, 20, 20)
    # pygame.draw.rect(screen, PALE_BLUE, rect, width=0)

    # Clear the screen to pale blue
    # screen.fill(GREY)

    # moveCar(guiCar)

    # Display the image on the screen
    screen.blit(image, (image_x + MOVE_MAP_X, image_y + MOVE_MAP_Y))

    # Draw the START line
    rect = pygame.Rect(350, 230, 20, 80)
    pygame.draw.rect(screen, BLACK, rect)

    # Draw checkpoint
    #rect = pygame.Rect(350, 630, 20, 80)
    #pygame.draw.rect(screen, BLACK, rect)
    # Loop through the cars and draw them and their information
    # Create a text string with the car's information
    Y_DISPLACEMENT = 25
    count = 0
    for car in guiCars:
        # text = "Car {0}: ({1}, {2}) - Orientation = {3} - Speed: {4} - Velocity: {5}".format(
        #   count, int(car.x), int(car.y), int(car.orientation), car.speed, car.velocity)
        # Render the text as a surface
        # text_surface = font.render(text, True, BLACK)

        # Text position
        # text_x = text_surface.get_width()/8
        # text_y = text_surface.get_height()/2 + count * Y_DISPLACEMENT

        # Draw the text on the screen
        # screen.blit(text_surface, [text_x, text_y])

        # Draw the car
        pygame.draw.rect(screen, car.colour, (MOVE_MAP_X + CIRCUIT_POS_X + (car.x) * SCALE - CAR_SIZE/2,
                                              MOVE_MAP_Y + CIRCUIT_POS_Y + (car.y) * SCALE - CAR_SIZE/2, CAR_SIZE, CAR_SIZE))

        if 340 < MOVE_MAP_X + CIRCUIT_POS_X + car.x * SCALE < 380 and 190 < MOVE_MAP_Y + CIRCUIT_POS_Y + car.y * SCALE < 310 and \
                players[count].on_the_line == False:
            players[count].add_lap()

            game.rank_update()
            i = 0
            for car_2 in guiCars:
                car_2.rank = players[i].rank
                i += 1

        if 270 < MOVE_MAP_X + CIRCUIT_POS_X + car.x * SCALE < 340 and 190 < MOVE_MAP_Y + CIRCUIT_POS_Y + car.y * SCALE < 500:
            players[count].not_on_the_line()


        if 340 < MOVE_MAP_X + CIRCUIT_POS_X + car.x * SCALE < 380 and 610 < MOVE_MAP_Y + CIRCUIT_POS_Y + car.y * SCALE < 730 and \
                players[count].on_the_line == False:

            #players[count].add_lap()

            game.rank_update()
            i = 0
            for car_2 in guiCars:
                car_2.rank = players[i].rank
                i += 1

        if  430 < MOVE_MAP_X + CIRCUIT_POS_X + car.x * SCALE < 500 and 610 < MOVE_MAP_Y + CIRCUIT_POS_Y + car.y * SCALE < 730:
            players[count].not_on_the_line()
        #game.rank_update()

        count = count + 1

        # GridOccupation.addBusy( car.x * SCALE, car.y * SCALE)

    #drawMap.drawGridFlow()
    #drawMap.drawVector()
    #drawMap.drawGridOccupation()
    #drawMap.drawBusyGrid(GridOccupation.busy_grid)
    GridOccupation.busy_grid = []

    y = 47
    for x in range(15, 30):
        GridOccupation.busy_grid.append((x,y))


    x = 12
    for y in range(17, 45):
        GridOccupation.busy_grid.append((x, y))


    y = 12
    for x in range(13, 49):
        GridOccupation.busy_grid.append((x, y))
    GridOccupation.resetBusy()

    #print(len(GridOccupation.busy_grid2))

    # --- Go ahead and update the screen
    pygame.display.update()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the PyGame window and quit
pygame.quit()
