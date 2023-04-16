import socket
import requests

class Car:
  def __init__(self, name, server, x=0, y=0, index=0):
    self.name = name
    self.server = server
    self.x = x
    self.y = y
    self.index = index # to be incremented every time we reach a given checkpoint

def parseCoordFromLine(coordinates):
    return [int(coord.strip()) for coord in coordinates.split(',')]

def getCoordForCar(car):
    # receiving coordinates from client
    coordinates, addr = UDPServerSocket.recvfrom(bufferSize)
    coordinates = coordinates.decode()
    car.x, car.y = parseCoordFromLine(coordinates)

def moveToCoordinate(car, target, delta):
    distX = target[0] - car.x
    distY = target[1] - car.y
    if abs(distX) < delta and abs(distY) < delta:
        car.index += 1 # if we are within a certain radius of our checkpoint, we move on to the next
        return
    # TODO this is where the car model will need to be taken into account bc the cars move while doing the calculations

    server_path = ""
    if distY > 0:
        server_path += "f"
    elif distY < 0:
        server_path += "b"

    if distX > 0:
        server_path += "r"
    elif distX < 0:
        server_path += "l" 

    if server_path == "":
        server_path = "s"

    r = requests.get(url=car.server+server_path)
    print(r.json())

if __name__ == "__main__":
    # read path from file and store information in a list of [x, y] values 
    filename = "PathCoordsNoDupes.txt"
    path = []

    with open(filename, "r") as file:
        path = file.readlines()
        path = [parseCoordFromLine(line) for line in path]

    # initialise car objects
    car1 = Car("Car1", "10.172.10.3:80/")
    car2 = Car("Car1", "10.172.10.4:80/")

    # set up server
    localIP = "127.0.0.1"
    localPort = 8888
    bufferSize = 1024
    
    UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    
    while(True):
        getCoordForCar(car1)
        getCoordForCar(car2)
        print(f"Received coords ({car1.x}, {car1.y}) for {car1.name} and ({car2.x}, {car2.y}) for {car2.name}")
        moveToCoordinate(car1, path[car1.index])
        moveToCoordinate(car2, path[car2.index])


        