#!/usr/bin/python
import RPi.GPIO as GPIO
import sys

class Buzzer:
	def __init__(self, pin_number, current_time, start_time, altitude_threshold):
		self.pin = pin_number
		self.start_time = start_time
		self.altitude_threshold = altitude_threshold

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin_number, GPIO.OUT)
		GPIO.output(pin_number, GPIO.LOW)
		
		self.toggle = 0 #Default toggle for delayed beeping. 0 = off, 1 = on
		
	def loop(self, current_time, altitude):
		if(current_time > self.start_time and altitude < self.altitude_threshold):
			return 1
		else:
			return 0
					
	def toggle_beep(self):
		if(self.toggle == 0):
			self.toggle = 1 #set toggle to 1 for next iteration
			GPIO.output(self.pin, GPIO.LOW)
			print "LOW"
		else:
			self.toggle = 0 #set toggle to 0 for next iteration
			GPIO.output(self.pin, GPIO.HIGH)
			print "HIGH"			
