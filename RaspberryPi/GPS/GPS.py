import serial

class GPS:
    def __init__(self):
        #Create a serial object that will read the GPS
        self.ser = serial.Serial('COM8', 4800, timeout=0)
        self.ser.readline()

        self.partial_string = ''

    def readGPS(self):
        raw_string = self.partial_string
        for data in self.ser.read(4096):
            raw_string+=data

        parsed_list = raw_string.split('\r\n')
        for data in parsed_list:
            if(data != ''):
                if(data[-1] != '\r'):
                    self.partial_string = data

        parsed_list = [x.rstrip() for x in parsed_list]

        return parsed_list

if __name__ == '__main__':
    gps = GPS()
    import time
    initialTime = time.time()*1000

    while True:
        currentTime = time.time()*1000
        if(currentTime-initialTime > 1000):
            data = gps.readGPS()
            for line in data:
                if(line.split(',')[0] == '$GPGGA'):
                    print line
            initialTime=currentTime

