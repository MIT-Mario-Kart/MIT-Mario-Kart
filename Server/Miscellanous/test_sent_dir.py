import socket

serverAddrPort = ("127.0.0.1", 8899)
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(serverAddrPort)
    s.sendall(b'CAR_ID_TEST\n.')
    data = s.recv(bufferSize)

print(f"recv: {data!r}")