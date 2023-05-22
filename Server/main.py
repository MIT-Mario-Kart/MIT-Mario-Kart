from MainServerClass import MainServer

server = MainServer(('', 8899))
server.serve_forever()

