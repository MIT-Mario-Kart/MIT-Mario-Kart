from MainServerClass import MainServer
from Server.Miscellanous import launch_gui

server = MainServer(('', 8893))
server.serve_forever()

launch_gui