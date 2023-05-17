import socket

serverAddrPort = ("172.20.10.2", 8998)
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(serverAddrPort)
    s.sendall(b"STOP")
