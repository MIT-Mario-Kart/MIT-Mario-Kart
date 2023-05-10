import socket

serverAddrPort = ("127.0.0.1", 8899)
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(serverAddrPort)
    s.sendall(b'CAL\n{"yellow": "[NSPoint(300, 300), NSPoint(300, 480), NSPoint(750, 300), NSPoint(750, 480)]"}')
    # s.sendall(b'CAL\n{"yellow": "[NSPoint(300, 300)]", "green": "[NSPoint(300, 480)]", "red": "[NSPoint(750, 300)]", "blue": "[NSPoint(750, 480)]"}')

    data = s.recv(bufferSize)

print(f"recv: {data!r}")
