# from Data_Link_Layer import dataLinkLayer
# import time
#
# dl = dataLinkLayer(5555, 1)
# time.sleep(2)
# i = 0
# while True:
#     dl.send(1, "Hello world%d" % i)
#     i += 1
#     time.sleep(2)


from Application_Layer import Application_Layer
import _thread

app = Application_Layer(1, 1)
print("Please input:\nUPLOAD [File URL]\nDOWNLOAD [File URL]\nCALCULATE [expression]")
while True:
    command = input()
    _thread.start_new_thread(app.send, (command,))
