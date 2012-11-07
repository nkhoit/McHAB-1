#!/usr/bin/python
import RPi.GPIO as GPIO
sys.path.append("../")
import Timer

class Buzzer:
	def __init__(self, pin_number, start_time, beeping_delay, altitude_threshold):
		self.pin = pin_number
		self.start_time = start_time
		self.altitude_threshold = altitude_threshold
		self.timer_start = Timer.Timer(start_time)
		self.timer_delay = Timer.Timer(beeping_delay)

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin_number, GPIO.OUT)
		GPIO.output(pin_number, GPIO.LOW)
		
		self.toggle = 0 #Default toggle for delayed beeping. 0 = off, 1 = on
		
		#Start timer_start
		self.timer_start.start_timer()
		
	def loop(self, altitude):
		if(self.timer_start.get_flag == 0 && altitude < self.altitude_threshold):
			self.beep_delay()
					
	def beep_delay(self):
		#Delay the beep for the self.delay amount
		if(self.timer_delay.previous_time == -1):
			self.timer_delay.start_timer()
		
		elif(self.timer_delay.get_flag == 0):
			if(self.toggle == 0):
				self.toggle = 1 #set toggle to 1 for next iteration
				GPIO.output(self.pin, GPIO.LOW)
				print "LOW"
			else:
				self.toggle = 0 #set toggle to 0 for next iteration
				GPIO.output(self.pin, GPIO.HIGH)
				print "HIGH"			
