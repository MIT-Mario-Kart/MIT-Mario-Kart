from MainServerClass import MainServer

server = MainServer(('', 8888))
server.serve_forever()
