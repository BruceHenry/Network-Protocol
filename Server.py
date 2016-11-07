# from Data_Link_Layer import dataLinkLayer
# import time
#
# dl = dataLinkLayer(5555, 0)
# while True:
#     time.sleep(1)


import time
from Application_Layer import Application_Layer
import atexit

mode = 1

app = Application_Layer(0, mode)

@atexit.register
def goodbye():
    app.dl.p.destroy()

while True:
    time.sleep(1)

