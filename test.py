#!/usr/bin/env python
# -*- coding: utf-8 -*-


import EasyVR



client = EasyVR.EasyVR("/dev/ttyUSB0")

#client.wakeup()

# For init purposes
client.getID()


#Set timeout to listen a command
client.setTimeout(5)

 
while 1==1:
#recognize commands in group 1
    client.recognizeCommand(1)
#Get number of recognized command in group 
    print client.getCommand()
     
