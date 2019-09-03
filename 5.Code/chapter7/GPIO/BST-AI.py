#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        led—buzzer
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
import RPi.GPIO as GPIO
import time
#Control LED pin is 9，10，11 ，buzzer pin is 16
R,G,B=9,10,11
buzzer=16
GPIO.setmode(GPIO.BCM)

GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
#Make buzzer no sound

GPIO.output(buzzer, False)
time.sleep(2)
GPIO.output(buzzer,True)
# Set work mode of PWM
pwmR = GPIO.PWM(R, 70)
pwmG = GPIO.PWM(G, 70)
pwmB = GPIO.PWM(B, 70)

pwmR.start(0)
pwmG.start(0)  
pwmB.start(0)
#Four modes
try:
	t = 0.01
	while True:
            for i in range(0,71):
                pwmG.ChangeDutyCycle(70)
                pwmB.ChangeDutyCycle(i)
                pwmR.ChangeDutyCycle(70-i)
                print(i)
                time.sleep(t)
            for i in range(70,-1,-1):
                pwmG.ChangeDutyCycle(0)
                pwmB.ChangeDutyCycle(i)
                pwmR.ChangeDutyCycle(70-i)
                print(i-1000)
                time.sleep(t)

        
except KeyboardInterrupt:
	pass
pwmR.stop()
pwmG.stop()
pwmB.stop()
GPIO.cleanup()
		