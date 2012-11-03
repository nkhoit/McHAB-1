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
        x,y,z=LSM.readRawAccel()
        sys.stdout.write('\rX: %d, Y: %d, Z: %d' % (x,y,z))
        sys.stdout.flush()

        '''
        counter+=1
        if(current-initial>1000):
            print 'Sampling Rate: ' + str(counter)
            initial=current
            counter=0
        '''
