from Data_Link_Layer import dataLinkLayer
import time

dl = dataLinkLayer(5555, 1)
time.sleep(2)
i = 0
while True:
    dl.send(1, "Hello world%d" % i)
    i += 1
    time.sleep(2)
