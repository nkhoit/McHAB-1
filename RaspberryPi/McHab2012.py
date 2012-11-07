#!/usr/bin/python
import time
import RPi.GPIO as GPIO

#import user libraries
from ImportDirectoryList import * #import all used directories
import Buzzer 
#import CutDown

class McHab2012:
	#Constants: To do, change format
	system_start_time = 3000 #3 seconds
	data_read_time = 20 #50 Hz
	buzzer_time = 1000 #1 minutes
	beep_time = 1000 
	cut_timer = 1000
	cut_time = 10000 #0.5	 minutes 
	buzzer_pin = 23 #GPIO pin 23
	cut_down_pin = 18 #GPIO pin 18
	buzzer_start_time = 3000 #30 minutes
	altitude_threshold = 500 #500 meters
	
	# cut_down_time = 10000
	# beeper_status = 0 # 0 = idle, 1 = on
	# buzzer_start = 3000
	# buzzer_pin = 23
	# altitude_threshold = 500 

	def __init__(self):		
		#self.timer_system_start = Timer.Timer(3000)
		#self.timer_buzzer_poll = Timer.Timer(1000)
		#self.timer_beeper = Timer.Timer(1000)
		#self.timer_cut_poll = Timer.Timer(1000)
	
		#start timer
		#self.timer_buzzer_poll.start_timer()
	
		#Initiate peripherals
		#self.buzzer = Buzzer.Buzzer(self.buzzer_pin, self.buzzer_start, self.buzzer_start, self.altitude_threshold) #Create Buzzer Object
		

		
		#self.CutDown = CutDown.CutDown(self.cut_down_pin, self.cut_down_time) #Create CutDown Object	
	
		#Set current to 0
		self.initial_time = time.time()*1000.0
		self.current_time = 0
		
		#Define timer variables
		self.previous_data_read_time = 0
		self.previous_buzzer_time = 0
		self.previous_cut_time = 0
		self.previous_beep_time = 0
		
		#Buzzer variables
		self.beep = 0 #0 = idle, 1 = on
		
		self.buzzer = Buzzer.Buzzer(self.buzzer_pin, self.current_time, self.buzzer_start_time, self.altitude_threshold) #Create Buzzer Object
		#self.CutDown = CutDown.CutDown(self.current_time, self.cut_down_pin, self.cut_time) #Create CutDown Object
		
			
	def loop(self):
		#get current time
		self.current_time = time.time()*1000.0 - self.initial_time
		
		#Buzzer 
		# if(self.timer_buzzer_poll.get_flag() == 0):
			# self.beeper_status = self.buzzer.loop(5) #Run buzzer subroutine	
			# self.timer_buzzer_poll.start_timer()
			
			#start beep timer if beeper status is on
			# if(self.beeper_status == 1):
				# self.timer_beeper.start_timer()
		
		#Beeping
		# if(self.beeper_status == 1 and self.timer_beeper.get_flag() == 0):
			# self.buzzer.toggle_beep()
			# self.timer_beeper.start_timer()
	
		# self.current_time = time.time()*1000.0 #Get current time
	
		#start up 
		# if(self.current_time < self.system_start_time):
			# self.buzzer.beep_delay(self.current_time)
	
		#Main loop for reading data, cut rope and buzzer
		# else:
			# if(self.current_time - self.previous_data_read_time > self.data_read_time):
				#Run data read subroutine
				# self.previous_data_read_time = self.current_time #reset timer
				
		if(self.current_time - self.previous_buzzer_time > self.buzzer_time):
			self.beep = self.buzzer.loop(self.current_time, 5) #Run buzzer subroutine
			self.previous_buzzer_time = self.current_time #reset timer
			print self.beep
			
		if(self.beep == 1 and self.current_time - self.previous_beep_time > self.beep_time):
			self.buzzer.toggle_beep()
			self.previous_beep_time = self.current_time
			
			# if(self.current_time - self.previous_cut_time > self.cut_timer):
				# self.CutDown.cut(self.current_time) #Run cut down subroutine
				# self.previous_cut_time = self.current_time #reset timer

if __name__ == '__main__':
	mchab = McHab2012()
	
	#Run the loop subroutine indefinitly
	while(1):
		mchab.loop()
		


