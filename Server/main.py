from MainServerClass import MainServer
from Algo.Control import cars
import threading
import GUI

def launch_server():
    server = MainServer(('', 8899))
    server.serve_forever()

my_thread = threading.Thread(target=launch_server)
my_thread.start()

gui = GUI.GUI()
gui.launchGUI(cars)
