#!/usr/bin/python
import RPi.GPIO as GPIO
import sys

class Buzzer:
    def __init__(self, pin_number1, pin_number2, current_time, start_time, altitude_threshold):
        self.pin1 = pin_number1
        self.pin2 = pin_number2
        self.start_time = start_time
        self.altitude_threshold = altitude_threshold

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(pin_number1, GPIO.OUT)
        GPIO.output(pin_number1, GPIO.LOW)

        GPIO.setup(pin_number2, GPIO.OUT)
        GPIO.output(pin_number2, GPIO.LOW)

        self.toggle = 0 #Default toggle for delayed beeping. 0 = off, 1 = on

    def loop(self, current_time, altitude):
        if(current_time > self.start_time and altitude < self.altitude_threshold):
            return 1
        else:
            return 0
            
    def turn_on(self):
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.HIGH)
    
    def turn_off(self):
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.LOW)            

    def toggle_beep(self):
        if(self.toggle == 0):
            self.toggle = 1 #set toggle to 1 for next iteration
            self.turn_off()
            print "LOW"
        else:
            self.toggle = 0 #set toggle to 0 for next iteration
            self.turn_on()
            print "HIGH"
            
    
