#!/usr/bin/env python
# -*- coding: utf-8 -*-


import EasyVR


client = EasyVR.EasyVR("/dev/ttyUSB0")

#client.wakeup()

client.getID()

client.setTimeout(5)

 
while 1==1:
    client.recognizeCommand(2)
    print client.getCommand()
     
