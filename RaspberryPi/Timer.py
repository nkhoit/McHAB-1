#!/usr/bin/python
import time

class Timer:
	#Constants: To do, change format

	def __init__(self, delay):
		self.current_time = time.time()*1000.0
		self.previous_time = -1
		self.delay = delay
		
	def start_timer(self):
		self.current_time = time.time()*1000.0
		self.previous_time = self.current_time
	
	def get_flag(self):
		self.current_time = time.time()*1000.0
		
		#If the delay is reached, return 0. Else return 1.
		if(self.current_time - self.previous_time > self.delay):
			self.previous_time = -1
			return 0
		else:
			return -1
			
		

		
		
			

		


