#!/usr/bin/python
import LSM303DLM as lsm
import L3G4200D as l3g
import time
import sys
import string

counter=0
initial=time.time()*1000.0

if __name__ == '__main__':
    LSM = lsm.LSM303DLM()
    L3G = l3g.L3G4200D()
    LSM.enableDefault()
    L3G.enableDefault()

    while(1):
        current=time.time()*1000.0
        a_x,a_y,a_z=LSM.readRawAccel()
        b_x,b_y,b_z=LSM.readRawMag()
        g_x,g_y,g_z=L3G.readRawGyro()
        #print 'Accel = X: %d, Y: %d, Z: %d' % (a_x,a_y,a_z)
        #print 'Mag   = X: %d, Y: %d, Z: %d' % (b_x,b_y,b_z)
        print 'Gyro   = X: %d, Y: %d, Z: %d' % (g_x,g_y,g_z)

