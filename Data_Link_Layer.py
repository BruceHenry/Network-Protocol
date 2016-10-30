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


# packet format(temp):
# 1st byte:seq
# 2nd byte:space
# 3rd byte:ack
# 4th byte:space
# 5th and later:data

class dataLinkLayer:
    p = physicalLayer()
    seq = 0
    ack = 0
    windowSize = 5
    send_buffer = []
    receive_buffer = []

    base = 0
    next_seq = 0

    def send(self, mode, buffer):
        self.send_buffer.append(packet(buffer))
        if mode == 1:
            self.go_back_n_sender()
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
        return str(pkt.seq) + " " + str(pkt.ack) + " " + pkt.buffer

    # the sender in go_back_n
    def go_back_n_sender(self):
        _thread.start_new_thread(self.go_back_n_send, ())
        _thread.start_new_thread(self.go_back_n_timeout, ())
        _thread.start_new_thread(self.go_back_n_receive, ())
        while True:
            pass

    # thread for sending
    def go_back_n_send(self):
        while True:  # send
            if self.next_seq < self.base + self.windowSize:
                self.send_buffer[self.next_seq].set_seq_ack(self.seq, self.ack)
                self.p.send(self.make_packet(self.send_buffer[self.next_seq]))
                self.seq += 1
                if self.base == self.next_seq:
                    self.timer.start()
                self.next_seq += 1

    # thread for timer
    def go_back_n_timeout(self):
        while True:
            # Timeout
            self.timer.start(3)
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
        while True:
            buffer = self.p.receive()
            self.receive_buffer[buffer[0]] = buffer[4:]
            self.p.send(str(self.seq) + " " + str(buffer[2]))

    def retransmit(self):
        pass

    # Return a timer object
    # Use timer.cancel() to stop the timer
    def timer(self, timeout):
        timer = threading.Timer(timeout, self.retransmit())
        return timer

    def selective_repeat_sender(self):
        pass

    def selective_repeat_receiver(self):
        pass
