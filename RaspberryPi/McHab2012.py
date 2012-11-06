#!/usr/bin/python
import time
import RPi.GPIO as GPIO

#import user libraries
from ImportDirectoryList import * #import all used directories
import Buzzer 
import CutDown

class McHab2012:
	#Constants: To do, change format
	data_read_time = 20 #50 Hz
	buzzer_time = 1000 #1 minutes
	cut_time = 200 #5 Hz
	buzzer_pin = 25 #GPIO pin 25
	cut_down_pin = 0 #GPIO pin 0

	def __init__(self):
		self.buzzer = Buzzer.Buzzer(self.buzzer_pin) #Create Buzzer Object
		self.CutDown = CutDown.CutDown(self.cut_down_pin) #Create CutDown Object
		
		#Timer Variables
		self.current_time = time.time()*1000.0
		self.previous_data_read_time = 0
		self.previous_buzzer_time = 0
		self.previous_cut_time = 0
			
	def loop(self):
		self.current_time = time.time()*1000.0 #Get current time
	
		if(self.current_time - self.previous_data_read_time > self.data_read_time):
			#Run data read subroutine
			self.previous_data_read_time = self.current_time #reset timer
		if(self.current_time - self.previous_buzzer_time > self.buzzer_time):
			self.buzzer.loop(self.current_time, 5) #Run buzzer subroutine
			self.previous_buzzer_time = self.current_time #reset timer
		if(self.current_time - self.previous_cut_time > self.cut_time):
			self.cut(self.current_time) #Run cut down subroutine
			self.previous_cut_time = self.current_time #reset timer

if __name__ == '__main__':
	mchab = McHab2012()
	
	#Run the loop subroutine indefinitly
	while(1):
		mchab.loop()
		


