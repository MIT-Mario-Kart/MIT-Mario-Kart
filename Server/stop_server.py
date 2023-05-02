import socket

serverAddrPort = ("172.20.10.2", 8000)
bufferSize = 1024

# connecting to hosts
TCPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
bytesToSend = "stop".encode()
stop_server = ""
while (stop_server != "y"):
    stop_server = input("Stop Server? ")
TCPClientSocket.sendto(bytesToSend, serverAddrPort)
