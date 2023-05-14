import pygame

from Algo.Car import Car
from Algo.FlowMaps.circuit20x20 import directions as fmdir
from Algo.Control import moveCar
import Algo.UpdateMovements as updateMov

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PALE_BLUE = (175, 215, 238)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

SCALE = 3.575

circuitPosX = 292
circuitPosY = 237

# List of cars
guiCar = Car(1, "s", 160, 20, 180, True)

# Initialize PyGame
pygame.init()

# Set the size of the window and create the screen
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# Set the window title
pygame.display.set_caption("Car Information")

# Create a font for the text
font = pygame.font.Font(None, 36)

# Load the image
image = pygame.image.load("circuit.jpeg")
# Get the image size
image_width = image.get_width()
image_height = image.get_height()
# Set the image position
image_x = 200 # 400 = screen center
image_y = 150 # 300 = screen center
image = pygame.transform.scale(image, (800, 800))

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Loop until the user clicks the close button
done = False

# Set the initial fullscreen state to False
fullscreen = False


while not done:
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

    # Clear the screen to white
    screen.fill(PALE_BLUE)

    # Loop through the cars and draw their information
    # Create a text string with the car's information
    text = "Car: ({0}, {1}) - Orientation = {2} - Speed: {3} - Velocity: {4}".format(
        int(guiCar.x), int(guiCar.y), int(guiCar.orientation), guiCar.speed, guiCar.velocity)

    # Render the text as a surface
    text_surface = font.render(text, True, BLACK)

    # Text position
    text_x = text_surface.get_width()/8
    text_y = text_surface.get_height()/2

    # Draw the text on the screen
    screen.blit(text_surface, [text_x, text_y])

    moveCar(guiCar)

    # Display the image on the screen
    screen.blit(image, (image_x, image_y))

    # Draw the car
    pygame.draw.circle(screen, (255, 0, 0), (circuitPosX + (guiCar.x)*SCALE, circuitPosY + (guiCar.y)*SCALE), 5)

    # --- Go ahead and update the screen
    pygame.display.update()

    # --- Limit to 60 frames per second
    clock.tick(4)

# Close the PyGame window and quit
pygame.quit()