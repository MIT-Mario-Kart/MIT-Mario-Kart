import socket
import threading
import  json
import re

from Algo.Car import Car
from Algo.FlowMaps.circuit20x20 import directions as fmdir
import Algo.Overtake.overtake as ovt
import Algo.FlowMaps.powerups as pu
from Algo.Grid import Grid
import Algo.UpdateMovements as updateMov
from Algo.Orientation import calcOrientation
# constant definitions

# initialise IDs
calibrationID = "CAL"
camID = "CAM"
stopID = "STOP"
calibrationColor = "yellow"

# initialise car objects
#car1 = Car("CAR1", ("172.20.10.6", 9999), x=160, y=20, orientation=180)
car1 = Car("CAR1", ("192.168.199.228", 9999), x=160, y=20, orientation=180)
# car2 = Car("CAR2", ("172.20.10.8", 9999), x=160, y=20, orientation=270)
dict_cars = {}
cars = [car1] 
for car in cars:
    dict_cars[car.id] = car

grid = Grid()
launched = False

def moveCar(car: Car):
    car.old_x = car.x
    car.old_y = car.y
    car.x = car.predicted_x # todo prevent errors because of threads
    car.y = car.predicted_y # todo prevent errors because of threads
    find_info_flowmap(car)
    calculateDeltaCar(car)

    if car.x <= 60 and car.y <= 30:
        updateMov.updateCarMovement(car, updateMov.BLUE_V)
        car.speed = "BLUE"
        # print("Zone 1")
    elif car.x <= 40 and car.y >= 130:
        updateMov.updateCarMovement(car, updateMov.BLUE_V)
        car.speed = "BLUE"
        # print("Zone 2")
    elif car.x >= 150 and car.y >= 120:
        updateMov.updateCarMovement(car, updateMov.RED_V)
        car.speed = "RED"
        # print("Zone 3")
    elif 40 <= car.x and car.x <= 90 and 40 <= car.y and car.y <= 150:
        updateMov.updateCarMovement(car, updateMov.BLUE_V)
        car.speed = "BLUE"
        # print("Zone 4")
    elif car.x >= 160 and car.y <= 60:
        updateMov.updateCarMovement(car, updateMov.RED_V) 
        car.speed = "RED"
        # print("Zone 5")
    else:
        updateMov.updateCarMovement(car, updateMov.GREEN_V)
        car.speed = "GREEN"
        # print("Zone 6")


    # updateMov.updateCarMovement(car, updateMov.GREEN_V)

    print(f"Updated prediction coords ({car.predicted_x}, {car.predicted_y}), cur dir: {car.orientation}  velocity: {car.velocity} flowmap orientation: {car.fm_orientation} delta: {car.delta}and desired_orientation: {car.desired_orientation} for {car.id}")

def updateCarMovement():
    threading.Timer(0.25, updateCarMovement).start()
    for car in cars:
        moveCar(car)


# updateAICarMovements()

def parseCoordFromLine(coordinates):
    return [int(coord.rstrip()) for coord in coordinates.split(',')]

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

def recvInfo(info):
    # print(info)
    # receiving coordinates from client
    info = info.decode()
    info = [inf for inf in info.split('\n') if inf != ""]
    return parseInfo(info)

def parseJson(recv_data):
    print("received")
    print(recv_data)
    recv_data = recv_data.rstrip("CAL")
    data = json.loads(recv_data)
    point_regex = r"{(\d+), (\d+)}"
    
    yellow_points_str = data["yellow"]
    points = []
    for match in re.finditer(point_regex, yellow_points_str):
        x, y = match.groups()
        points.append([int(x), int(y)])
    yellow_points_list = points
    
    green_points_str = data["green"]
    points = []
    for match in re.finditer(point_regex, green_points_str):
        x, y = match.groups()
        points.append([int(x), int(y)])
    green_points_list = points
    
    blue_points_str = data["blue"]
    points = []
    for match in re.finditer(point_regex, blue_points_str):
        x, y = match.groups()
        points.append([int(x), int(y)])
    blue_points_list = points

    return {"yellow": yellow_points_list, "green": green_points_list,  "blue": blue_points_list}

