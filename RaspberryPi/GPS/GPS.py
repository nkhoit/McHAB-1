import serial

class GPS:
    def __init__(self, port = '/dev/ttyAMA0'):
        #Create a serial object that will read the GPS
        self.ser = serial.Serial(port, 4800, timeout=0)

    def readGPS(self):
        gpsList=[]
        while(self.ser.inWaiting()>0):
            data = self.ser.readline()
            gpsList.append(data.rstrip())

        return gpsList


if __name__ == '__main__':
    gps = GPS()
    import time
    initialTime = time.time()*1000

    while True:
        currentTime = time.time()*1000
        if(currentTime-initialTime > 1000):
            data = gps.readGPS()
            print ('\n').join(data)
            initialTime=currentTime

