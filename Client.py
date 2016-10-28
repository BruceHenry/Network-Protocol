import socket
import sys
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 9999
s.connect((host, port))

fileName = "D:/cnn_test.har"
with open(fileName, 'rb') as f:
    size = os.path.getsize(fileName)
    buffers = []
    for n in range(0, int(size / 256) + 1):
        buffer = f.read(256)#.decode("utf-8-sig")
        s.send(buffer)
while True:
    msg = s.recv(1024)
    print(msg.decode('utf-8'))
    if msg.decode('utf-8') == "end":
        break
s.close()

str=input()
application(str)