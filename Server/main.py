from MainServerClass import MainServer
import GUI
from Algo.Control import cars
server = MainServer(('', 8899))
server.serve_forever()

# gui = GUI.GUI()
# gui.launchGUI(cars)