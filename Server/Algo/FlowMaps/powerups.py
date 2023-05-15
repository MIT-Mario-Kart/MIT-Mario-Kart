import time
import Car as c
import random

SLOW, NORMAL, FAST = range(3)

def timer(sec):
    start_time = time.time()
    target_time = start_time + sec

    while time.time() < target_time:
        pass 

# recommended sec is 5
def speedup(mycar, sec): 
    prev = mycar.a
    mycar.a = FAST

    timer(sec)
    mycar.a = NORMAL # or 1 idk

# recommended sec is 3
# intesity can go from 0 to 0.9 (0 -> freeze)
def slowdown(mycar, cars, sec): 
    prev = mycar.a
    for car in cars :
        car.a = SLOW
    mycar.a = prev # or 1 idk

    timer(sec)
    for car in cars :
        car.a = NORMAL


def inversion(cars, sec):
    for car in cars:
        if (not(car.ai)):
            car.inverted = 1
            timer(sec)
            car.inverted = 0


def powerUp(myCar, otherCars):
    pu = random.randint(0,2)
    match pu:
        case 0:
            speedup(myCar, 5)
        case 1:
            slowdown(myCar, otherCars, 5)
        case 2:
            inversion(otherCars, 5)
        case _:
            speedup(myCar, 5)
    




    
