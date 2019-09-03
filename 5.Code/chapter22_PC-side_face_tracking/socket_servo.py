#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        socket_servoMotor
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
from __future__ import division
import Adafruit_PCA9685
import time  
import socket

address = ('192.168.1.66',7783)#本主机IP

#Complete the standard socket connection，binding,monitoring,to the raspberry
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)
#Initialize servo
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(1,0,400)
pwm.set_pwm(0,0,500)
time.sleep(1)
#Initialize PID
x=0
y=0
thisError_x=0
lastError_x=0
thisError_y=0
lastError_y=0
X_P=425
Y_P=425
flag=0
y=0

while 1:
    #Socket “recevie" immediately after entering the servo
    data,addr=s.recvfrom(2048)
    if not data:
        break
    #print("got data from",addr)
    #socket communication data needs to be decoded first.
    x=data.decode()
    print(x)
    #The value sent are x and y,and in the actual "," is used as the flag.
    strX=str(x)
    arr=strX.split(',')
    #String type directly into int will report an error, so first convert to float type
    intX=int(float(arr[0]))
    intY=int(float(arr[1]))
    print('x:',intX,'y:',intY)
    
    ############
    thisError_x=intX-320
    thisError_y=intY-240
    pwm_x=thisError_x*6+1*(thisError_x-lastError_x)
    pwm_y=thisError_y*6+1*(thisError_y-lastError_y)
    
    lastError_x=thisError_x
    lastError_y=thisError_y
    XP=pwm_x/100
    YP=pwm_y/100
    X_P=X_P+int(XP)
    Y_P=Y_P+int(YP)
    if X_P>670:
        X_P=650
    if X_P<0:
        X_P=0
    if Y_P>670:
        Y_P=650
    if Y_P<50:
        Y_P=0
    ###########
    print('**',X_P,Y_P)
    pwm.set_pwm(1,0,650-X_P)
    pwm.set_pwm(2,0,800-Y_P)
    

    time.sleep(0.02)
s.close()

