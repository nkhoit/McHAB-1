import socket
import pygame
import time

ADDR = ('142.157.144.158',31092)

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized Joystick : %s' % j.get_name()

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ADDR))
while True:
    pygame.event.pump()

    axis_val=j.get_axis(0)
    if ((axis_val > 0.05) or (axis_val < -0.05)):
        print 'Axis %i reads %.2f' % (i, axis_val)
        client.send(str(axis_val)+'\n')

    for i in range(0, j.get_numbuttons()):
        if j.get_button(i) != 0:
            print 'Button %i reads %i' % (i, j.get_button(i))

    time.sleep(.01)

client.close()
