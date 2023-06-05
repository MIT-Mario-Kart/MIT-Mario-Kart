import threading

from MainServerClass import MainServer
from Algo.Car import Car, BLUE_C, RED_C, GREEN_C, ROSE_C
from Game.Game import Game
from Algo.Control import Control

# launch our MainServer instance on port 8899
def launch_server(control):
    server = MainServer(('', 8899), control)
    server.serve_forever()

# create all car objects corresponding to the real life cars
car1 = Car("CAR1", 1, "CAR_ID_1", GREEN_C, color="green", x=160, y=20, orientation=180, ai=True)
car2 = Car("CAR2", 2, "CAR_ID_2", RED_C, color="red", x=140, y=20, orientation=180, ai=False)
car3 = Car("CAR3", 2, "CAR_ID_3", ROSE_C, color="pink", x=140, y=20, orientation=180, ai=True)
car4 = Car("CAR4", 2, "CAR_ID_4", BLUE_C, color="blue", x=140, y=20, orientation=180, ai=False)


car_list = [car1, car2, car3, car4]
control = Control(car_list) # create an instance of Control, which will control all the cars created above
my_thread = threading.Thread(target=launch_server, args=[control])
my_thread.start() # we launch our server on a new thread because pygame needs to be on the main thread
game = Game(car_list, 11, control) # create an instance Game which will take care of managing everything related 
                                   # to the GUI and overall game information (ie. number of laps, rank of each car, ...)

while True:
    game.update()
