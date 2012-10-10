#!/usr/bin/python

import serial
import struct
import numpy as np
import os
import math
import _transformations as tf
import sys
import time
import Matrix as m

COM='COM3'
BAUD=115200

F_sample = 100
T_sample = 1.0/F_sample
GYRO_FS = 1000 #16 bit register

Cbi_hat = np.identity(3)

g_i = np.array([0,0,-1])

b_d= np.array([0,1,0])

def change_frame(matrix):
    frame=np.array([-1,0,0],[0,-1,0],[0,0,-1])
    return np.dot(frame,matrix)

def normalize(array):
    temp=math.sqrt(array[0]**2+array[1]**2+array[2]**2)
    return np.array([array[0]/temp,array[1]/temp,array[2]/temp])

def convert_gyro(array):
    x_c=float(array[0])*GYRO_FS/2**16*math.pi/180
    y_c=float(array[1])*GYRO_FS/2**16*math.pi/180
    z_c=float(array[2])*GYRO_FS/2**16*math.pi/180

    #print str(x_c)
    return np.array([x_c,y_c,z_c])

def cross(array):
    return np.array([[0, -array[2], array[1]],[array[2],0,-array[0]],[-array[1],array[0],0]])

if __name__ == '__main__':
    try:
        ser=serial.Serial(COM,BAUD,timeout=1)
    except:
        print 'Could not connect to ' + COM
        exit()

    while(True):
        line=ser.readline().rstrip()
        if(len(line)==18):
            line_u=struct.unpack('hhhhhhhhh', line)
            #print str(line_u)

            raw_accel=np.array([line_u[0],line_u[1],line_u[2]])
            norm_accel=normalize(raw_accel)
            #c_accel=change_frame(norm_accel)

            raw_gyro=np.array([line_u[3],line_u[4],line_u[5]])
            omega_measured=convert_gyro(raw_gyro)
            #print str(omega_measured)
            #omega_measured=normalize(raw_gyro)

            raw_magne=np.array([line_u[6],line_u[7],line_u[8]])
            norm_magne=normalize(raw_magne)

            b_b=np.dot(Cbi_hat,b_d.T)
            g_b=np.dot(Cbi_hat,g_i.T)

            r=-10*(np.dot(cross(g_b),norm_accel.T) + np.dot(cross(b_b),norm_magne.T))

            omega_hat = omega_measured+r
            omega_hat_mag = math.sqrt(omega_hat[0]**2+omega_hat[1]**2+omega_hat[2]**2)

            Ak = np.eye(3) - cross(omega_hat)*math.sin(omega_hat_mag*T_sample)/omega_hat_mag + (1-math.cos(omega_hat_mag*T_sample))*np.dot(cross(omega_hat),cross(omega_hat))/omega_hat_mag**2

            Cbi_hat = np.dot(Ak,Cbi_hat)
            det_Cbi_hat = np.linalg.det(Cbi_hat)

            euler=tf.euler_from_matrix(Cbi_hat, axes='syxz')
            euler=tuple([x*180/math.pi for x in euler])

            sys.stdout.write(str(Cbi_hat)+'\n')
            sys.stdout.flush()














