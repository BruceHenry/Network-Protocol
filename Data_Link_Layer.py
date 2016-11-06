from Physical_Layer import physicalLayer
import threading
import _thread


class packet:
    seq = 0
    ack = 0
    buffer = ""

    def __init__(self, buffer):
        self.buffer = buffer

    def set_seq_ack(self, seq, ack):
        self.seq = seq
        self.ack = ack


class dataLinkLayer:
    windowSize = 5
    send_buffer = []
    receive_buffer = []

    next_expected_seq = 0

    base = 0
    next_seq = 0

    def __init__(self, ip, port, client_flag, application_layer):
        self.client_flag = client_flag
        self.p = physicalLayer(ip, port, self, client_flag)
        self.app = application_layer
        self.t = self.timer(0.5)
        self.log = {"retransmission": 0,
                    "ack_sent": 0,
                    "ack_received": 0,
                    "duplicate": 0,
                    "start_time": 0,
                    "end_time": 0,
                    "time": 0,
                    }

    def send(self, mode, buffer):
        if mode == 1:
            if self.go_back_n_send(packet(buffer)):
                return True
            else:
                return False

        elif mode == 2:
            if self.selective_repeat_sender():
                return True
            else:
                return False

    def receive(self, mode, data):
        if mode == 1:
            if self.go_back_n_receiver(data):
                return True
            else:
                return False

        elif mode == 2:
            if self.selective_repeat_receiver():
                return True
            else:
                return False

    def make_packet(self, pkt):
        packet_without_checksum = str(pkt.seq) + str(pkt.ack) + pkt.buffer
        checksum = self.ichecksum(packet_without_checksum)
        return str(pkt.seq) + " " + str(pkt.ack) + " " + str(checksum) + " " + pkt.buffer

    # def refuse(self, packet):
    #     print("Window full, cannot send data now")
    #     return False

    def go_back_n_send(self, packet):
        # send
        if self.next_seq < self.base + self.windowSize:
            self.send_buffer.append(packet)
            self.send_buffer[self.next_seq].set_seq_ack(self.next_seq, 0)
            self.p.send(self.make_packet(self.send_buffer[self.next_seq]))
            print("go_back_n_send:", self.send_buffer[self.next_seq].seq, self.send_buffer[self.next_seq].ack)
            if self.base == self.next_seq:
                self.setTimer()
                self.t.start()
            self.next_seq += 1
            return True
        else:
            print("Window full, cannot send data now")
            return False

    def go_back_n_timeout(self):
        # Timeout
        self.t.cancel()
        self.setTimer()
        self.t.start()
        for i in range(self.base, self.next_seq):
            self.p.send(self.make_packet(self.send_buffer[i]))
            print("timeout re-send", self.send_buffer[i].seq, self.send_buffer[i].ack)

    # the receiver in go_back_n
    def go_back_n_receiver(self, buffer):
        # buffer = self.p.receive()
        print("go_back_n_receiver:", buffer[:22])
        packet_slice = buffer.split(" ", 3)
        if len(packet_slice) != 4:
            return False
        try:
            seq = int(packet_slice[0])
            ack = int(packet_slice[1])
            checksum = int(packet_slice[2])
            data = packet_slice[3]
        except:
            return False

        if not ack:
            valid = self.ichecksum(str(seq) + str(ack) + data, checksum)
            ack_pkt = packet("ACK")
            if (not valid and self.next_expected_seq == seq):
                ack_pkt.set_seq_ack(self.next_expected_seq, 1)
                self.p.send(self.make_packet(ack_pkt))
                self.next_expected_seq += 1
                # return data
                self.app.receive(data)


            elif self.next_expected_seq != seq:
                print("Out of order packet")
                ack_pkt.set_seq_ack(self.next_expected_seq - 1, 1)
                self.p.send(self.make_packet(ack_pkt))
                return False
        else:
            valid = self.ichecksum(str(seq) + str(ack) + data, checksum)
            if (not valid and self.base <= int(seq)):
                self.base = int(seq) + 1
                if self.base == self.next_seq:
                    self.t.cancel()
                else:
                    self.setTimer()
                    self.t.start()

    # Return a timer object
    # Use timer.cancel() to stop the timer
    def timer(self, timeout):
        timer = threading.Timer(timeout, self.go_back_n_timeout, ())
        return timer

    def setTimer(self):
        self.t = self.timer(0.5)

    def ichecksum(self, data, sum=0):
        """ Compute the Internet Checksum of the supplied data.  The checksum is
        initialized to zero.  Place the return value in the checksum field of a
        packet.  When the packet is received, check the checksum, by passing
        in the checksum field of the packet and the data.  If the result is zero,
        then the checksum has not detected an error.
        """
        # make 16 bit words out of every two adjacent 8 bit words in the packet
        # and add them up
        for i in range(0, len(data), 2):
            if i + 1 >= len(data):
                sum += ord(data[i]) & 0xFF
            else:
                w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i + 1]) & 0xFF)
                sum += w

        # take only 16 bits out of the 32 bit sum and add up the carries
        while (sum >> 16) > 0:
            sum = (sum & 0xFFFF) + (sum >> 16)

        # one's complement the result
        sum = ~sum

        return sum & 0xFFFF

    def selective_repeat_sender(self):
        pass

    def selective_repeat_receiver(self):
        pass

        return sum & 0xFFFF

    def selective_repeat_sender(self):
        pass

    def selective_repeat_receiver(self):
        pass

        # d = dataLinkLayer(5425)
        # d.send(1, 'blahblahblah')
