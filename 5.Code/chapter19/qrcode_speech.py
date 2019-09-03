#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file       qrcode—speech
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
from aip import AipSpeech
import pygame
import threading


#Initizlize baidu speech
APP_ID='14842692'
API_KEY='d06L3VtQCXr0qyL9PWGySGf0'
SECRET_KEY='ScxR7ObkPQ1blfGzZGDGkBe5oobfOlDc'
#APP_ID='xxxxx'
#API_KEY='xxxxx'
#SECRET_KEY='xxxxx'
aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

#Initizlize gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
#Initizlize servo
servo_updown=500
servo_rightleft=390
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(0, 0, servo_rightleft)
pwm.set_pwm(1, 0, servo_updown)

#When the servo is over the allowable angle, buzzer will alarm
def warning():
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(16,True)
    time.sleep(1)
    GPIO.output(16,False)
    
def motion_speech(content):
    text=content
    result = aipSpeech.synthesis(text = text, 
                             options={'spd':5,'vol':9,'per':0,})
    if not isinstance(result,dict):
        with open('audio.mp3','wb') as f:
            f.write(result)  
    else:print(result)
    #Use Raspberry Pi own pygame
    pygame.mixer.init()
    pygame.mixer.music.load('/home/pi/Adafruit_Python_PCA9685/audio.mp3')
    pygame.mixer.music.play()
    
#Water lights    
def red_yellow_blue():
    content='红绿蓝小灯'
    motion_speech(content)
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
#Two degrees of freedom steering of the servo

def right():
    content='伺服电机右转'
    motion_speech(content)
    global servo_rightleft
    servo_rightleft-=50
    if servo_rightleft<=170 or servo_rightleft>=570:
        warning()
    else : 
        pwm.set_pwm(1, 0, servo_rightleft)        
def left(): 
    content='伺服电机左转'
    motion_speech(content)
    global servo_rightleft
    servo_rightleft+=50
    if servo_rightleft<=170 or servo_rightleft>=570:
        warning()
    else : 
        pwm.set_pwm(1, 0, servo_rightleft)   
def turn_down():
    content='伺服电机向下'
    motion_speech(content)
    global servo_updown
    servo_updown-=50
    if servo_updown<=170 or servo_updown>=570:
        warning()
    else:
        pwm.set_pwm(2,0,servo_updown)
def turn_up():
    content='伺服电机向上'
    motion_speech(content)
    global servo_updown
    servo_updown+=50
    if servo_updown<=170 or servo_updown>=570:
        warning()
    else:
        pwm.set_pwm(2,0,servo_updown)

ap=argparse.ArgumentParser()
#Provide a csv file,the QR code content be displayed on the screen,a special file to save.
ap.add_argument("-o","--output",type=str,default="content.csv",
                help="path to output csv file containing barcode")
args=vars(ap.parse_args())

print('starting video stream....')
#Command of using web camera
vs=VideoStream(src=0).start()
#Command of using Raspberry Pi’s own camera：
#vs=VideoStream(usePiCamera=True).start()
time.sleep(2.0)
#Write content into csv
csv=open(args["output"],"w")
found=set()
#Avoid conngestion,multiple treatments
lastData=''
sendDate=0
while True:
    frame=vs.read()
    frame=imutils.resize(frame,width=400)
    barcodes=pyzbar.decode(frame)
    for barcode in barcodes:
        (x,y,w,h)=barcode.rect
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        #Decode the content of the QRcode,enter the time,content and type
        barcodeData=barcode.data.decode("utf-8")
        barcodeType=barcode.type
        
        text="{}({})".format(barcodeData,barcodeType)
        
        cv2.putText(frame,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,
                    (0,0,255),2)
        
        newData=barcodeData
        currentDate=time.time()
        #Identify every three seconds, print out the incorrect information,
        #If you want to add a new QR code, add a judgment.
        if (currentDate-sendDate>4):
            print('1')
            if newData=='red_yello_blue light up':
                tid=threading.Thread(target=red_yellow_blue)
                tid.setDaemon(True)
                tid.start()
                sendDate=time.time() 
            elif newData=='right_left servo turn 0':
                tid=threading.Thread(target=left)         #less than 500
                tid.setDaemon(True)
                tid.start()
                sendDate=time.time()
            elif newData=='right_left servo turn 180':
                tid=threading.Thread(target=right)
                tid.setDaemon(True)
                tid.start()
                sendDate=time.time()
            elif newData=='turn down':
                tid=threading.Thread(target=turn_down)
                tid.setDaemon(True)
                tid.start()
                sendDate=time.time()
            elif newData=='turn up':
                tid=threading.Thread(target=turn_up)
                tid.setDaemon(True)
                tid.start()
                sendDate=time.time()
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
