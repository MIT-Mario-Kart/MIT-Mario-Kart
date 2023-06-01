import threading

from MainServerClass import MainServer
from Algo.Car import Car, BLUE_C, RED_C, GREEN_C
from Game.Game import Game
from Algo.Control import Control

def launch_server(control):
    server = MainServer(('', 8899), control)
    server.serve_forever()

car1 = Car("CAR1", 1, "CAR_ID_1", GREEN_C, color="green", x=160, y=20, orientation=180, ai=True)
car2 = Car("CAR2", 2, "CAR_ID_2", RED_C, color="red", x=140, y=20, orientation=180, ai=True)

car_list = [car1, car2]
control = Control(car_list)
my_thread = threading.Thread(target=launch_server, args=[control])
my_thread.start()
game = Game(car_list, 11, control)

while True:
    game.update()
