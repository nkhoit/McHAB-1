#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from ImportDirectoryList import * #import all used directories

#Constants: To do, change format
data_read_time = 20 #50 Hz
buzzer_time = 60000 #1 minutes
cut_time = 200 #5 Hz

#Timer Variables
current_time = time.time()*1000.0
previous_data_read_time = 0
previous_buzzer_time = 0
previous_cut_time = 0

if __name__ == '__main__':
	#Initiate sensors and other codes to be ran before loop function
	initiate()
	
	#Run the loop subroutine indefinitly
	while(1):
		loop()
		

def initiate():
	#Sensor initialization and codes to be ran before loop
	GPIO.setmode(GPIO.BCM)
		
def loop():
	if(current_time - previous_data_read_time > data_read_time):
		buzzer_loop() #Run data read subroutine
		previous_data_read_time = current_time #reset timer
	if(current_time - previous_buzzer_time > buzzer_time):
		#Run buzzer subroutine
		previous_buzzer_time = current_time #reset timer
	if(current_cut_time - previous_cut_time > cut_time):
		#Run cut down subroutine
		previous_cut_time = curent_time #reset timer


