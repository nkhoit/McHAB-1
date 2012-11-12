#!/usr/bin/python
import time
import RPi.GPIO as GPIO

#import user libraries
from ImportDirectoryList import * #import all used directories
import Buzzer
import CutDown

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
    altitude_threshold = 500

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

        #Buzzer variables
        self.beep = 0 #0 = idle, 1 = on

        #Initiate Peripherals
        self.buzzer = Buzzer.Buzzer(self.buzzer_pin1, self.buzzer_pin2, self.current_time, self.buzzer_start_time, self.altitude_threshold) #Create Buzzer Object
        self.CutDown = CutDown.CutDown(self.current_time, self.cut_down_pin, self.cut_time) #Create CutDown Object

        #temp variables, remove later
        self.previous_time_temp = 0
        self.count = 0

    def loop(self):
        #get current time
        self.current_time = time.time()*1000.0 - self.initial_time

        #Main loop for reading data, cut rope and buzzer
        if(self.current_time - self.previous_data_read_time > self.data_read_time):
            #Run data read subroutine
            self.previous_data_read_time = self.current_time #reset timer

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
        if(self.current_time - self.previous_cut_time > self.cut_timer):
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



