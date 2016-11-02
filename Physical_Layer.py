import socket
import threading
import SocketServer
import random


framesize = 1024l
chance_of_fail = 0
chance_of_corruption = 10

def is_dropped(chance_of_fail):
    number = random.randint(1,100)
    if number <= chance_of_fail:
        return True
    else:
        return False

def is_corrupted(chance_of_corruption):
    number = random.randint(1,100)
    if number <= chance_of_corruption:
        return True
    else:
        return False


class Frame():
    def __init__(self, data):
        self.data = '[' + data + ']'

    def data(self):
        return self.data

    def add_corruption(self):
        self.data[random.randint(0,framesize)] = '*'
        self.data[random.randint(0,framesize)] = '5'
        self.data[random.randint(0,framesize)] = 'V'
        self.data[random.randint(0,framesize)] = '?'


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class physicalLayer(SocketServer.BaseRequestHandler):
    def __init__(self, ip, port, data_layer):
        self.ip = ip
        self.port = port
        self.data_layer = data_layer

        self.server = ThreadedTCPServer(('localhost', self.port), self)

        self.server_thread = threading.Thread(target=server.serve_forever)

        self.server_thread.daemon = True
        self.server_thread.start()

        print "Server loop running in thread:", server_thread.name

    def send(self, data):
        f = frame(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        try:
            if(is_dropped(chance_of_fail)):
                print 'Corrupted frame'
            else:
                if(is_corrupted(chance_of_corruption)):
                    frame.add_corruption()
                sock.sendall(frame.data())
                response = sock.recv(framesize)
        finally:
            sock.close()

    def handle(self):
        data = self.request.recv(framesize)
        self.data_layer.receive()

    def destroy(self):
        self.server.shutdown()
        self.server.server_close()
