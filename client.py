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
    app.send(command)
    print("Press any key to write log")
    write_log = input()
    app.write_log()
