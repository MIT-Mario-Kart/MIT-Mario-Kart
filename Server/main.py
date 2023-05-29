from MainServerClass import MainServer
from Server.Algo.Car import Car, BLUE_C, RED_C, GREEN_C
from Server.Game.Game import Game

server = MainServer(('', 8893))
server.serve_forever()

car1 = Car("CAR1", "Test", "Test", ("172.20.10.6", 9999), BLUE_C, x=160, y=20, orientation=180)
car1.rank = 3
car2 = Car("CAR2", "Test", "Test", ("172.20.10.8", 9999), RED_C, x=140, y=20, orientation=180)
car2.rank = 2
car3 = Car("CAR3", "Test", "Test", ("172.20.10.8", 9999), GREEN_C, x=120, y=20, orientation=180)
car3.rank = 1

car_list = [car1, car2, car3]

game = Game(car_list)



while True:
    game.update()



