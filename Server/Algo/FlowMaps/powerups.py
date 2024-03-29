import time
import Algo.Car as c
import random
import datetime
STOP = 0
SLOW = 180
NORMAL = 200
FAST = 220

# canges mycar.acc so it gets faster
def speedup(mycar): 
    mycar.acc = FAST

# changes the acceleration of all the cars except mycar so they slow down
def slowdown(mycar, cars): 
    for car in cars :
        if car != mycar:
            car.acc = SLOW
        car.startTime = datetime.datetime.now()

# stops mycar
def stopCar(myCar):
    myCar.acc = STOP

# gets a random powerup for mycar (possibly impacting all cars)
def powerUp(myCar, cars):
    pu = random.randint(0,2)

    if pu == 0:
        slowdown(myCar, cars)
        print(f"START POWERUP SLOW {myCar.id}")
        myCar.powerup = "slow"

    elif pu==1:
        speedup(myCar)
        print(f"START POWERUP FAST {myCar.id}")
        myCar.powerup = "fast"
    elif pu==2:
        stopCar(myCar)
        print(f"START POWERUP STOP CAR {myCar.id}")
        myCar.powerup = "stop"
    myCar.startTime = datetime.datetime.now()  

