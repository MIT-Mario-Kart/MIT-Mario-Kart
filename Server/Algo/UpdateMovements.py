import Algo.Car as Car
import math
from Algo.GridOccupation import GridOccupation

MAX_VELOCITY = 7
ANGLE_UNIT = 15

ANGLE_PRECISION = ANGLE_UNIT  # in degrees
FLOAT_PRECISION = 0.00005

MAX_ACC = 1
MAX_DECEL = -MAX_ACC
ACC_UNIT = 0.9  # it's normal for this to be > MAX_ACC

BRAKE = 0.0
USR = -1.0
RED_V = 0.4 * MAX_VELOCITY
BLUE_V = 0.8 * MAX_VELOCITY
GREEN_V = MAX_VELOCITY

SCALE = 2.75


# car: (...)
# desired_velocity: desired speed for the car (STOP, GREEN_V, BLUE_V, RED_V, USER_ACC)
# No return value
def updateCarMovement(car: Car, desired_velocity: float, grid):
    # Update orientation

    if not eqWithin(car.desired_orientation, 0, ANGLE_PRECISION):
        # print(f"desired_orientation: {car.desired_orientation}")
        # Turn right if fm_orientation < 0 (i.e. decrement angle)
        if car.desired_orientation < 0:
            car.orientation = modulo(car.orientation - ANGLE_UNIT, 360)
        # Else turn left (i.e. increment angle)
        else:
            car.orientation = modulo(car.orientation + ANGLE_UNIT, 360)

    # Update acceleration, velocity and finally coordinates

    if eqWithin(desired_velocity, BRAKE, FLOAT_PRECISION):

        # Start braking (user control or AI stopping)

        if car.velocity > 0:
            car.a = MAX_DECEL
        else:
            car.a = 0

        car.velocity = max(0, car.velocity + car.a)

    elif eqWithin(desired_velocity, RED_V, FLOAT_PRECISION):

        vDiff = RED_V - car.velocity
        if gtWithin(vDiff, 0, FLOAT_PRECISION):

            # RED_V is quicker than current velocity => accelerate

            # Update acceleration
            if car.a < 0:
                car.a = 0
            else:
                car.a = min(MAX_ACC, abs(MAX_VELOCITY - car.velocity) * ACC_UNIT)

            # Update velocity
            car.velocity = min(RED_V, car.velocity + car.a)


        elif gtWithin(-vDiff, 0, FLOAT_PRECISION):

            # RED_V is slower than current velocity => brake

            # Update acceleration
            if gtWithin(car.velocity, RED_V, FLOAT_PRECISION):
                car.a = MAX_DECEL
            else:
                car.a = 0

            # Update velocity
            car.velocity = max(RED_V, car.velocity + car.a)


    elif eqWithin(desired_velocity, BLUE_V, FLOAT_PRECISION):

        vDiff = BLUE_V - car.velocity
        if gtWithin(vDiff, 0, FLOAT_PRECISION):

            # RED_V is quicker than current velocity => accelerate

            # Update acceleration
            if car.a < 0:
                car.a = 0
            else:
                car.a = min(MAX_ACC, abs(MAX_VELOCITY - car.velocity) * ACC_UNIT)

            # Update velocity
            car.velocity = min(BLUE_V, car.velocity + car.a)


        elif gtWithin(-vDiff, 0, FLOAT_PRECISION):

            # RED_V is slower than current velocity => brake

            # Update acceleration
            if gtWithin(car.velocity, BLUE_V, FLOAT_PRECISION):
                car.a = MAX_DECEL
            else:
                car.a = 0

            # Update velocity
            car.velocity = max(BLUE_V, car.velocity + car.a)

    elif eqWithin(desired_velocity, GREEN_V, FLOAT_PRECISION):
        vDiff = GREEN_V - car.velocity
        if gtWithin(vDiff, 0, FLOAT_PRECISION):

            # GREEN_V is quicker than current velocity => accelerate

            # Update acceleration
            if car.a < 0:
                car.a = 0
            else:
                car.a = min(MAX_ACC, abs(MAX_VELOCITY - car.velocity) * ACC_UNIT)

            # Update velocity (only if car still isn't at GREEN_V yet)
            car.velocity = min(GREEN_V, car.velocity + car.a)

    elif eqWithin(desired_velocity, USR, FLOAT_PRECISION):

        # User only has accelerate/brake controls

        # Update acceleration
        car.a = min(MAX_ACC, abs(MAX_VELOCITY - car.velocity) * ACC_UNIT)

        # Update velocity
        car.velocity = min(MAX_VELOCITY, car.velocity + car.a)


    # grid.setNextPositionOccupy2(car)

    # grid.resetBusy()



# Returns only positive nb mod(base) 
def modulo(nb: int, base: int):
    remainder = nb % base
    if remainder < 0:
        return remainder + base
    else:
        return remainder


# Returns whether a > b within a certain range
def gtWithin(a: float, b: float, within: float):
    return (a - b) > within


def eqWithin(a: float, b: float, within: float):
    return abs(a - b) < within
