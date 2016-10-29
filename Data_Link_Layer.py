from Physical_Layer import physicalLayer


class packet:
    seq = 0
    ack = 0
    buffer = ""
    # timer


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

    def send_ack(self, seq):
        self.seq += 1
        ack = seq + 1
        message = str(self.seq) + " " + str(ack)
        return message

    def go_back_n(self):
        base = 0
        next_seq = 0
        ack=0
        while True:
            if next_seq < base + self.windowSize:
                message=self.send_ack()+" "+str(self.send_buffer[])
                self.p.send()


    def selective_repeat(self):
        pass

    def main(self):
        pass
