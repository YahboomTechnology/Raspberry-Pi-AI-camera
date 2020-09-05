#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 02:40:07 2019

@author: pi
"""

from __future__ import division
import time
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()


#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm.set_pwm(channel,0,int(angle))

pwm.set_pwm_freq(50)

set_servo_angle(1,0)
time.sleep(0.8)
set_servo_angle(1,270)
time.sleep(0.8)
set_servo_angle(1,0)

#UP DOWN 150 390 620  1
# RIGHT LEFT 120 390 620  2

print('Moving servo on channel 0, press Ctrl-C to quit...')

