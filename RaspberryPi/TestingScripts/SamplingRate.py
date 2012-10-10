#!/usr/bin/python

import serial
import time

COM='/dev/ttyAMA0'
BAUD=115200

ser=serial.Serial(COM,BAUD,timeout=1)
counter=0
initial=time.time()*1000.0

while True:
    current=time.time()*1000.0
    ser.readline()
    counter+=1
    if(current-initial>1000):
        print 'Sampling Rate: ' + str(counter)
        initial=current
        counter=0

