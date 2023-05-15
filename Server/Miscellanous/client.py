import socket

serverAddrPort = ("127.0.0.1", 8888)
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(serverAddrPort)
    s.sendall(b"HEY")
    data = s.recv(bufferSize)

print(f"recv: {data!r}")