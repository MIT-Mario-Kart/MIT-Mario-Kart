import time
import Car as c

def timer(sec):
    start_time = time.time()
    target_time = start_time + sec

    while time.time() < target_time:
        pass 

# recommended sec is 5
def speedup(mycar, sec): 
    prev = mycar.a
    mycar.a *= 1.2

    timer(sec)
    mycar.a = prev # or 1 idk

# recommended sec is 3
# intesity can go from 0 to 0.9 (0 -> freeze)
def slowdown(mycar, cars, intensity, sec): 
    prev = mycar.a
    for car in cars :
        car.a = intensity
    mycar.a = prev # or 1 idk

    timer(sec)
    for car in cars :
        car.a = 1


def inversion(cars, sec):
    for car in cars:
        if (c.isPlayer(car)):
            car.inverted = 1
            timer(sec)
            car.inverted = 0




    

