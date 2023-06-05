import time
import Algo.Car as c
import random
import datetime
STOP = 0
SLOW = 180
NORMAL = 200
FAST = 220

def speedup(mycar): 
    mycar.a = FAST

# intensity can go from 0 to 0.9 (0 -> freeze)
def slowdown(mycar, cars): 
    for car in cars :
        if car != mycar:
            car.a = SLOW
        car.startTime = datetime.datetime.now()

def stopCar(myCar):
    myCar.a = STOP

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

