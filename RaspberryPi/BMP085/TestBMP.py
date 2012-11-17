#!/usr/bin/python

import BMP085

if __name__ == '__main__':
    bmp = BMP085.BMP085(0x77,2)

    temp=bmp.readTemperature()
    pressure = bmp.readPressure()
    altitude = bmp.readAltitude()

    print "Temperature: %.2f C" % temp
    print "Pressure: %.2f hPa" % (pressure / 100.0)
    print "Altitude: %.2f" % altitude
