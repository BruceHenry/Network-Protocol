import socket
import threading
import socketserver
import random

framesize = 1024
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
        self.data =  data

    def data(self):
        return self.data

    def add_corruption(self):
        self.data[random.randint(0,len(data))] = '*'
        self.data[random.randint(0,len(data))] = '5'
        self.data[random.randint(0,len(data))] = 'V'
        self.data[random.randint(0,len(data))] = '?'


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class physicalRequestHandler(socketserver.BaseRequestHandler):

        def handle(self):
            data = str(self.request.recv(framesize),'utf-8')
            print (data)
            self.server.data_layer.receive(1,data)


class physicalLayer():
    def __init__(self, ip, port, data_layer):
        self.ip = ip
        self.port = port

        self.server = ThreadedTCPServer(('localhost', self.port), physicalRequestHandler)

        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.server.data_layer = data_layer

        self.server_thread.daemon = True
        self.server_thread.start()


        print ("Server loop running in thread:", self.server_thread.name)


    def send(self, data):
        f = Frame(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        try:
            if(is_dropped(chance_of_fail)):
                print ('Corrupted frame')
            else:
                if(is_corrupted(chance_of_corruption)):
                    f.add_corruption()
                sock.sendall(bytes(f.data, 'utf-8'))
                response = sock.recv(framesize)
        finally:
            sock.close()

    def destroy(self):
        self.server.shutdown()
        self.server.server_close()
