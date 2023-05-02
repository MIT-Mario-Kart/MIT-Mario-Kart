import socket
from FlowMaps.circuit20x20 import directions as fmdir

class Car:
  def __init__(self, id, server, x=0, y=0, index=0):
    self.id = id
    self.server = server
    self.x = x
    self.y = y
    self.index = index # to be incremented every time we reach a given checkpoint
    self.velocity = 0
    self.orientation = 0
    self.desired_orientation = 0
    self.delta = 0 # steering angle
    self.a = 0 # acceleration

def parseCoordFromLine(coordinates):
    return [int(coord.strip()) for coord in coordinates.split(',')]

def recvInfo(camID, stopID, cars):
    c, addr = TCPServerSocket.accept()
    # receiving coordinates from client
    info, addr = TCPServerSocket.recvfrom(bufferSize)
    info = info.decode()
    print(info, addr)
    info = [line.split(',') for line in info.split('\n')]
    id = info[0][0]
    if id == camID:
        for i in range(1, len(cars) + 1):
            getCoordForCar(cars, info[i])
    elif id == stopID:
        for car in cars:
            TCPServerSocket.sendto(b"-1", car.server)
            print(f"Stopped {car.id}")
        # exit()
    elif id == car1.id:
        getCoordForCar(car1, info[1])

def getCoordForCar(car, coordinates):
    coordinates = coordinates.decode()
    line = parseCoordFromLine(coordinates)
    print(line)
    car.x, car.y, car.orientation = line[1:]
    print(f"Received coords ({car.x}, {car.y}) for {car.id}")
    if (not(car.x > 200 or car.y > 200)):
        find_info_flowmap(car)
        moveCar(car)

def moveCar(car):
    car.delta = car.desired_orientation - car.orientation
    
    if (180 <= car.delta <= 270):
        car.delta = 180
    elif (270 <= car.delta <= 360):
        car.delta = 0
    else:
        car.delta += 90
    car.move = False
    TCPServerSocket.sendto(str(car.delta).encode())

def find_velocity_and_orientation():
    pass

def find_info_flowmap(car):
    # Assumes that coord x and y are between 0 and 200
    car.desired_orientation = fmdir[(car.x//10) - 1][(car.y//10) - 1]

if __name__ == "__main__":
    # read path from file and store information in a list of [x, y] values 
    # filename = "Path/PathCoordsNoDupes.txt"
    # path = []

    # with open(filename, "r") as file:
    #     path = file.readlines()
    #     path = [parseCoordFromLine(line) for line in path]

    # delta = 3 # hardcoded will need to be defined later on

    # # initialise car objects
    # # name = str(input("Car IP: "))
    # car1 = Car("CAR1", ("172.20.10.4", 9999))
    # cars = [car1]

    # camID = "cam"
    # stopID = "stop"
    # # set up server
    bufferSize = 4096

    # # TCPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
    # # TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # ServerAddr = ("172.20.10.2", 8888)

    # TCPServerSocket.bind(ServerAddr)
    # TCPServerSocket.connect(("172.20.10.2", 8888))
    # TCPServerSocket.listen()

      # This is the alternative code for TCP instead of UDP
    # My proposal is that we use one TCP socket for everything.
    
    
    HOST = "172.20.10.2"  # addr to bind to (generally server's computer local IP addr)
    PORT = 8000   # port to listen on (non-privileged ports are > 1023)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print(conn)
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(bufferSize)
                print("received")
                print(data)
    print("TCP server launched")
    # while(True):
    #     # TODO maybe add a way to check that all the values are valid without crashing the program
    #     recvInfo(camID, stopID, cars)