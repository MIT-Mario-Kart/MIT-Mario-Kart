from MainServerClass import MainServer

time_delta = 0.1 # in seconds


server = MainServer(('', 8888), time_delta)
server.serve_forever()
# if stop:
#     server.shutdown()
