import socket

serverAddrPort = ("172.20.10.2", 8888)
bufferSize = 1024

# connecting to hosts
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
bytesToSend1 = "25, 66".encode()
bytesToSend2 = "168, 157".encode()
# sending username by encoding it
UDPClientSocket.sendto(bytesToSend1, serverAddrPort)
# sending password by encoding it
UDPClientSocket.sendto(bytesToSend2, serverAddrPort)

# receiving status from server
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0].decode())
print(msg)
