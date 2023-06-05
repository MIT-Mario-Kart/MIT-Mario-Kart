from socketserver import ThreadingTCPServer,BaseRequestHandler
import socket

# set up server
bufferSize = 4096

class handler(BaseRequestHandler):
    clients = set()

    # Handle method called for every new connection. It keeps track of every new client and calls the recvInfo
    # method from Control.
    def handle(self):
        print(f'Connected: {self.client_address[0]}:{self.client_address[1]}')
        self.clients.add(self.request)
        
        while True:
            msg = self.request.recv(bufferSize)
            if not msg:
                print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                break # exits handler, framework closes socket
            
            toSend = self.server.control.recvInfo(msg)

            if toSend != None:
                if toSend == "CAL":
                    self.sendToCameraAck()
                else:
                    self.request.send((str(toSend) + "\n").encode()) # sends the information needed by each car

    #  Opens a UDP socket and acknowledges the calibration initiated by the camera
    def sendToCameraAck(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # define the address and port to send the request to
        address = (self.client_address[0], 12345)

        # send the request
        message = b'Calibrated'
        sock.sendto(message, address)
        sock.close()

            
# Our MainServer class is a subclass of ThreadingTCPServer, meaning that it will open a thread for each new connection
# and keep it as long as it is not closed either by the server itself or the other party.This class needs a handler 
# (which will inherit from a BaseRequestHandler), this will determine the function that is called for every new connection.
class MainServer(ThreadingTCPServer):
    def __init__(self, server_address, control_in):
        super().__init__(server_address, handler)
        self.control = control_in # save the instance of control needed to update each car in the game