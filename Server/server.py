import socket
import requests
from FlowMaps.circuit20x20 import directions as fmdir

class Car:
  def __init__(self, name, server, x=0, y=0, interaction_index=0, index=0, move=False):
    self.name = name
    self.server = server
    self.x = x
    self.y = y
    self.interaction_index = interaction_index
    self.index = index # to be incremented every time we reach a given checkpoint
    self.move = move
    self.velocity = 0
    self.orientation = 0
    self.desired_orientation = 0
    self.delta = 0 # steering angle
    self.a = 0 # acceleration

def parseCoordFromLine(coordinates):
    return [int(coord.strip()) for coord in coordinates.split(',')]

def getCoordForCar(car):
    # receiving coordinates from client
    coordinates, addr = TCPServerSocket.recvfrom(bufferSize)
    # print(coordinates)
    if coordinates == b"1":
        bytesToSend1 = b"-1"
        TCPServerSocket.sendto(bytesToSend1, CarAddrPort)
        exit()
        
    coordinates = coordinates.decode()
    line = parseCoordFromLine(coordinates)
    print(line)
    # if (line[0] == car.interaction_index):
    car.x, car.y, car.orientation = line[1:]
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

def moveCar(car):
    car.delta = car.desired_orientation - car.orientation
    
    if (180 <= car.delta <= 270):
        car.delta = 180
    elif (270 <= car.delta <= 360):
        car.delta = 0
    else:
        car.delta += 90
    car.move = False
    return str(car1.delta).encode()

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
    car_IP = "172.20.10.3"
    car1 = Car("Car1", f"http://{car_IP}:80/")

    # set up server
    bufferSize = 4096
    
    
    # This is the alternative code for TCP instead of UDP
    # My proposal is that we use one TCP socket for everything.
    
    
    # HOST = "172.20.10.4"  # addr to bind to (generally server's computer local IP addr)
    # PORT = 65432   # port to listen on (non-privileged ports are > 1023)
    
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    #     s.bind((HOST, PORT))
    #     s.listen()
    #     conn, addr = s.accept()
    #     with conn:
    #         print(f"Connected by {addr}")
    #         while True:
    #             data = conn.recv(bufferSize)
    #             print("received")
    #             print(data)
    
    UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    print("UDP server up and listening")
    CarAddrPort = (car_IP, 8888)
    bytesToSend1 = "BEGIN CONNECTION".encode()
    ClientAddrPort = ("127.0.0.1", 9999)
    TCPServerSocket.sendto(bytesToSend1, ClientAddrPort)
    # packet_recv = ""
    # while (packet_recv != ""):
        
    while(True):
        TCPServerSocket.sendto(bytesToSend1, CarAddrPort)
        if (car1.interaction_index == 0):
            bytesToSend1 = "BEGIN CONNECTION".encode()
        # print(BServerSocket.recvfrom(bufferSize))
        # print(TCPServerSocket.recvfrom(bufferSize))
        # TODO maybe add a way to check that all the values are valid without crashing the program
        getCoordForCar(car1)
        # if(car1.move):
        print(f"Received coords ({car1.x}, {car1.y}) for {car1.name}")
        if (not(car1.x > 200 or car1.y > 200)):
            find_info_flowmap(car1)
            bytesToSend1 = moveCar(car1)
            if car1.index == len(path):
                print("Reached destination")
                exit()