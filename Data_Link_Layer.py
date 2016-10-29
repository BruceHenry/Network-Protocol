from Physical_Layer import physicalLayer
import threading

class packet:
    seq = 0
    ack = 0
    buffer = ""
    # timer

    def set_seq_ack(self, seq, ack):
        self.seq = seq
        self.ack = ack


class dataLinkLayer:
    p = physicalLayer()
    seq = 0
    ack = 0
    windowSize = 5
    send_buffer = []
    receive_buffer = []

    def send(self, buffer):
        self.buffer = buffer
        self.p.send()

    def receive(self):
        self.p.send(self.seq, self.ack)
        return self.buffer

    # def send_ack(self, seq):
    #     self.seq += 1
    #     ack = seq + 1
    #     message = str(self.seq) + " " + str(ack)
    #     return message

    def make_packet(self, pkt):
        return str(pkt.seq) + " " + str(pkt.ack) + " " + pkt.buffer

    def go_back_n(self):
        base = 0
        next_seq = 0
        ack = 0
        while True:#send
            if next_seq < base + self.windowSize:
                self.send_buffer[next_seq].set_seq_ack(self.seq, self.ack)
                self.p.send(self.make_packet(self.send_buffer[next_seq]))
                self.seq += 1
                if base == next_seq:
                    pass
                    # start_timer()
                next_seq += 1
            else:
                break
        while True:#Timeout
            # start_timer()
            for i in range(base, next_seq):
                self.p.send(self.make_packet(self.send_buffer[i]))


    def retransmit(self):
        pass



    #Return a timer object
    #Use timer.cancel() to stop the timer
    def timer(self,timeout):
        timer = threading.Timer(timeout, self.retransmit())
        return timer






    def selective_repeat(self):
        pass

    def main(self):
        pass

