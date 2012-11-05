#!/usr/bin/python
import RPi.GPIO as GPIO

class Buzzer:
	start_time = 1800000 #30 minutes
	altitude_threshold = 500 #500 meters

	def __init__(self, pin_number):
		GPIO.setup(pin_number, GPIO.OUT)
		
	def buzzer_loop(self, current_time, altitude):
		#if(not (current_time < start_time) && altitude < altitude_threshold):
			GPIO.output(pin_number, GPIO.HIGH)


