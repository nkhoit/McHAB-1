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

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            data=self.request.recv(4096)
            convert=int(fabs(float(data))*4096)
            dac.setVoltage(convert)
            print data,


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




