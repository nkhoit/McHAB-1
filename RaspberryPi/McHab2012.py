#!/usr/bin/python
import time
import datetime
import os
import RPi.GPIO as GPIO

#import user libraries
from ImportDirectoryList import * #import all used directories
import Buzzer
import CutDown
import GPS
import BMP085
import LSM303DLM
import L3G4200D

class McHab2012:
    #Constants: To do, change format
    system_start_time = 5000
    data_read_time = 20
    buzzer_time = 1000
    beep_time = 1000
    cut_timer = 1000
    cut_time = 15000
    buzzer_pin1 = 23
    buzzer_pin2 = 22
    cut_down_pin = 18
    buzzer_start_time = 40000
    altitude_threshold = 1000
    imu_time = 40
    gps_time = 2000
    bmp_time = 1000

    #Boundary Cutdown
    NSEW_limits = [46*100+10, 45*100+25, 72*100+20, 73*100+20]

    # cut_down_time = 10000
    # beeper_status = 0 # 0 = idle, 1 = on
    # buzzer_start = 3000
    # buzzer_pin = 23
    # altitude_threshold = 500

    def __init__(self):
        #Get initial time offset
        self.initial_time = time.time()*1000.0
        self.current_time = 0

        #Define timer variables
        self.previous_start_up_time = 0
        self.previous_data_read_time = 0
        self.previous_buzzer_time = 0
        self.previous_cut_time = 0
        self.previous_beep_time = 0

        #Define data read variable
        self.previous_IMU_read = 0
        self.previous_GPS_read = 0
        self.previous_BMP_read = 0

        #Buzzer variables
        self.beep = 0 #0 = idle, 1 = on

        #GPS initial conditions
        self.locked = False
        self.initialPosition = []
        self.boundary_cutdown = False

        #Initiate Peripherals
        self.buzzer = Buzzer.Buzzer(self.buzzer_pin1, self.buzzer_pin2, self.current_time, self.buzzer_start_time, self.altitude_threshold) #Create Buzzer Object
        self.CutDown = CutDown.CutDown(self.current_time, self.cut_down_pin, self.cut_time) #Create CutDown Object
        self.lsm = LSM303DLM.LSM303DLM()
        self.lsm.enableDefault()
        self.l3g = L3G4200D.L3G4200D()
        self.l3g.enableDefault()
        self.bmp = BMP085.BMP085()
        self.gps = GPS.GPS()

        #Create log files
        newpath = './log'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        self.imu_file = open(newpath+"/IMUData.txt","w")
        self.bmp_file = open(newpath+"/BMPData.txt","w")
        self.gps_file = open(newpath+"/GPSData.txt","w")

        #temp variables, remove later
        self.previous_time_temp = 0
        self.count = 0

    def loop(self):
        #get current time
        self.current_time = time.time()*1000.0 - self.initial_time

        #Main loop for reading data, cut rope and buzzer

        #Read IMU at 25Hz
        if(self.current_time - self.previous_IMU_read > self.imu_time):
            accel = self.lsm.readRawAccel()
            mag = self.lsm.readRawMag()
            gyro = self.l3g.readRawGyro()

            self.imu_file.write("ax:%d;ay:%d;az:%d;gx:%d;gy:%d;gz:%d;mx:%d;my:%d;mz:%d\n" %(accel[0],accel[1],accel[2],gyro[0],gyro[1],gyro[2],mag[0],mag[1],mag[2]))

            self.previous_IMU_read = self.current_time

        #Read GPS at 1Hz
        if(self.current_time - self.previous_GPS_read > self.gps_time):
            gps_list = self.gps.readGPS()

            for line in gps_list:
                self.gps_file.write(line+"\n")
                data=line.split(',')
                if(data[0]=='$GPGGA'):
                    if(len(data)==15):
                        coord = [data[2], data[4]]
                        if(data[6]=='1' and self.locked==False):
                            self.initialPosition = coord
                            self.locked = True
                            print "We get signal! We're at: " + str(self.initialPosition)
                        if(self.locked):
                            if( coord[0] > NSEW[0] or coord[0] < NSEW[1] or coord[1] < NSEW[2] or coord[1] > NSEW[3] ):
                                self.boundary_cutdown=True

            self.previous_GPS_read = self.current_time

        #Read BMP at 1Hz
        if(self.current_time - self.previous_BMP_read > self.bmp_time):
            temp=self.bmp.readTemperature()
            pressure=self.bmp.readPressure()
            altitude=self.bmp.readAltitude()

            self.bmp_file.write("temp:%f;p:%f;alt:%f\n" %(temp,pressure,altitude))

            self.previous_BMP_read = self.current_time

        #Print time to the screen every one seconds for debugging
        if(self.current_time - self.previous_time_temp > 1000):
            print self.count
            self.count += 1
            self.previous_time_temp = self.current_time

        #Check at a very low frequency if the platform reached the time threshold and altitude to beep
        if(self.current_time - self.previous_buzzer_time > self.buzzer_time):
            self.beep = self.buzzer.loop(self.current_time, 5) #Run buzzer subroutine
            self.previous_buzzer_time = self.current_time #reset timer

        #Cut down the rope if the timing is reached
        if((self.current_time - self.previous_cut_time > self.cut_timer) or self.boundary_cutdown):
            self.CutDown.cut(self.current_time) #Run cut down subroutine
            self.previous_cut_time = self.current_time #reset timer

        #Beep the buzzer at a fast frequency for start up and landing
        if(self.current_time - self.previous_beep_time > self.beep_time):
            #beep if the platform landed or it just started
            if(self.beep == 1 or self.current_time < self.system_start_time):
                self.buzzer.toggle_beep()
                self.previous_beep_time = self.current_time
            elif(self.beep == 0 and self.current_time > self.system_start_time):
                self.buzzer.turn_off() #TEMP, change to make the buzzer turn off once

if __name__ == '__main__':
    mchab = McHab2012()

    #Run the loop subroutine indefinitly
    while(1):
        mchab.loop()



