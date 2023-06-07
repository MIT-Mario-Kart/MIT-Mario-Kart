import threading
import json
import re
import ast

from Algo.Car import Car
from Algo.FlowMaps.NewFlowMap import directions as fmdir
import Algo.FlowMaps.powerups as pu
from Algo.Grid import Grid
import Algo.UpdateMovements as updateMov
import datetime
import Algo.overtake as ovt
# constant definitions
POWERUP = '1'
POWERUP_TIME = 5

RED = '2'
GREEN = '3'
BLUE = '4'
OFF = '5'

BLUE_PRCNT = 1.0
RED_PRCNT = 0.8
GREEN_PRCNT = 1.2

colors = ["yellow", "green", "blue", "orange", "red", "pink"]
powerups_list = [[[10, 20], [30, 40]]]

# initialise IDs
calibrationID = "CAL"
camID = "CAM"



class Control:
    def __init__(self, cars):
        self.cars = cars.copy()
        self.dict_cars = {}
        for car in self.cars:         
            self.dict_cars[car.color] = car
        # initialise Grid
        self.grid = Grid()

    # Checks if a car is placed on a power up (when we are not using the information from the color sensor)
    def isOnPowerUp(self, car : Car):
        for pu in powerups_list:
            if pu[0][0] <= car.x <= pu[0][1] and pu[1][0] <= car.y <= pu[1][1]:
                return True
        return False

    # Figure out if a car has reached the finish line
    def isOnFinishLine(self, car : Car):
        if ((150 <= car.x <160) and (10 <= car.y < 40)) :
            return True
        return False

    # Checks if the car has collected all checkpoints in the circuit 
    # (it is not necessary to check the order because of the disposition of the circuit and the way we add a checkpoint)
    def hasAllCheckpoints(self, car : Car):
        if len(car.checkpoints) >= 6:
            return True
        return False
    
    def moveCar(self, car: Car):
        # save its previous coordinate (useful for updateCarMovement)
        car.old_x = car.x
        car.old_y = car.y
        
        # check if the car has finished a lap (without cheating)
        if self.isOnFinishLine(car) and self.hasAllCheckpoints(car):
            car.add_lap()
            print(f"NEW LAP for {car.id}")

        # check if a car has taken a powerup when we are not using the color sensors
        # if self.isOnPowerUp(car):
        #     if car.startTime == -1: # we only apply a powerup if we are not currently using one
        #         pu.powerUp(car, self.cars)

        # check if a car has finished using a powerup and reset its current acceleration
        if car.startTime != -1 and (datetime.datetime.now() - car.startTime).seconds >= POWERUP_TIME:
            car.startTime = -1
            car.acc = pu.NORMAL
            print(f"STOP POWERUP {car.id}")
        
        # if the car is AI driven, calculate the delta that needs to be sent
        if car.ai:
            self.find_info_flowmap(car)
            self.calculateDeltaCar(car)

        # get the acceleration that needs to be sent to the car when we are not using the color sensors
        # self.findCarAcc(car)

        return 

    # Get the car acceleration based on its zone in the circuit
    # Previously was also used to call updateCarMovement when we were simulating the algorithm in GUI
    # (calls are left in comments)
    def findCarAcc(self, car : Car):
        if car.x <= 60 and car.y <= 30:
            # list_occupation = updateMov.updateCarMovement(car, updateMov.BLUE_V)
            car.speed = "BLUE"
            if len(car.checkpoints) == 0 or car.checkpoints[-1] != BLUE:
                car.checkpoints.append(BLUE)
                print("New checkpoint")
                car.acc *= BLUE_PRCNT
        elif car.x <= 40 and car.y >= 130:
            # list_occupation = updateMov.updateCarMovement(car, updateMov.BLUE_V)
            car.speed = "BLUE"
            if len(car.checkpoints) == 0 or car.checkpoints[-1] != BLUE:
                car.checkpoints.append(BLUE)
                print("New checkpoint")
                car.acc *= BLUE_PRCNT
        elif car.x >= 120 and car.y >= 120:
            # list_occupation = updateMov.updateCarMovement(car, updateMov.RED_V)
            car.speed = "RED"
            if len(car.checkpoints) == 0 or car.checkpoints[-1] != RED:
                car.checkpoints.append(RED)
                print("New checkpoint")
                car.acc *= RED_PRCNT
        elif 40 <= car.x and car.x <= 90 and 40 <= car.y and car.y <= 150:
            # list_occupation = updateMov.updateCarMovement(car, updateMov.BLUE_V)
            car.speed = "BLUE"
            if len(car.checkpoints) == 0 or car.checkpoints[-1] != BLUE:
                car.checkpoints.append(BLUE)
                print("New checkpoint")
                car.acc *= BLUE_PRCNT
        elif car.x >= 160 and car.y <= 60:
            # list_occupation = updateMov.updateCarMovement(car, updateMov.RED_V)
            car.speed = "RED"
            if len(car.checkpoints) == 0 or car.checkpoints[-1] != RED:
                car.checkpoints.append(RED)
                print("New checkpoint")
                car.acc *= RED_PRCNT                      
        else:
            # list_occupation = updateMov.updateCarMovement(car, updateMov.GREEN_V)
            car.speed = "GREEN"
            if len(car.checkpoints) == 0 or car.checkpoints[-1] != GREEN:
                car.checkpoints.append(GREEN)
                print("New checkpoint")
                car.acc *= GREEN_PRCNT

    def updateCarMovement(self):
        threading.Timer(0.001, self.updateCarMovement).start()
        for rank in range(1, 4):
            for rank_2 in range(0, 3):
                if self.cars[rank_2].rank == rank:
                    car = self.cars[rank_2]
                    break
                
        for car in self.cars:
            self.moveCar(car)

    # Receives information from the connections and splits it by the newline characters
    # then parses the info and acts accordingly
    def recvInfo(self, info):
        # receiving coordinates from client 
        info = [inf for inf in info.split('\n') if inf != ""]
        return self.parseInfo(info)

    # Parse information received by the camera and arranges it in a dictionary of the form:
    # {'color1':[[x, y], ...], 'color1Angles':[[angle], ...], ...}
    def parseJson(self, recv_data):
        result = {}
        recv_data = recv_data.rstrip()
        data = json.loads(recv_data)
        point_regex = r"{(\d+), (\d+)}"
        
        for color in colors:
            points_str = data.get(color)
            if points_str:
                points = []
                for match in re.finditer(point_regex, points_str):
                    x, y = match.groups()
                    points.append([int(y), int(x)])
                result[color] = points
                angles_str = data[f"{color}Angles"]
                result[f"{color}Angles"] = [int(x) for x in ast.literal_eval(angles_str)]
        return result

    # Parses the information received by a connection and based on the id sent, reacts differently
    def parseInfo(self, info):
        id = info[0]
        if id == calibrationID: # enter calibration mode
            # all calibration points have the same color
            calibrationPoints = self.parseJson(info[1])[self.grid.calibrationColor]
            self.grid.setupGrid(calibrationPoints)
            return "CAL" # tell MainServerClass to acknowledge calibration

        elif id == camID: # saves the information sent by the camera for each car
            points = self.parseJson(info[1])
            for id, val in points.items():
                if self.grid.calibrated:
                    car = self.dict_cars.get(id)
                    if car:
                        if len(val) == 1: # we don't use the information when there are false positives
                            car.x, car.y = self.grid.getCircuitCoords(val[0][0], val[0][1])
                            car.orientation = points.get(f"{id}Angles")[0]
                            if car.started:
                                self.moveCar(car)
                        print(f"Coord: {car.x}, {car.y} {car.orientation}")
        else:
            for car in self.cars:
                # if the id corresponds to one of our cars we then reply with the information necessary to move the car
                if id == car.id: 
                    if not(car.ai) and info[1] == OFF: # stop the players cars when going off the map
                        print(f"{car.id} is out of the map")
                        return "200 0" # we stop the car
                    if info[1] == POWERUP:
                        if car.startTime == -1: # we only apply a powerup if we are not currently using one
                            pu.powerUp(car, self.cars)
                    if car.ai:
                        if car.started:
                            # apply overtake to slow down the car if it's too close to other cars
                            ovt.slowDown(car, self.cars) 
                            return f"{int(car.delta)} {int(car.acc)}"
                        else:
                            return "200 0" # we don't move the car if the game hasn't started
                    else:
                        if car.started and car.joystick_connected:
                            acc = 0
                            if car.controller.forward == 1:
                                acc = car.acc
                            elif car.controller.backward == 1:
                                acc = -car.acc

                            return f"{int(car.controller.horiz_move * 90 + 90)} {int(acc)}"
                        else:
                            return "200 0" # we don't move the car if the game hasn't started

    # Calculates the delta information that should be sent to the car 
    # and the desired orientation used by updateMovement
    def calculateDeltaCar(self, car: Car):
        right = car.orientation - car.fm_orientation
        right = right + 360 if right < 0 else right
        left = car.fm_orientation - car.orientation
        left = left + 360 if left < 0 else left
        if (left <= right):

            left = 90 if left > 90 else left
            car.desired_orientation = left
            car.delta = 90 + left
        else:
            right = 90 if right > 90 else right
            car.delta = 90 - right
            car.desired_orientation = -right

    # Looks for the orientation corresponding to the position of a given car in the flowmap
    def find_info_flowmap(self, car: Car):
        # if the car is out of bounds, we give it an orientation that will make it 
        # go back into the circuit 
        if car.x < 0:
            car.fm_orientation= 0
        elif car.x >= 200:
            car.fm_orientation = 180
        elif car.y < 0 :
            car.fm_orientation = 270
        elif car.y >= 200:
            car.y.fm_orientaion = 90
        else:
            car.fm_orientation = fmdir[int(car.x // 5)][int(car.y // 5)]


