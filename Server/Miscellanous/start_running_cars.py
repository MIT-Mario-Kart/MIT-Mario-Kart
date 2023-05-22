import socket

serverAddrPort = ("172.20.10.6", 8899                   )
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(serverAddrPort)
    s.sendall(b"START")
