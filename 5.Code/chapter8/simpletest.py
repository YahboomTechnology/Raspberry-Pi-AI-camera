# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
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


pwm.set_pwm_freq(60)
#UP DOWN 150 390 620  1
# RIGHT LEFT 120 390 620  2

print('Moving servo on channel 0, press Ctrl-C to quit...')

pwm.set_pwm(1,0,200)
time.sleep(0.2)
pwm.set_pwm(2, 0,200)
time.sleep(0.2)
    
pwm.set_pwm(1,0,500)
time.sleep(0.2)
pwm.set_pwm(2, 0,390)
time.sleep(0.2)


'''
updownpulse=500
while True:
    s=input("input: ")
    print(s)
    global updownpulse
    if s==123:
        updownpulse+=5
        pwm.set_pwm(2,0,updownpulse)
    elif s==321:
        updownpulse-=5
        pwm.set_pwm(2,0,updownpulse)
'''        

    
