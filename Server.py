import socket
import sys

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 9999
serversocket.bind((host, port))
serversocket.listen(5)

clientsocket, addr = serversocket.accept()
fileName = "receivedFile.txt"
f = open(fileName, "wb")
while True:
    buffer = clientsocket.recv(256)
    f.write(buffer)
f.close()


while True:
    clientsocket, addr = serversocket.accept()
    print("Address: %s" % str(addr))
    msg = 'Welcom!' + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    while True:
        msg = input()
        clientsocket.send(msg.encode('utf-8'))
        if msg == "end":
            break
    clientsocket.close()
