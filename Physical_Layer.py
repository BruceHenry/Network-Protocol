import socket
import _thread
import threading
import socketserver
import random

import time

framesize = 1024
chance_of_fail = 5
chance_of_corruption = 5


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


class Frame():
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
        if not client_flag:
            self.client_flag = 0
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.bind((self.ip, self.port))
            serversocket.listen(5)
            print("Server running and listening for client")
            self.soc, addr = serversocket.accept()
            _thread.start_new_thread(receive, (self,))
            # self.server = ThreadedTCPServer(('localhost', self.port), physicalRequestHandler)
            # self.server_thread = threading.Thread(target=self.server.serve_forever)
            # self.server_thread.daemon = True
            # self.server_thread.start()
            # print("Server loop running in thread:", self.server_thread.name)
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
                print('Corrupted frame')
            else:
                if (is_corrupted(chance_of_corruption)):
                    f.add_corruption()
                self.soc.sendall(bytes(f.data, 'utf-8'))
        except:
            pass
            #self.soc.close()

    def destroy(self):
        self.soc.close()


def receive(dl):
    print("Receive thread created")
    while (True):
        try:
            data = str(dl.soc.recv(framesize), 'utf-8')
        except:
            continue
        # print("phyical receiver:", data)
        if data == "":
            continue
        dl.data_layer.receive(1, data)
