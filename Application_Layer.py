from Data_Link_Layer import dataLinkLayer
import sys
import os
import math


class Application_Layer:
    def __init__(self, client_flag):
        self.dl = dataLinkLayer("127.0.0.1", 5555, client_flag, self)
        self.received_buffer = []

    def send(self):
        pass

    def receive(self, buffer):
        commd, numpieces, piece, data = self.parse_packet(buffer)
        if commd == "FILE":
            self.received_buffer.append(data)
            if numpieces == piece:
                self.make_file(self.received_buffer)

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
        data = packet_data.split('\n')
        commd = data[0][data[0].find('COMMAND:') + 8:]
        numpieces = data[1][data[1].find('PIECES:') + 7:]
        piece = data[2][data[2].find('PIECENUM:') + 9:]
        data = data[3][data[3].find('DATA:') + 5:]
        return commd, numpieces, piece, data

    def send_file(self):
        fileName = "D:/cnn_test.har"
        command = "FILE"
        with open(fileName, 'rb') as f:
            buffer = f.read()
            send_buffer = self.make_packet(command, buffer)
            for i in send_buffer:
                self.dl.send(1, i)

    def make_file(self, ):
        fileName = "Received_File.txt"
        with open(fileName, 'wb') as f:
            for i in range(0, len(self.received_buffer)):
                f.write(self.received_buffer[i])
