import random
import socket
import threading
import json
import re
import copy
import ast

from Algo.Car import Car
from Algo.Car import RED_C, BLUE_C, GREEN_C, BRUN_C, VIOLET_C, ROSE_C
from Algo.FlowMaps.circuit20x20 import directions as fmdir
import Algo.Overtake.overtake as ovt
import Algo.FlowMaps.powerups as pu
from Algo.Grid import Grid
import Algo.UpdateMovements as updateMov
from Algo.Orientation import calcOrientation
from GUI import GUI

# constant definitions
POWERUP = 1

# initialise IDs
calibrationID = "CAL"
camID = "CAM"
stopID = "STOP"
startID = "START"
calibrationColor = "yellow"
guiID = "GUI"
calDeltaID = "CALDELTA"
calDeltaLeftID = "CALDELTALeft"
calDeltaRightID = "CALDELTARight"


# initialise car objects
car1 = Car("CAR_ID_TEST", "Test", "Test", ("172.20.10.6", 9999), GREEN_C, color="green", x=160, y=20, orientation=180, ai=False)
car1.rank = 3
# car2 = Car("CAR2", "Test", "Test", ("172.20.10.8", 9999), RED_C, x=140, y=20, orientation=180)
# car2.rank = 2
# car3 = Car("CAR3", "Test", "Test", ("172.20.10.8", 9999), GREEN_C, x=120, y=20, orientation=180)
# car3.rank = 1
#car4 = Car("CAR4", "Test", "Test", ("172.20.10.6", 9999), VIOLET_C, x=180, y=20, orientation=180)
#car4.rank = 4
#car5 = Car("CAR5", "Test", "Test", ("172.20.10.8", 9999), ROSE_C, x=100, y=20, orientation=180)
#car5.rank = 6
#car6 = Car("CAR6", "Test", "Test", ("172.20.10.8", 9999), BRUN_C, x=110, y=20, orientation=180)
#car6.rank = 5


dict_cars = {}
cars = [car1]
for car in cars:         
    dict_cars[car.color] = car

grid = Grid()
launched = False


def moveCar(car: Car):
    car.old_x = car.x
    car.old_y = car.y
    # car.x = car.predicted_x  # todo prevent errors because of threads
    # car.y = car.predicted_y  # todo prevent errors because of threads
    find_info_flowmap(car)
    # if (car.started):
    #     return car.delta

    # if not(car.cam):
        # car.x = car.predicted_x  # todo prevent errors because of threads
        # car.y = car.predicted_y  # todo prevent errors because of threads

    coeff = 1.0

    if car.id == cars[0].id:
        coeff = 0.9

    if car.x <= 60 and car.y <= 30:
        list_occupation = updateMov.updateCarMovement(car, updateMov.BLUE_V, gui)
        car.speed = "BLUE"
        # print("Zone 1")
    elif car.x <= 40 and car.y >= 130:
        list_occupation = updateMov.updateCarMovement(car, updateMov.BLUE_V, gui)
        car.speed = "BLUE"
        # print("Zone 2")
    elif car.x >= 120 and car.y >= 120:
        list_occupation = updateMov.updateCarMovement(car, updateMov.RED_V, gui)
        # print("Zone 3")
    elif 40 <= car.x and car.x <= 90 and 40 <= car.y and car.y <= 150:
        list_occupation = updateMov.updateCarMovement(car, updateMov.BLUE_V, gui)
        car.speed = "BLUE"
        # print("Zone 4")
    elif car.x >= 160 and car.y <= 60:
        list_occupation = updateMov.updateCarMovement(car, updateMov.RED_V, gui)
        car.speed = "RED"
        # print("Zone 5")
    else:
        list_occupation = updateMov.updateCarMovement(car, updateMov.GREEN_V, gui)
        car.speed = "GREEN"
        # print("Zone 6")

    calculateDeltaCar(car)
    print(f"Coord: {car.x}, {car.y} {car.orientation} {car.fm_orientation}")


    return list_occupation
    # updateMov.updateCarMovement(car, updateMov.GREEN_V)

    # print(f"Updated prediction coords ({car.predicted_x}, {car.predicted_y}), cur dir: {car.orientation}  velocity: {car.velocity} flowmap orientation: {car.fm_orientation} delta: {car.delta}and desired_orientation: {car.desired_orientation} for {car.id}")


def updateCarMovement():
    threading.Timer(0.05, updateCarMovement).start()
    # for rank in range(1,4):

    #     for rank_2 in range(0,3):
    #         if cars[rank_2].rank ==  rank:
    #             car = cars[rank_2]
    #             break

    moveCar(car)

    # car.left_circle, car.right_circle = ovt.calculateCircles(car)




