from Physical_Layer import physicalLayer


class dataLinkLayer:
    p = physicalLayer()
    seq = 0
    ack = 0
    windowSize = 5
    buffer = ""

    def send(self, buffer):
        self.buffer = buffer

    def receive(self):
        pass
        self.p.send(self.seq, self.ack)
        return self.buffer
