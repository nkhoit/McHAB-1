#!/usr/bin/python
import LSM303DLM as lsm
import time
import sys
import string

counter=0
initial=time.time()*1000.0

if __name__ == '__main__':
    LSM = lsm.LSM303DLM()
    LSM.enableDefault()

    while(1):
        current=time.time()*1000.0
        a_x,a_y,a_z=LSM.readRawAccel()
        b_x,b_y,b_z=LSM.readRawMag()
        #print 'Accel = X: %d, Y: %d, Z: %d' % (a_x,a_y,a_z)
        print 'Mag   = X: %d, Y: %d, Z: %d' % (b_x,b_y,b_z)


        '''
        counter+=1
        if(current-initial>1000):
            print 'Sampling Rate: ' + str(counter)
            initial=current
            counter=0
        '''
