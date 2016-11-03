from Data_Link_Layer import dataLinkLayer
import  time

dl=dataLinkLayer(5555,1)
time.sleep(2)
dl.send(1,"Hello world")