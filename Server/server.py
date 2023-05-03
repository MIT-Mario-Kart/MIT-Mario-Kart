import socket
from FlowMaps.circuit20x20 import directions as fmdir
from socketserver import ThreadingTCPServer,BaseRequestHandler
from Car import Car
import Overtake.overtake as ovt

def parseCoordFromLine(coordinates):
    return [int(coord.strip()) for coord in coordinates.split(',')]

def recvInfo(info):
    # receiving coordinates from client
    info = info.decode()
    info = info.split('\n')
    id = info[0]
    if id == camID:
        print("HI")
        # for i in range(1, len(cars)+1):
        #     getCoordForCar(cars[i-1], info[i])
        #     ovt.calculateCircles(car[i])
        # for car in cars:
        #     ovt.overtake(car, cars)

    elif id == stopID:
        for car in cars:
            server.sendto(b"-1", car.server)
            print(f"Stopped {car.id}")
        server.shutdown()
    else:
        for car in cars:
            if id == car.id:
                # print(info)
                getCoordForCar(car, info[1])
                if (not(car.x > 200 or car.y > 200)):
                    find_info_flowmap(car)
                    return moveCar(car)

def getCoordForCar(car, coordinates):
    car.x, car.y, car.orientation = parseCoordFromLine(coordinates)
    print(f"Received coords ({car.x}, {car.y}) and direction {car.orientation} for {car.id}")
    
def moveCar(car):
    car.delta = car.desired_orientation - car.orientation
    
    if (180 <= car.delta <= 270):
        car.delta = 180
    elif (270 <= car.delta <= 360):
        car.delta = 0
    else:
        car.delta += 90
    return car.delta

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
                    self.request.send(toSend.encode())
    server = ThreadingTCPServer(('',8888), handler)
    server.serve_forever()
    
