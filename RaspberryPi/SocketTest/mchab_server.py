#!/usr/bin/env python

from Adafruit_MCP4725 import MCP4725
import SocketServer
import sys
import RPi.GPIO as GPIO
from math import fabs
from threading import Thread

HOST=''
PORT=31092
BUFFERSIZE=4096
dac=MCP4725(0x60)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data=float(self.request.recv(4096))
            except:
                pass
            print str(data)
            if(data<0):
                data=-data
                GPIO.output(18,GPIO.HIGH)
            else:
                GPIO.output(18,GPIO.LOW)
            convert=int(fabs(data)*4096/4)
            dac.setVoltage(convert)


class TCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads=True
    allow_reuse_address=True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self,server_address,RequestHandlerClass)

if __name__ == '__main__':
    server=TCPServer((HOST,PORT), TCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
        sys.exit(0)




