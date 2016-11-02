import math

class applicationLayer:

    maxBytes = 256

    def init(self, data_link_layer):
        self.datalinklayer = data_link_layer

    commands = ['SENDFILE', 'MSG', 'CALCULATE', 'RESPONSE']
    command_handlers = []

    packet_format = 'COMMAND:{0}\nPIECES:{1}\nPIECENUM:{2}\nDATA:{3}'

    def make_packet(self, command, message):
        packets_to_send = []
        if len(message) > self.maxBytes:
            numpieces = math.ceil(len(message)/float(self.maxBytes))
            for x in range (0, int(numpieces)):
                chunk = self.maxBytes if x < numpieces else len(message) % self.maxBytes
                packets_to_send.append(self.packet_format.format(command,
                    numpieces,
                    x+1,
                    message[0:chunk]
                    ))
                message = message[chunk:]
            return packets_to_send
        else:
            return [self.packet_format.format(command, 0, 0, message)]


    def parse_packet(self, packet_data):
        data = packet_data.split('\n')
        commd = data[0][data[0].find('COMMAND:')+8:]
        numpieces = data[1][data[1].find('PIECES:')+7:]
        piece = data[2][data[2].find('PIECENUM:')+9:]
        data = data[3][data[3].find('DATA:')+5:]
        return commd,numpieces,piece,data

    def handle_msg(data):
        print "I got " + data


    command_handlers = [handle_msg, handle_msg, handle_msg, handle_msg]



app = applicationLayer()

pack = app.send_msg('Hello this is a test. And a really long message. But I mean')

app.parse_packet(pack[0])
