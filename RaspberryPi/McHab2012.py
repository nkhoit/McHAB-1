#!/usr/bin/python
import time
import RPi.GPIO as GPIO

#import user libraries
from ImportDirectoryList import * #import all used directories
import Buzzer 

class McHab2012:
	#Constants: To do, change format
	data_read_time = 20 #50 Hz
	buzzer_time = 60000 #1 minutes
	cut_time = 200 #5 Hz

	#Timer Variables
	current_time = time.time()*1000.0
	previous_data_read_time = 0
	previous_buzzer_time = 0
	previous_cut_time = 0

	def __init__(self):
		#Sensor initialization and codes to be ran before loop
		GPIO.setmode(GPIO.BCM)
			
	def loop(self):
		if(self.current_time - self.previous_data_read_time > self.data_read_time):
			buzzer_loop() #Run data read subroutine
			self.previous_data_read_time = self.current_time #reset timer
		if(self.current_time - self.previous_buzzer_time > self.buzzer_time):
			#Run buzzer subroutine
			self.previous_buzzer_time = self.current_time #reset timer
		if(self.current_cut_time - self.previous_cut_time > self.cut_time):
			#Run cut down subroutine
			self.previous_cut_time = self.curent_time #reset timer

if __name__ == '__main__':
	mchab = McHab2012()
	
	#Initiate sensors and other codes to be ran before loop function
	mchab.initiate()
	
	#Run the loop subroutine indefinitly
	while(1):
		mchab.loop()
		


