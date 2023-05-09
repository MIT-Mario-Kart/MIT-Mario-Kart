from socketserver import ThreadingTCPServer,BaseRequestHandler
import socket
from Algo.Control import recvInfo

# set up server
bufferSize = 4096

class handler(BaseRequestHandler):
    clients = set()

    def handle(self):
        print(f'Connected: {self.client_address[0]}:{self.client_address[1]}')
        self.clients.add(self.request)
        
        while True:
            msg = self.request.recv(bufferSize)
            if not msg:
                print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                break # exits handler, framework closes socket
            print(f'Received: {msg}')
            toSend = recvInfo(msg)
            if toSend:
                if toSend == "CAL":
                    self.sendToCameraAck()
                else:
                    self.request.send((str(toSend) + "\n").encode())
                    print(f"Sent {toSend}")

    def sendToCameraAck(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # define the address and port to send the request to
        address = (self.client_address[0], 12345)

        # send the request
        message = b'Calibrated'
        sock.sendto(message, address)
        sock.close()

            

class MainServer(ThreadingTCPServer):
    def __init__(self, server_address):
        super().__init__(server_address, handler)
            