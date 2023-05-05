import socket
from FlowMaps.circuit20x20 import directions as fmdir
from socketserver import ThreadingTCPServer,BaseRequestHandler
from Car import Car
import Overtake.overtake as ovt
import math

def parseCoordFromLine(coordinates):
    return [int(coord.rstrip()) for coord in coordinates.split(',')]

def sendCarInfo(car, toSend):
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
    id = info[0]
    # print(id)
    if id == camID:
        return "ACK"
        # for i in range(1, len(cars)+1):
        #     getCoordForCar(cars[i-1], info[i])
        #     ovt.calculateCircles(car[i])
        # for car in cars:
        #     ovt.overtake(car, cars)

    elif id == stopID:
        print(f"Stopped {cars[0].id}")
        return "-1"
    else:
        for car in cars:
            if id == car.id:
                for i in range(1, len(info)):
                    getCoordForCar(car, info[i])
                    if (not(car.x > 200 or car.y > 200) and not(car.x < 0 or car.y < 0)):
                        find_info_flowmap(car)
                        print(f"Received coords ({car.x}, {car.y}), cur dir: {car.orientation} and desired dir: {car.desired_orientation} for {car.id}")
                        moveCar(car)
                    return car.delta 

def getCoordForCar(car, coordinates):
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
    pass

def find_info_flowmap(car):
    # Assumes that coord x and y are between 0 and 200
    car.desired_orientation = fmdir[(car.x//10) - 1][(car.y//10) - 1]

if __name__ == "__main__":
    # read path from file and store information in a list of [x, y] values 
    filename = "Path/PathCoordsNoDupes.txt"
    path = []

    with open(filename, "r") as file:
        path = file.readlines()
        path = [parseCoordFromLine(line) for line in path]

    delta = 3 # hardcoded will need to be defined later on

    # initialise car objects
    # name = str(input("Car IP: "))
    car1 = Car("CAR1", ("172.20.10.9", 9999))
    cars = [car1]

    camID = "CAM"
    stopID = "STOP"
    # set up server
    bufferSize = 4096
    stop = False
    class handler(BaseRequestHandler):
        def handle(self):
            print(f'Connected: {self.client_address[0]}:{self.client_address[1]}')
            while True:
                msg = self.request.recv(bufferSize)
                if not msg:
                    print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                    break # exits handler, framework closes socket
                print(f'Received: {msg}')
                toSend = recvInfo(msg)
                if toSend:
                    self.request.send((str(toSend) + "\n").encode())
                    print(f"Sent {toSend}")

                
    server = ThreadingTCPServer(('',8998), handler)
    server.serve_forever()
    if stop:
        server.shutdown()

