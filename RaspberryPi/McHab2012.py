#!/usr/bin/python
import time
import RPi.GPIO as GPIO

#import user libraries
from ImportDirectoryList import * #import all used directories
import Buzzer 
import CutDown

class McHab2012:
	#Constants: To do, change format
	system_start_time = 3000 #3 seconds
	data_read_time = 20 #50 Hz
	buzzer_time = 1000 #1 minutes
	cut_timer = 1000
	cut_time = 10000 #0.5	 minutes 
	buzzer_pin = 23 #GPIO pin 23
	cut_down_pin = 18 #GPIO pin 18
	buzzer_start_time = 1800000 #30 minutes
	altitude_threshold = 500 #500 meters

	def __init__(self):		
		#Timer Variables
		self.current_time = time.time()*1000.0
		self.previous_data_read_time = self.current_time
		self.previous_buzzer_time = self.current_time
		
		#timer offset
		self.cut_time += self.current_time
		self.buzzer_start_time += self.current_time
		self.system_start_time += self.current_time
		
		self.buzzer = Buzzer.Buzzer(self.buzzer_pin, self.current_time, self.buzzer_start_time, self.altitude_threshold) #Create Buzzer Object
		self.CutDown = CutDown.CutDown(self.current_time, self.cut_down_pin, self.cut_time) #Create CutDown Object
		
			
	def loop(self):
		self.current_time = time.time()*1000.0 #Get current time
	
		#start up 
		if(self.current_time < self.system_start_time):
			self.buzzer.beep_delay(self.current_time)
	
		#Main loop for reading data, cut rope and buzzer
		else:
			if(self.current_time - self.previous_data_read_time > self.data_read_time):
				#Run data read subroutine
				self.previous_data_read_time = self.current_time #reset timer
				
			if(self.current_time - self.previous_buzzer_time > self.buzzer_time):
				self.buzzer.loop(self.current_time, 5) #Run buzzer subroutine
				self.previous_buzzer_time = self.current_time #reset timer
				
			if(self.current_time - self.previous_cut_time > self.cut_timer):
				self.CutDown.cut(self.current_time) #Run cut down subroutine
				self.previous_cut_time = self.current_time #reset timer

if __name__ == '__main__':
	mchab = McHab2012()
	
	#Run the loop subroutine indefinitly
	while(1):
		mchab.loop()
		


