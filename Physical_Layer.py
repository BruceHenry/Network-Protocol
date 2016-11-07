import socket
import _thread
import threading
import socketserver
import random


import time
from constant import *

framesize = 512



def is_dropped(chance_of_fail):
    number = random.randint(1, 100)
    if number <= chance_of_fail:
        print("A packet is dropped")
        return True
    else:
        return False


def is_corrupted(chance_of_corruption):
    number = random.randint(1, 100)
    if number <= chance_of_corruption:
        print("A packet is corrupted")
        return True
    else:
        return False


class Frame:
    def __init__(self, data):
        self.data = data

    def data(self):
        return self.data

    def add_corruption(self):
        ls = list(self.data)
        ls[random.randint(0, len(self.data))] = '*'
        ls[random.randint(0, len(self.data))] = '5'
        ls[random.randint(0, len(self.data))] = 'V'
        ls[random.randint(0, len(self.data))] = '?'
        self.data = ''.join(ls)


# class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass


# class physicalRequestHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         data = str(self.request.recv(framesize), 'utf-8')
#         self.server.data_layer.receive(1, data)


class physicalLayer():
    def __init__(self, ip, port, data_layer, client_flag):
        self.ip = ip
        self.port = port
        self.data_layer = data_layer
        self.log = {"total_frame": 0, "total_data": 0, "drop_chance": 0, "corrupt_chance": 0}
        if not client_flag:
            self.client_flag = 0
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serversocket.bind((self.ip, self.port))
            serversocket.listen(5)
            print("Server running and listening for client")
            self.soc, addr = serversocket.accept()
            _thread.start_new_thread(receive, (self,))
        else:
            self.client_flag = 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, self.port))
            self.soc = sock
            _thread.start_new_thread(receive, (self,))

    def send(self, data):
        f = Frame(data)
        try:
            if (is_dropped(chance_of_fail)):
                # print('Corrupted frame')
                pass
            else:
                if (is_corrupted(chance_of_corruption)):
                    f.add_corruption()
                padded_length = framesize - 1 - len(f.data) - len(str(len(f.data)))
                padded_frame = f.data.ljust(len(f.data) + padded_length, ' ')
                sent_frame = str(len(f.data)) + ' ' + padded_frame
                self.log['total_frame'] += 1
                self.log['total_data'] += len(f.data)
                self.log['drop_chance'] = chance_of_fail
                self.log['corrupt_chance'] = chance_of_corruption
                self.soc.sendall(bytes(sent_frame, 'utf-8'))
        except:
            pass
            # self.soc.close()

    def destroy(self):
        self.soc.close()


def receive(dl):
    print("Receive thread created")
    while (True):
        try:
            data = str(dl.soc.recv(framesize), 'utf-8')
            padding = data.split(" ", 1)
            payload = padding[1][0:int(padding[0])]


        except:
            continue
        # print("phyical receiver:", data)
        if data == "":
            continue
        dl.data_layer.receive(mode, payload)
