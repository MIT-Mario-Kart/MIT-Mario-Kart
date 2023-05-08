import socket
import threading
import  json

from Algo.Car import Car
from Algo.FlowMaps.circuit20x20 import directions as fmdir
import Algo.Overtake.overtake as ovt
from Algo.Grid import Grid
from Algo.UpdateMovements import updateMovement
from Algo.Orientation import calcOrientation
# constant definitions

# initialise IDs
calibrationID = "CAL"
camID = "CAM"
stopID = "STOP"
calibrationColor = "yellow"

# initialise car objects
car1 = Car("CAR1", ("172.20.10.9", 9999))
dict_cars = {}
cars = [car1] 
for car in cars:
    dict_cars[car.id] = car

grid = Grid()

def updateAICarMovements():
    threading.Timer(0.25, updateAICarMovements).start()
    updateMovement(cars)

def parseCoordFromLine(coordinates):
    return [int(coord.rstrip()) for coord in coordinates.split(',')]

def sendCarInfo(car: Car, toSend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # s.bind(('172.20.10.2', 7777))
        s.connect(car.server)   
        print(f"Sent to {car.id}: {str(toSend)}")
        s.sendall(str(toSend).encode())
        s.close()

def recvInfo(info):
    print(info)
    # receiving coordinates from client
    info = info.decode()
    info = [inf for inf in info.split('\n') if inf != ""]
    parseInfo(info)

def parseJson(recv_data):
    recv_data = recv_data
    parsed_json_data = json.loads(recv_data)
    result = {}
    point_str = "NSPoint("
    for id, val in parsed_json_data.items():
        points = []
        while point_str in val:
            start = val.index(point_str)
            end = val.index(")", start, len(val))
            x,y = parseCoordFromLine(val[start+len(point_str):end])
            points.append([x, y])
            val = val[end+1:]
        result[id] = points
    print(result)
    return result

def parseInfo(info):
    id = info[0]
    if id == calibrationID:
        # all calibration points have the same color
        calibrationPoints = parseJson(info[1])[calibrationColor]
        calibrationPoints.sort(key= lambda p:(p[1], p[0])) # order them along the y axis
        top_left, top_right, bot_left, bot_right = calibrationPoints

        # # if we implement the color system
        # calibrationPoints = parseJson(info[1])
        # top_left = calibrationPoints[grid.top_left_color][0]
        # top_right = calibrationPoints[grid.top_right_color][0]
        # bot_left = calibrationPoints[grid.bot_left_color][0]
        # bot_right = calibrationPoints[grid.bot_right_color][0]

        grid.setupGrid(top_left, top_right, bot_left, bot_right)
        updateAICarMovements()
        return "CAL"
    
    elif id == camID:
        points = parseJson(info[1])
        for id, val in points.items():
            car = dict_cars.get(id)
            if car:
                car.old_x = car.x
                car.old_y = car.y
                if len(val) > 1:
                    car.x = car.predicted_x # todo prevent errors because of threads
                    car.y = car.predicted_y # todo prevent errors because of threads
                else:
                    car.x, car.y = grid.getCircuitCoords(val)
                find_velocity_and_orientation(car)
                ovt.calculateCircles(car)
        for car in cars:
            ovt.overtake(car, cars)
        for car in cars:
            moveCar(car)

    elif id == stopID:
        print(f"Stopped {cars[0].id}")
        return "-1"
    else:
        car = dict_cars.get(id)
        if car:
            for i in range(1, len(info)):
                getCoordForCar(car, info[i])
                if (not(car.x > 200 or car.y > 200) and not(car.x < 0 or car.y < 0)):
                    find_info_flowmap(car)
                    print(f"Received coords ({car.x}, {car.y}), cur dir: {car.orientation} and desired dir: {car.desired_orientation} for {car.id}")
                    moveCar(car)
                return car.delta
        else:
            print(f"ERROR: Connection to server without or with incorrect ID, received: {id}")

def getCoordForCar(car: Car, coordinates):
    car.old_x = car.x
    car.old_y = car.y
    car.x, car.y, car.orientation = parseCoordFromLine(coordinates)     

def moveCar(car):
    right = car.orientation - car.desired_orientation
    right = right +360 if right < 0  else right
    left = car.desired_orientation - car.orientation
    left = left +360 if left < 0  else left

    if (left <= right):
        car.delta = left
        # car.delta = 90 + (left/180) * 90
    else:
        # car.delta = 90 - (right/180)*90
        car.delta = -right

    # sendCarInfo(car, car.delta)

def find_velocity_and_orientation():
    car.orientation, car.velocity = calcOrientation([[car.old_x, car.old_y], [car.x, car.y]])

def find_info_flowmap(car: Car):
    # Assumes that coord x and y are between 0 and 200
    car.desired_orientation = fmdir[(car.x//10) - 1][(car.y//10) - 1]
