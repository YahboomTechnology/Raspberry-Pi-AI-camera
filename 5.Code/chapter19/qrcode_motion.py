#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file       qrcode—motion
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
from __future__ import division
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
import Adafruit_PCA9685

#Initialize gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
#Initialize the servo
servo_updown=390
servo_rightleft=390
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(0, 0, servo_rightleft)
pwm.set_pwm(1, 0, servo_updown)
#When the servo exceeds the allowable angle, it will alarm and the buzzer
def warning():
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(16,True)
    time.sleep(1)
    GPIO.output(16,False)
#Water light
def red_yellow_blue():
    for i in range(0,2):
        GPIO.output(9,True)
        time.sleep(0.1)
        GPIO.output(10,True)
        time.sleep(0.1)
        GPIO.output(11,True)
        time.sleep(0.1)
        GPIO.output(10,False)
        time.sleep(0.1)
        GPIO.output(9,False)
        time.sleep(0.1)
        GPIO.output(11,False)
#Steering two degrees of freedom steering
#Use global to control the angle of the steering gear
def right():
    global servo_rightleft
    servo_rightleft-=50
    if servo_rightleft<=170 or servo_rightleft>=570:
        warning()
    else : 
        pwm.set_pwm(1, 0, servo_rightleft)        
def left():
    global servo_rightleft
    servo_rightleft+=50
    if servo_rightleft<=170 or servo_rightleft>=570:
        warning()
    else : 
        pwm.set_pwm(1, 0, servo_rightleft)   
def turn_down():
    global servo_updown
    servo_updown-=50
    if servo_updown<=170 or servo_updown>=570:
        warning()
    else:
        pwm.set_pwm(2,0,servo_updown)
def turn_up():
    global servo_updown
    servo_updown+=50
    if servo_updown<=70 or servo_updown>=570:
        warning()
    else:
        pwm.set_pwm(2,0,servo_updown)

ap=argparse.ArgumentParser()
#Provide a csv file, so that in the end, not only the QR code content can be displayed on the screen, but also a special file for saving
ap.add_argument("-o","--output",type=str,default="content.csv",
                help="path to output csv file containing barcode")
args=vars(ap.parse_args())

print('starting video stream....')
#For web camera
vs=VideoStream(src=0).start()
#Raspberry Pi camera
#vs=VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#Write content to csv
csv=open(args["output"],"w")
found=set()
#Avoid congestion, process multiple times
lastData=''
sendDate=0
while True:
    frame=vs.read()
    frame=imutils.resize(frame,width=400)
    barcodes=pyzbar.decode(frame)
    for barcode in barcodes:
        (x,y,w,h)=barcode.rect
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        barcodeData=barcode.data.decode("utf-8")
        barcodeType=barcode.type
        
        text="{}({})".format(barcodeData,barcodeType)
        
        cv2.putText(frame,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,
                    (0,0,255),2)
        
        newData=barcodeData
        currentDate=time.time()
        #Recognition, every three seconds, and print out incorrect information,
        if (currentDate-sendDate>3):
            print('1')
            if newData=='red_yello_blue light up':
                red_yellow_blue()
                sendDate=time.time()
            elif newData=='right_left servo turn 0':
                left()          #less than 500
            elif newData=='right_left servo turn 180':
                right()
            elif newData=='turn down':
                turn_down()
            elif newData=='turn up':
                turn_up()
            else : print('incorrect data:',newData)
        else:
            continue
 
        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.datetime.now(),barcodeData))
            csv.flush()
            found.add(barcodeData)
    cv2.imshow("found_code",frame)
    key=cv2.waitKey(1)&0xFF
    if key==ord("q"):
        break


csv.close()
cv2.destroyAllWindows()
vs.stop()
        