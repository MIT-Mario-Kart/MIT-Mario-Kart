import socket
import requests

class Car:
  def __init__(self, name, server, x=0, y=0, interaction_index=0, index=0, move=False):
    self.name = name
    self.server = server
    self.x = x
    self.y = y
    self.interaction_index = interaction_index
    self.index = index # to be incremented every time we reach a given checkpoint
    self.move = move

def parseCoordFromLine(coordinates):
    return [int(coord.strip()) for coord in coordinates.split(',')]

def getCoordForCar(car):
    # receiving coordinates from client
    coordinates, addr = UDPServerSocket.recvfrom(bufferSize)
    coordinates = coordinates.decode()
    line = parseCoordFromLine(coordinates)
    if (line[0] == car.interaction_index):
        car.x, car.y = line[1:]
        car.interaction_index += 1
        car.move = True

def moveToCoordinate(car, target, delta):
    distX = target[0] - car.x
    distY = target[1] - car.y
    if abs(distX) < delta and abs(distY) < delta:
        car.index += 1 # if we are within a certain radius of our checkpoint, we move on to the next
        return
    # TODO this is where the car model will need to be taken into account bc the cars move while doing the calculations

    server_path = ""
    if distY > 0:
        server_path += "F"
    elif distY < 0:
        server_path += "B"

    if distX > 0:
        server_path += "R"
    elif distX < 0:
        server_path += "L" 
    print(server_path)
    if server_path == "" or server_path[0] not in  ["F", "B"]:
        server_path = "S"

    requests.get(url=car.server+server_path)
    car.move = False

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
    car_IP = "172.20.10.4"
    car1 = Car("Car1", f"http://{car_IP}:80/")

    # set up server
    bufferSize = 4096
    cam_addr = '00:00:00:00:00:00'#your address here
    BServerSocket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    port = 1
    print("Bluetooth server up and listening")

    UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    print("UDP server up and listening")
    CarAddrPort = (car_IP, 8888)
    bytesToSend1 = "BEGIN CONNECTION".encode()
    UDPServerSocket.sendto(bytesToSend1, CarAddrPort)
    while(True):
        print(BServerSocket.recvfrom(bufferSize))

        # TODO maybe add a way to check that all the values are valid without crashing the program
        # getCoordForCar(car1)
        # if(car1.move):
        #     # print(f"Received coords ({car1.x}, {car1.y}) for {car1.name}")
            # moveToCoordinate(car1, path[car1.index], delta)
            # if car1.index == len(path):
            #     print("Reached destination")
            #     exit()

        