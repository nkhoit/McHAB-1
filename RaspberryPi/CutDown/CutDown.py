#!/usr/bin/python
import RPi.GPIO as GPIO

class CutDown:
    delay = 10000 #1 minutes

    def __init__(self, current_time, pin_number, cut_down_time):
        self.pin = pin_number #Set cut down GPIO pin
        self.cut_down_time = cut_down_time #Set cut down time
        self.previous_time = current_time #previous time. Used to time the amount of time to set the voltage high
        self.status = 0 #current status of the cut down. 0 = idle 1 = wire is cut

        #Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, GPIO.LOW)

    def cut(self, current_time):
        #if cut down time is reached, set the output to high for a short interval of time. If the line is cut, do not attempt to perform anymore cut.
        if(self.status != 1 and current_time > self.cut_down_time):
            #Start timer and turn on resistor
            if(self.previous_time == 0):
                self.previous_time = current_time
                GPIO.output(self.pin, GPIO.HIGH) #BURN!!!!!!!
                self.previous_time = current_time; #Start timer
                print "cut"

            #Resistor is on for an amount determined by delay and then will be shut off
            elif(current_time - self.previous_time > self.delay):
                GPIO.output(self.pin, GPIO.LOW) #STOP BURNING
                self.status = 1; #Wire is cut
                print "turn off resistor"

