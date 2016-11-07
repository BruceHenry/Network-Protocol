from Data_Link_Layer import dataLinkLayer
import sys
import os
import math
import time
import base64


class Application_Layer:
    maxBytes = 256
    packet_format = 'COMMAND:{0}\nPIECES:{1}\nPIECENUM:{2}\nDATA:{3}'
    commands = ['LOG', 'CALCULATE', 'RESPONSE', 'DOWNLOAD', 'UPLOAD']

    def __init__(self, client_flag, mode):
        self.start_time = 0
        self.endtime = 0
        self.mode = mode
        self.dl = dataLinkLayer("127.0.0.1", 5555, client_flag, self)
        self.received_buffer = []
        self.client_flag = client_flag
        self.log = {"time": 0,
                    "mode":mode
                    }

    def send(self, input):
        self.start_time = time.time()
        command = input.split(" ")
        if command[0] == self.commands[4] and self.client_flag:
            self.send_file(command[1])
        elif command[0] == self.commands[3] and self.client_flag:
            packets = self.make_packet(command[0], command[1])
            self.dl.send(self.mode, packets[0])
        elif command[0] == self.commands[1] and self.client_flag:
            packets = self.make_packet(command[0], command[1])
            print(packets)
            self.dl.send(self.mode, packets[0])
        elif command[0] == self.commands[0] and self.client_flag:
            self.write_log()
        else:
            print("Invalid command!!!")
        self.endtime = time.time()
        self.log["time"] += self.endtime - self.start_time

    def receive(self, buffer):
        # print("app received:", buffer, '\n----------')
        self.start_time = time.time()
        commd, numpieces, piece, data = self.parse_packet(buffer)
        if commd == "FILE":
            self.received_buffer.append(data)
            if numpieces == piece:
                self.make_file()
        elif commd == self.commands[3] and not self.client_flag:
            self.send_file(str(data))
        elif commd == self.commands[2] and self.client_flag:
            print("Result :", data)
        elif commd == self.commands[1] and not self.client_flag:
            self.calculate(str(data))
        # elif commd == self.commands[0] and not self.client_flag:
        #     self.write_log()
        elif commd == "EXIT":
            self.destroy()
            self.endtime = time()
            self.log["time"] += self.endtime - self.start_time

        self.endtime = time.time()
        self.log["time"] += self.endtime - self.start_time

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
        extension = self.get_extension(fileName)
        extension_packet = self.packet_format.format(command, 1, 0, extension)
        self.dl.send(self.mode, extension_packet)
        with open(fileName, 'r') as f:
            buffer = f.read()
            send_buffer = self.make_packet(command, buffer)
            for i in send_buffer:
                while True:
                    if self.dl.send(self.mode, i):
                        break
                    else:
                        time.sleep(0.5)
                        continue
                # print("send:", i, "\n----------")
                time.sleep(0.1)
        print("The file has sent!")

    def make_file(self):
        fileName = "Received_File" + '.' + self.received_buffer[0]

        with open(fileName, 'w') as f:
            for i in range(1, len(self.received_buffer)):
                f.write(self.received_buffer[i])
            f.flush()
        print("A file is received!")
        self.received_buffer = []

    def calculate(self, expression):
        command = self.commands[2]
        try:
            result = eval(expression)
        except:
            result = "Not an valid expression,please try again"
        finally:
            buffer = self.make_packet(command, str(result))
            self.dl.send(self.mode, buffer[0])

    def get_extension(self, file_url):
        names = file_url.split(".")
        extension = names[len(names) - 1]
        return extension

    def write_log(self):
        if self.client_flag == 1:
            file_name = "Client_Log.txt"
            # packets = self.make_packet(self.commands[0], "Write log")
            # print(packets)
            # self.dl.send(self.mode, packets)
        else:
            file_name = "Server_log.txt"
        with open(file_name, 'a') as f:
            f.write(str(self.dl.p.log))
            f.write(str(self.dl.log))
            f.write(str(self.log))
            f.write("\n")
            f.flush()
            print("Log has been written")