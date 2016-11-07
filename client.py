from Application_Layer import Application_Layer
from Server import mode

app = Application_Layer(1, mode)
print("Please input:\nUPLOAD [File URL]\nDOWNLOAD [File URL]\nCALCULATE [expression]")
while True:
    command = input()
    app.send(command)
