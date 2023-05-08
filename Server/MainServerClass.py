from socketserver import ThreadingTCPServer,BaseRequestHandler
from Algo.Control import recvInfo

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
                self.request.send((str(toSend) + "\n").encode())
                print(f"Sent {toSend}")

class MainServer(ThreadingTCPServer):
    def __init__(self, server_address, time_interval):
        super().__init__(server_address, handler)
            