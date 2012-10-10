#!/usr/bin/python

import serial
import struct
import os
import math
import sys
import time
import Matrix as m

COM='COM3'
BAUD=115200

F_sample = 100
T_sample = 1.0/F_sample
GYRO_FS = 1000 #16 bit register

Cbi_hat = m.unit_matrix(3)

g_i = m.Matrix([[0],[0],[-1]])

b_d= m.Matrix([[0],[1],[0]])

def change_frame(matrix):
    frame=m.Matrix([[-1,0,0],[0,-1,0],[0,0,-1]])
    return frame*matrix

def normalize(array):
    temp=math.sqrt(array[(0,0)]**2+array[(1,0)]**2+array[(2,0)]**2)
    return m.Matrix([[array[(0,0)]/temp],[array[(1,0)]/temp],[array[(2,0)]/temp]])

def convert_gyro(array):
    x_c=float(array[(0,0)])*GYRO_FS/2**16*math.pi/180
    y_c=float(array[(1,0)])*GYRO_FS/2**16*math.pi/180
    z_c=float(array[(2,0)])*GYRO_FS/2**16*math.pi/180

    #print str(x_c)
    return m.Matrix([[x_c],[y_c],[z_c]])

def cross(array):
    return m.Matrix([[0, -array[(2,0)], array[(1,0)]],
					[array[(2,0)],0,-array[(0,0)]],
					[-array[(1,0)],array[(0,0)],0]])

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

            raw_accel=m.Matrix([[line_u[0]],[line_u[1]],[line_u[2]]])
            norm_accel=normalize(raw_accel)
            #c_accel=change_frame(norm_accel)

            raw_gyro=m.Matrix([[line_u[3]],[line_u[4]],[line_u[5]]])
            omega_measured=convert_gyro(raw_gyro)
            #print str(omega_measured)
            #omega_measured=normalize(raw_gyro)

            raw_magne=m.Matrix([[line_u[6]],[line_u[7]],[line_u[8]]])
            norm_magne=normalize(raw_magne)

            b_b=Cbi_hat*b_d
            g_b=Cbi_hat*g_i

            r=-10*((cross(g_b)*norm_accel) + (cross(b_b)*norm_magne))

            omega_hat = omega_measured+r
            omega_hat_mag = math.sqrt(omega_hat[(0,0)]**2+omega_hat[(1,0)]**2+omega_hat[(2,0)]**2)

            Ak = m.unit_matrix(3) - cross(omega_hat)*math.sin(omega_hat_mag*T_sample)*(1.0/omega_hat_mag) + (1-math.cos(omega_hat_mag*T_sample))*(cross(omega_hat)*cross(omega_hat))*(1.0/omega_hat_mag)**2

            Cbi_hat = Ak*Cbi_hat

            sys.stdout.write(str(Cbi_hat)+'\n')
            sys.stdout.flush()














