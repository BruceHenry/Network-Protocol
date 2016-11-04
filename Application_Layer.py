from Data_Link_Layer import dataLinkLayer
import sys
import os
import math
import time
import base64


class Application_Layer:
    maxBytes = 256
    packet_format = 'COMMAND:{0}\nPIECES:{1}\nPIECENUM:{2}\nDATA:{3}'

    def __init__(self, client_flag):
        self.dl = dataLinkLayer("127.0.0.1", 5555, client_flag, self)
        self.received_buffer = []

    def send(self, input):
        command = input.split(" ")
        if command[0] == "UPLOAD":
            self.send_file(command[1])

    def receive(self, buffer):
        # print("app received:", buffer, '\n----------')
        commd, numpieces, piece, data = self.parse_packet(buffer)
        if commd == "FILE":
            self.received_buffer.append(data)
            if numpieces == piece:
                self.make_file()
        if commd == "EXIT":
            self.destroy()

    def make_packet(self, command, message):
        packets_to_send = []
        if len(message) > self.maxBytes:
            numpieces = math.ceil(len(message) / float(self.maxBytes))
            for x in range(0, int(numpieces)):
                chunk = self.maxBytes if x < numpieces else len(message) % self.maxBytes
                packets_to_send.append(self.packet_format.format(command,
                                                                 numpieces,
                                                                 x + 1,
                                                                 message[0:chunk]
                                                                 ))
                message = message[chunk:]
            return packets_to_send
        else:
            return [self.packet_format.format(command, 0, 0, message)]

    def parse_packet(self, packet_data):
        data = packet_data.split('\n', 3)
        commd = data[0][data[0].find('COMMAND:') + 8:]
        numpieces = data[1][data[1].find('PIECES:') + 7:]
        piece = data[2][data[2].find('PIECENUM:') + 9:]
        data = data[3][data[3].find('DATA:') + 5:]
        return commd, numpieces, piece, data

    def send_file(self, file_path):
        # fileName = "D:/a.txt"
        fileName = file_path
        command = "FILE"
        with open(fileName, 'r') as f:
            buffer = f.read()
            send_buffer = self.make_packet(command, buffer)
            for i in send_buffer:
                while True:
                    if self.dl.send(1, i):
                        break
                    else:
                        time.sleep(0.5)
                        continue
                # print("send:", i, "\n----------")
                time.sleep(0.1)

    def make_file(self):
        fileName = "Received_File.txt"

        with open(fileName, 'w') as f:
            for i in range(0, len(self.received_buffer)):
                f.write(self.received_buffer[i])
            f.flush()
        self.received_buffer = []
