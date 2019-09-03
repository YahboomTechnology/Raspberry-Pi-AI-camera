#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file         gpio
    * @version      V1.0
    * @details
    * @par History
    @author: longfuSun
"""


import RPi.GPIO as GPIO

import time
#Set work mode to BCM
GPIO.setmode(GPIO.BCM)
#Set pins we will use
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
#run 10 times
for i in range(0,10):
    GPIO.output(20,True)
    time.sleep(0.5)
    GPIO.output(20,False)
    GPIO.output(21,True)
    time.sleep(0.5)
    GPIO.output(21,False)
GPIO.cleanup()

