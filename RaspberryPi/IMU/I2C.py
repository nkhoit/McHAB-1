#!/usr/bin/python
import smbus

class I2C:
    def __init__(self, address, bus=smbus.SMBus(0)):
        self.address=address
        self.bus=bus

    def writeByte(self, reg, value):
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except IOError, err:
            print "Error accessing 0x%02X" % self.address
            return -1

    def readByte(self, reg):
        try:
            return self.bus.read_byte_data(self.address, reg)
        except IOError, err:
            print "Error accessing 0x%02X" % self.address
            return -1


