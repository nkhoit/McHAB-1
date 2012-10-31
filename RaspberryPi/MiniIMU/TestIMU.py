#!/usr/bin/python
import LSM303 as lsm
import time
import sys

counter=0
initial=time.time()*1000.0

if __name__ == '__main__':
    LSM = lsm.LSM303()
    LSM.enableDefault()

    while(1):
        current=time.time()*1000.0
        x,y,z=LSM.readAccel()
        sys.stdout.write('\rX: %d, Y: %d, Z: %d' % (x,y,z))
        sys.stdout.flush()

        '''
        counter+=1
        if(current-initial>1000):
            print 'Sampling Rate: ' + str(counter)
            initial=current
            counter=0
        '''
