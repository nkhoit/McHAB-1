#!/usr/bin/python

import serial
import struct

COM='/dev/ttyAMA0'
BAUD=115200

ser=serial.Serial(COM,BAUD,timeout=1)

while True:
    line=ser.readline().rstrip()
    if(len(line)==18):
        converted=struct.unpack('hhhhhhhhh', line)
        print str(converted)
