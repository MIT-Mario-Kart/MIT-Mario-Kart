import time
import Algo.Car as c
import random
import datetime

SLOW = 180
NORMAL = 200
FAST = 220

def timer(sec):
    start_time = time.time()
    target_time = start_time + sec

    while time.time() < target_time:
        pass 

# recommended sec is 5
def speedup(mycar): 
    mycar.acc = FAST
# recommended sec is 3
# intesity can go from 0 to 0.9 (0 -> freeze)
""" def slowdown(mycar, cars, sec): 
    prev = mycar.a
    for car in cars :
        car.a = SLOW
    mycar.a = prev # or 1 idk

    timer(sec)
    for car in cars :
        car.a = NORMAL """

def slowdown(mycar): 
    
    mycar.acc = SLOW 



""" def inversion(cars, sec):
    for car in cars:
        if (not(car.ai)):
            car.inverted = 1
            timer(sec)
            car.inverted = 0 """

def inversion(myCar):
    myCar.inverted = -1



def powerUp(myCar):
    pu = random.randint(0,1)

    if pu == 0:
        slowdown(myCar)
        print("START POWERUP SLOW")

    elif pu==1:
        speedup(myCar)
        print("START POWERUP FAST")
    # else:
    #     inversion(myCar)
    myCar.startTime = datetime.datetime.now()

""" case 2:
        inversion(myCar, 5) """

    