def parseCoordFromLine(coordinates):
    res = []
    for coord in coordinates.split(','):
        try:
            res.append(int(coord.rstrip()))
        except:
            continue
    return res


def getPowerUp(pow):
    return int(pow.rstrip())


def updatePowerUp(car: Car, pow):
    car.powerup = getPowerUp(pow)


def sendCarInfo(car: Car, toSend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # s.bind(('172.20.10.2', 7777))
        s.connect(car.server)
        print(f"Sent to {car.id}: {str(toSend)}")
        s.sendall(str(toSend).encode())
        s.close()


def recvInfo(info, needToBeDecoded=True):
    # print(info)
    # receiving coordinates from client
    if (needToBeDecoded):
        info = info.decode()

    info = [inf for inf in info.split('\n') if inf != ""]
    return parseInfo(info)


def parseJson(recv_data):
    # print("received")
    # print(recv_data)
    recv_data = recv_data.rstrip()
    data = json.loads(recv_data)
    point_regex = r"{(\d+), (\d+)}"

    yellow_points_str = data["yellow"]
    points = []
    for match in re.finditer(point_regex, yellow_points_str):
        x, y = match.groups()
        points.append([int(y), int(x)])
    yellow_points_list = points

    green_points_str = data["green"]
    points = []
    for match in re.finditer(point_regex, green_points_str):
        x, y = match.groups()
        points.append([int(y), int(x)])
    green_points_list = points

    blue_points_str = data["blue"]
    points = []
    for match in re.finditer(point_regex, blue_points_str):
        x, y = match.groups()
        points.append([int(y), int(x)])
    blue_points_list = points

    yellow_angles_str = data["yellowAngles"]
    yellow_angles_list = [int(x) for x in ast.literal_eval(yellow_angles_str)]

    green_angles_str = data["greenAngles"]
    green_angles_list = [int(x) for x in ast.literal_eval(green_angles_str)]

    blue_angles_str = data["blueAngles"]
    blue_angles_list = [int(x) for x in ast.literal_eval(blue_angles_str)]

    return {"yellow": yellow_points_list, "green": green_points_list, "blue": blue_points_list, "yellowAngles": yellow_angles_list, "greenAngles": green_angles_list, "blueAngles": blue_angles_list}


def parseInfo(info):
    id = info[0]
    if id == calibrationID:
        # all calibration points have the same color
        calibrationPoints = parseJson(info[1])["yellow"]
        calibrationPoints.sort(key=lambda p: (p[1], p[0]))  # order them along the y axis

        # # if we implement the color system
        # calibrationPoints = parseJson(info[1])
        # top_left = calibrationPoints[grid.top_left_color][0]
        # top_right = calibrationPoints[grid.top_right_color][0]
        # bot_left = calibrationPoints[grid.bot_left_color][0]
        # bot_right = calibrationPoints[grid.bot_right_color][0]

        grid.setupGrid(calibrationPoints)
        
        return "CAL"

    elif id == camID:
        # print(info)
        points = parseJson(info[1])
        for id, val in points.items():
            # id will be the color of the car (green or blue for now)
            # value will be an array of array
            # [[687, 1248], [845, 639]]
            if grid.calibrated:
                car = dict_cars.get(id)
                if car:
                    car.old_x = car.x
                    car.old_y = car.y
                    # if len(val) > 1:
                    #     car.x = car.predicted_x # todo prevent errors because of threads
                    #     car.y = car.predicted_y # todo prevent errors because of threads
                    # else:

                    if len(val) == 1:
                        # print(f"COORDS {val[0]}")
                        car.x, car.y = grid.getCircuitCoords(val[0][0], val[0][1])
                        # find_velocity_and_orientation(car)
                        # print(f"{id}Angles")
                        car.orientation = points.get(f"{id}Angles")[0]
                        if car.started:
                            moveCar(car)
                        car.cam = True
                    else:
                        car.cam = False
            # else:
                # if grid.detect_point:
                #     if id == calibrationColor:
                #         if len(val) == 1:
                #             x, y = grid.getCircuitCoords(val[0][0], val[0][1])
                #             grid.diff_x = x - grid.point[0] 
                #             grid.diff_y = y - grid.point[1]
                #             grid.calibrated = True
                # elif grid.calibratedLeft:
                #     if id == calibrationColor:
                #         if len(val) == 1:
                #             grid.real_left = val[0]
                #             print(grid.real_left)
                #             grid.calibratedLeft = False
                # elif grid.calibratedRight:
                #     if id == calibrationColor:
                #         if len(val) == 1:
                #             grid.real_top = val[0]
                #             print(grid.real_top)
                #             grid.calibratedRight = False
                #             grid.calibrated = True   
                        # print(f"{id}Angles")
                        # car.orientation = points.get(f"{id}Angles")[0]
                    print(f"Coord: {car.x}, {car.y} {car.orientation}")
            else:
                if grid.detect_point:
                    if id == calibrationColor:
                        if len(val) == 1:
                            x, y = grid.getCircuitCoords(val[0][0], val[0][1])
                            grid.diff_x = x - grid.point[0] + 10
                            grid.diff_y = y - grid.point[1]
                            grid.calibrated = True
                # ovt.calculateCircles(car)
        # for car in cars:
        # ovt.overtake(car, cars)
        # for car in cars:
        # moveCar(car)
        # pass

    elif id == calDeltaID:
        grid.detect_point = True
    elif id == calDeltaLeftID:
        grid.calibratedLeft = True
    elif id == calDeltaRightID:
        grid.calibratedRight = True
    elif id == stopID:
        print(f"Stopped {cars[0].id}")
        return "200"
    elif id == startID:
        updateCarMovement()
        print(f"Start moving cars")
        for car in cars:
            car.started = True
        # updateCarMovement()
    elif id == guiID:
        gui.launchGUI(cars)
    else:
        for car in cars:
            if id == car.id:
                if car.ai:
                    if car.started:
                        return f"{int(car.delta)}"
                    else:
                        return "200"
                else:
                    if car.joystick_connected:
                        toSend = 1
                        if car.manette.forward == 1:
                            toSend = 2
                        elif car.manette.backward == 1:
                            toSend = 0
                        
                        return f"{int(car.manette.horiz_move * 90 + 90)} {toSend}"
        # else:
        #     print(f"ERROR: Connection to server without or with incorrect ID, received: {id}")


def getCoordForCar(car: Car, coordinates):
    car.old_x = car.x
    car.old_y = car.y
    car.x, car.y, car.orientation = parseCoordFromLine(coordinates)


def calculateDeltaCar(car : Car):
    right = car.orientation - car.fm_orientation
    right = right + 360 if right < 0 else right
    left = car.fm_orientation - car.orientation
    left = left + 360 if left < 0 else left

    
    

    # old_delta = car.delta 
    # tmp_delta = car.delta
    if (left <= right):
        
        left = 90 if left > 90 else left
        car.desired_orientation = left
        car.delta = 90 + left

    #     if (left <= 5):
    #         car.delta = 90
    #     elif (5 < left <= 40):
    #         car.delta = 135
    #     elif (left > 40):
    #         car.delta = 180
    #     print(f"LEFT {left}")
        # car.delta = 180 if left <10 else 90
    else:
        
        right = 90 if right > 90 else right
        car.delta = 90 - right
        # car.delta = 0 if right < 10 else 90
        # if (right <= 5):
        #     car.delta = 90
        # elif (5 < right <= 40):
        #     car.delta = 45
        # elif (right > 40):
        #     car.delta = 0

        # if right == 0:
        #     right = 0.1
        car.desired_orientation = -right
        # print(f"RIGHT {right}")
    
        # car.delta = 90 - (right / 180) * 90

    # if abs(car.delta - car.old_delta) < 10:
    #     car.delta = car.old_delta
    # sendCarInfo(car, car.delta)

def find_velocity_and_orientation(car):
    if car.moving:
        if car.count == 100:
            car.orientation = calcOrientation([[car.old_x, car.old_y], [car.x, car.y]])
            car.count = 0
        else:
            car.count += 1


def find_info_flowmap(car: Car):
    # Assumes that coord x and y are between 0 and 199
    # car.started = False
    # car.delta = 200
    if car.x < 0:
        car.fm_orientation= 0
    elif car.x >= 200:
        car.fm_orientation = 180
    elif car.y < 0 :
        car.fm_orientation = 270
    elif car.y >= 200:
        car.y.fm_orientaion = 90
    else:
        car.x = 190 if car.x >= 200 else car.x
        car.x = 0 if car.x < 0 else car.x
        car.y = 190 if car.y >= 200 else car.y
        car.y = 0 if car.y < 0 else car.y
        car.fm_orientation = fmdir[int(car.x // 10)][int(car.y // 10)]


