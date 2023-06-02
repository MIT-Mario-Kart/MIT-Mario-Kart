from socketserver import ThreadingTCPServer,BaseRequestHandler
import socket
from datetime import datetime

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
            # print(f'Received: {msg}')
            
            # If the string contains CR_ID_PU then it's coming from the car
            # We need to get rid of the end of the string
            # 'CAR_ID_RESET\x00\x03\x00\x00\xe4\xe9\xfe?Z\x00\x00\x00\x0c\x00\x00\x00DS @\xc4\x88\xfe?\xfc\xff\xff\xff'
            
            if "CAR_ID_" in str(msg):
                #will be received one time
                # msg = str(msg).split("\\n")[0][2:] + "\n" + str(msg).split("\\n")[1][0]
                toSend = self.server.control.recvInfo(msg, self.request)
            else:
                #current_time = datetime.now()
                #print(current_time)
                toSend = self.server.control.recvInfo(msg)

            if toSend != None:
                if toSend == "CAL":
                    self.sendToCameraAck()
                else:
                    #pass
                    print(f"Sent {toSend}")
                    #self.request.send((str(toSend) + "\n").encode())

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
    def __init__(self, server_address, control_in):
        super().__init__(server_address, handler)
        self.allow_reuse_address = True
        self.control = control_in