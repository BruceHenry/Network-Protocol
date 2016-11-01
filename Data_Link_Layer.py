from Physical_Layer import physicalLayer
import threading
import _thread


class packet:
    seq = 0
    ack = 0
    buffer = ""

    def __init__(self):
        pass

    def __init__(self, buffer):
        self.buffer = buffer

    def set_seq_ack(self, seq, ack):
        self.seq = seq
        self.ack = ack



# packet format(temp):
# 1st byte:seq
# 2nd byte:space
# 3rd byte:ack
# 4th byte:space
# 5th and later:data

class dataLinkLayer:
    p = physicalLayer()
    windowSize = 5
    send_buffer = []
    receive_buffer = []

    next_expected_seq=0
    timer=self.timer();

    base = 0
    next_seq = 0

    def send(self, mode, buffer):

        if mode == 1:
            self.go_back_n_sender(packet(buffer))
            return 1
        elif mode == 2:
            self.selective_repeat_sender()
            return 1
        else:
            return -1

    def receive(self, mode):
        if mode==1:
            self.go_back_n_receiver()
            return 1
        elif mode==2:
            self.selective_repeat_receiver()
            return 1
        else:
            return -1

    # def send_ack(self, seq):
    #     self.seq += 1
    #     ack = seq + 1
    #     message = str(self.seq) + " " + str(ack)
    #     return message

    def make_packet(self, pkt):
        packet_without_checksum=str(pkt.seq)+ str(pkt.ack)+pkt.buffer
        checksum=self.ichecksum(packet_without_checksum)
        return str(pkt.seq) + " " + str(pkt.ack) + " " +str(checksum)+" "+pkt.buffer

    def refuse(self,packet):
        print("Window full, cannot send data now")
        return False



    # thread for sending
    def go_back_n_send(self,packet):
            # send
            if self.next_seq < self.base + self.windowSize:
                self.send_buffer.append(packet)
                self.send_buffer[self.next_seq].set_seq_ack(self.next_seq,0)
                self.p.send(self.make_packet(self.send_buffer[self.next_seq]))
                if self.base == self.next_seq:
                    self.timer.start()
                self.next_seq += 1
                return True
            else:
                self.refuse(packet)


    # thread for timer
    def go_back_n_timeout(self):
            # Timeout
            self.timer.start()
            for i in range(self.base, self.next_seq):
                self.p.send(self.make_packet(self.send_buffer[i]))

    # thread for receiving ack...
    def go_back_n_receive(self):
        while True:
            buffer = self.p.receive()
            if buffer[4] == '1':  # check integrity(suppose 1 means NOT intact)
                self.p.send(self.make_packet(self.send_buffer[buffer[2]]))
            else:
                self.base = buffer[2] + 1
                if self.base == self.next_seq:
                    self.timer.cancel()
                else:
                    self.timer.start()


    # the receiver in go_back_n
    def go_back_n_receiver(self):


        buffer = self.p.receive()
        packet=buffer.split(" ")
        seq=packet[0]
        ack=int(packet[1])
        checksum=packet[2]
        if(not ack):
            data=packet[3]
            valid=self.ichecksum(seq+ack+data,checksum)
            ack_pkt = packet("")
            if(not valid and self.next_expected_seq==seq):
                ack_pkt.set_seq_ack(self.next_expected_seq,1)
                self.p.send(self.make_packet(ack_pkt))
                self.next_expected_seq+=1
                return  data
            elif(self.next_expected_seq!=seq):
                print("Out of order packet")
                ack_pkt.set_seq_ack(self.next_expected_seq-1, 1)
                self.p.send(self.make_packet(ack_pkt))
                return False
        else:
            valid = self.ichecksum(seq + ack , checksum)
            if(not valid and self.base!=int(seq)):
                self.base=int(seq)+1
                if(self.base==self.next_seq)
                    self.timer.cancel()



    # Return a timer object
    # Use timer.cancel() to stop the timer
    def timer(self, timeout):
        timer = threading.Timer(timeout, self.go_back_n_timeout())
        return timer

    def ichecksum(data, sum=0):
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