def parseInfo(info):
    id = info[0]
    if id == calibrationID:
        # all calibration points have the same color
        calibrationPoints = parseJson(info[1])["yellow"]
        calibrationPoints.sort(key= lambda p:(p[1], p[0])) # order them along the y axis
        top_left, top_right, bot_left, bot_right = calibrationPoints
        

        # # if we implement the color system
        # calibrationPoints = parseJson(info[1])
        # top_left = calibrationPoints[grid.top_left_color][0]
        # top_right = calibrationPoints[grid.top_right_color][0]
        # bot_left = calibrationPoints[grid.bot_left_color][0]
        # bot_right = calibrationPoints[grid.bot_right_color][0]

        grid.setupGrid(top_left, top_right, bot_left, bot_right)
        updateCarMovement()
        
        return "CAL"
    
    elif id == camID:
        points = parseJson(info[1])
        for id, val in points.items():
            # id will be the color of the car (green or blue for now)
            # value will be an array of array
            # [[687, 1248], [845, 639]]
            car = dict_cars.get(id)
            if car:
                car.old_x = car.x
                car.old_y = car.y
                if len(val) > 1:
                    car.x = car.predicted_x # todo prevent errors because of threads
                    car.y = car.predicted_y # todo prevent errors because of threads
                else:
                    car.x, car.y = grid.getCircuitCoords(val)
                # find_velocity_and_orientation(car)
                ovt.calculateCircles(car)

        for car in cars:
            if (car.powerup == 1):
                pu.powerUp(car, cars)

            ovt.overtake(car, cars)

        
        for car in cars:
            # moveCar(car)
            pass

    elif id == stopID:
        print(f"Stopped {cars[0].id}")
        return "-1"
    elif id == "CAR_ID_TEST":
        for car in cars:
            # car.old_x = car.x
            # car.old_y = car.y
            # car.x = car.predicted_x # todo prevent errors because of threads
            # car.y = car.predicted_y # todo prevent errors because of threads
            # min(int(car.delta) +5, 180)
            # max(int(car.delta) - 20, 0)
            return min(int(car.delta) +5, 180)
    else:
        car = dict_cars.get(id)
        if car:
            updatePowerUp(car, info[1])
            sendCarInfo(car, f"{car.delta}, {car.a}")
        else:
            print(f"ERROR: Connection to server without or with incorrect ID, received: {id}")

def getCoordForCar(car: Car, coordinates):
    car.old_x = car.x
    car.old_y = car.y
    car.x, car.y, car.orientation = parseCoordFromLine(coordinates)     

def calculateDeltaCar(car):
    right = car.orientation - car.fm_orientation
    right = right + 360 if right < 0  else right
    left = car.fm_orientation - car.orientation
    left = left + 360 if left < 0  else left

    car.old_delta = car.delta
    if (left <= right):
        car.desired_orientation = left
        car.delta = 90 + (left/180) * 90
        # car.delta = 180 if left <10 else 90
    else:
        # car.delta = 0 if right < 10 else 90
        if right == 0:
            right = 0.1
        car.desired_orientation = -right
        car.delta = 90 - (right/180)*90

    if abs(car.delta - car.old_delta) < 10:
        car.delta = car.old_delta

    # sendCarInfo(car, car.delta)

# def find_velocity_and_orientation():
#     car.orientation, car.velocity = calcOrientation([[car.old_x, car.old_y], [car.x, car.y]])

def find_info_flowmap(car: Car):
    # Assumes that coord x and y are between 0 and 199
    car.x = 190 if car.x >= 200 else car.x
    car.x = 0 if car.x < 0 else car.x
    car.y = 190 if car.y >= 200 else car.y
    car.y = 0 if car.y < 0 else car.y
    car.fm_orientation = fmdir[int(car.x//10)][int(car.y//10)]
