import socket
import threading
import socketserver
import random

framesize = 1024
chance_of_fail = 0
chance_of_corruption = 10


def is_dropped(chance_of_fail):
    number = random.randint(1, 100)
    if number <= chance_of_fail:
        return True
    else:
        return False


def is_corrupted(chance_of_corruption):
    number = random.randint(1, 100)
    if number <= chance_of_corruption:
        return True
    else:
        return False


class Frame():
    def __init__(self, data):
        self.data = '[' + data + ']'

    def getdata(self):
        return self.data

    def add_corruption(self):
        ls = list(self.data)
        ls[random.randint(0, framesize)] = '*'
        ls[random.randint(0, framesize)] = '5'
        ls[random.randint(0, framesize)] = 'V'
        ls[random.randint(0, framesize)] = '?'
        self.data = ''.join(ls)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class physicalLayer(socketserver.BaseRequestHandler):
    def __init__(self, ip, port, data_layer):
        self.ip = ip
        self.port = port
        self.data_layer = data_layer

        self.server = ThreadedTCPServer(('localhost', self.port), self)

        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.server_thread.daemon = True
        self.server_thread.start()

        print("Server loop running in thread:", self.server_thread.name)

    def send(self, data):
        f = Frame(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        try:
            if (is_dropped(chance_of_fail)):
                print('Corrupted frame')
            else:
                if (is_corrupted(chance_of_corruption)):
                    f.add_corruption()

                print(f.getdata())

                sock.sendall(f.getdata().encode())
                response = sock.recv(framesize)
                #print(response)
        finally:
            sock.close()

    def handle(self):
        data = self.request.recv(framesize)
        self.data_layer.go_back_n_receiver(data)

    def destroy(self):
        self.server.shutdown()
        self.server.server_close()
