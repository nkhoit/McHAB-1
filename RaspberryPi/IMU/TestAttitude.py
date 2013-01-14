import Attitude

att=Attitude.Attitude()

while(1):
    z,y,x=att.getAttitude()
    print 'x: ' + str(x) + ' y: ' + str(y) + ' z: ' + str(z)
