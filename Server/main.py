from MainServerClass import MainServer

server = MainServer(('', 8893))
server.serve_forever()
