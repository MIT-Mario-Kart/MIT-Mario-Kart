import socket

serverAddrPort = ("127.0.0.1", 9999)
bufferSize = 1024

# connecting to hosts
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
bytesToSend1 = "1".encode()
UDPClientSocket.bind((serverAddrPort[0], serverAddrPort[1]))
val, addr = UDPClientSocket.recvfrom(bufferSize)
stop_server = ""
while (stop_server != "yes"):
    stop_server = input("Stop Server? ")
UDPClientSocket.sendto(bytesToSend1, addr)
