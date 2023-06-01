import pygame

# from Algo.Control import moveCar
from Algo.Control import cars
#from Algo.Control import rank_list
from Algo.Overtake.overtake import *
from Algo.FlowMaps.GUi_FlowMaps import GUI_FlowMaps
from Algo.GridOccupation import GridOccupation
import Manette
import Game
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = Server.Game.Game.GRIS_CLAIR

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
CAR_SIZE = 25

# # Set the window title
pygame.display.set_caption("Car Information")

# # Create a font for the text
font = pygame.font.Font(None, 36)

# # Load the image
image = pygame.image.load("../../Image/circuit.jpeg")
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
GridOccupation = GridOccupation(CIRCUIT_POS_X + MOVE_MAP_X, CIRCUIT_POS_Y + MOVE_MAP_Y, 532, NB_CASE_OCCUPATION)

class GUI:

    def __init__(self):
        self.start = False
    for player in players:
        player.update(Game.Game.second)

    def launchGUI(self, cars):
        player1 = Game.Player("BLUE", False, 1, cars[0], 0)
        # player2 = Game.Player("RED", False, 2, cars[1], 1)
        # player3 = Game.Player("GREEN", False, 3, cars[2], 2)
        #player4 = Game.Player("VIOLET", False, 4, cars[3],3)
        #player5 = Game.Player("ROSE", False, 5, cars[4],4)
        #player6 = Game.Player("BRUN", False, 6, cars[5],5)

        players = [player1]

        gameStarted = False
        game = Game.Game(players)
        game.gui_init()
        screen = game.get_window()


        # # Set the window title
        pygame.display.set_caption("Car Information")

        # # Create a font for the text
        font = pygame.font.Font(None, 36)

        # # Load the image
        image = pygame.image.load("circuit.jpeg")
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

    #drawMap.drawGridFlow()
    #drawMap.drawVector()
    drawMap.drawGridOccupation()
    drawMap.drawBusyGrid(GridOccupation.busy_grid)
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

                    players[count].add_lap()

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

            drawMap.drawGridFlow()
            drawMap.drawVector()
            # drawMap.drawGridOccupation()
            

            y = 47
            for x in range(15, 30):
               GridOccupation.busy_grid.append((x, y))

            x = 12
            for y in range(17, 45):
               GridOccupation.busy_grid.append((x, y))

            y = 12
            for x in range(13, 49):
               GridOccupation.busy_grid.append((x, y))

            x = 2
            for y in range(0, 60):
               GridOccupation.busy_grid.append((x, y))

            x = 57
            for y in range(0, 60):
               GridOccupation.busy_grid.append((x, y))

            y = 2
            for x in range(0, 60):
               GridOccupation.busy_grid.append((x, y))

            y = 57
            for x in range(0, 60):
               GridOccupation.busy_grid.append((x, y))
            drawMap.drawBusyGrid(GridOccupation.busy_grid)
            GridOccupation.resetBusy()
            GridOccupation.busy_grid = []

            #print(len(GridOccupation.busy_grid2))

            # --- Go ahead and update the screen
            pygame.display.update()

            # --- Limit to 60 frames per second
            clock.tick(60)

        # Close the PyGame window and quit
        pygame.quit()
