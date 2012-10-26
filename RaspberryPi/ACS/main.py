#!/usr/bin/python

import serial
import struct
import numpy as np
import os
import math
import _transformations as tf
import sys
import time
import Adafruit_MCP4725 as MCP4725
import RPi.GPIO as GPIO

COM='/dev/ttyAMA0'
BAUD=115200

DAC_MAX = 4095
F_sample = 50
T_sample = 1.0/F_sample
GYRO_FS = 1000 #16 bit register
drift=np.array([-88, 20, 5])

Cbi_hat = np.identity(3)
g_i = np.array([0,0,-1])
b_d = np.array([-0.52031361 , 0.56860619 , 0.6371505 ])
C_d = np.identity(3)

counter=0
initial=time.time()*1000.0

def change_frame(matrix):
    frame=np.array([-1,0,0],[0,-1,0],[0,0,-1])
    return np.dot(frame,matrix)

def normalize(array):
    temp=math.sqrt(array[0]**2+array[1]**2+array[2]**2)
    return np.array([array[0]/temp,array[1]/temp,array[2]/temp])

def convert_gyro(array):
    conv = lambda x: (-float(x)/(2**15))*GYRO_FS*math.pi/180.0

    return np.array([conv(array[0]),conv(array[1]),conv(array[2])])

def cross(array):
    return np.array([[0, -array[2], array[1]],[array[2],0,-array[0]],[-array[1],array[0],0]])

def parseData(line_u):
    raw_accel=np.array([-line_u[0],-line_u[1],-line_u[2]])
    norm_accel=normalize(raw_accel)

    raw_gyro=np.array([line_u[3],line_u[4],line_u[5]])-drift
    omega_measured=convert_gyro(raw_gyro)

    raw_magne=np.array([line_u[6],line_u[7],line_u[8]])
    norm_magne=normalize(raw_magne)
    norm_magne=np.array([-norm_magne[0],-norm_magne[1],norm_magne[2]])

    return norm_accel, omega_measured, norm_magne

def setSpeed(dac,speed):
    if(speed<0):
        GPIO.output(22, GPIO.LOW)
        speed=-speed
    else:
        GPIO.output(22, GPIO.HIGH)

    dac.setVoltage(int(speed*DAC_MAX/5.0))


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)

    dac = MCP4725.MCP4725(0x60)

    firstRun = True

    try:
        ser=serial.Serial(COM,BAUD,timeout=1)
    except:
        print 'Could not connect to ' + COM
        exit()

    while(True):
        line=ser.readline().rstrip()
        if(len(line)==18):
            line_u=struct.unpack('hhhhhhhhh', line)
            norm_accel,omega_measured,norm_magne = parseData(line_u)
            #print omega_measured

            if(firstRun):
                b_d=np.array([norm_magne[0],norm_magne[1],norm_magne[2]])
                firstRun=False

            b_b=np.dot(Cbi_hat,b_d.T)
            g_b=np.dot(Cbi_hat,g_i.T)

            r=-10*(np.dot(cross(g_b),norm_accel.T) + np.dot(cross(b_b),norm_magne.T))

            omega_hat = omega_measured+r
            omega_hat_mag = math.sqrt(omega_hat[0]**2+omega_hat[1]**2+omega_hat[2]**2)
            omega_hat_mag_r = 1.0/omega_hat_mag

            Ak = np.eye(3) - cross(omega_hat)*math.sin(omega_hat_mag*T_sample)*omega_hat_mag_r + (1-math.cos(omega_hat_mag*T_sample))*np.dot(cross(omega_hat),cross(omega_hat))*omega_hat_mag_r**2

            Cbi_hat_new = np.dot(Ak,Cbi_hat)

            euler=tf.euler_from_matrix(Cbi_hat_new, axes='szyx')
            euler=tuple([x*180/math.pi for x in euler])

            #setSpeed(dac,euler[0]*5.0/180.0)
            #sys.stdout.write(str(euler)+'\r')
            #sys.stdout.flush()
            #print str(Cbi_hat)

            b_body_d = np.dot(C_d,b_d.T)
            g_body_d = np.dot(C_d,g_i.T)

            u_p = -0.05*(np.dot(cross(g_body_d),g_b.T) + np.dot(cross(b_body_d),b_b.T))
            u_d = -0.05*omega_measured[2]

            u_p = np.dot(np.dot(u_p,Cbi_hat),np.array([0,0,1]).T)

            tau = u_d + u_p
            print str(1000*tau)

            Cbi_hat = Cbi_hat_new

            current=time.time()*1000.0
            counter+=1
            if(current-initial>1000):
                #print 'Sampling Rate: ' + str(counter)
                initial=current
                counter=0


