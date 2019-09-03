#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        sevo_face_nosocket
    * @version      V1.0
    * @details
    * @par History
    @author: longfuSun
"""

from __future__ import division
import cv2
import Adafruit_PCA9685
import time  
import numpy as np
import threading
#Initialize PCA9685 and servo
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(1,0,500)
pwm.set_pwm(2,0,500)
time.sleep(1)
#Initialize the camera and set the threshold
#If you think the card is serious, please adjust the "1" and "2" two codes
cap = cv2.VideoCapture(0)
#“1”，camera resolution，center poiont is（320，240）

cap.set(cv2.cv.CV_CAP_PROP_FOURCC,cv2.cv.CV_FOURCC('M','J','P','G'))
cap.set(3, 320)
cap.set(4, 240)
#Import classifier
face_cascade = cv2.CascadeClassifier( '123.xml' )
x=0;
thisError_x=0
lastError_x=0
thisError_y=0
lastError_y=0

Y_P = 425
X_P = 425
flag=0
y=0
w=0
h=0
facebool = False

def xx():
    while True:
        CON=0
        if CON==0:
            pwm.set_pwm(1,0,650-X_P+200)
            #pwm.set_pwm(2,0,650-Y_P+200)
            CON+=1
        else:
            pwm.set_pwm(1,0,650-X_P)
            #pwm.set_pwm(2,0,650-Y_P)
    

tid=threading.Thread(target=xx)
tid.setDaemon(True)
tid.start()
    
while True:
    
    ret,frame = cap.read()
    
    #frame=cv2.GaussianBlur(frame,(5,5),0)
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
   
    faces=face_cascade.detectMultiScale(gray)
    max_face=0
    value_x=0
    
    
    if len(faces)>0:
        #print('face found!')
        #temp = (x,y,w,h)
        (x,y,w,h) = faces[0]
        cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
        result=(x,y,w,h)
        x=result[0]+w/2
        y=result[1]+h/2
        facebool = True
        '''
        
        for(x,y,w,h) in faces:
            #找到矩形的中心位置
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            result=(x,y,w,h)
            x=result[0]+w/2
            y=result[1]+h/2
            '''
    
        #“2” error value
        
        
    #while facebool:    
        thisError_x=x-160
        thisError_y=y-120
        #if thisError_x > -20 and thisError_x < 20 and thisError_y > -20 and thisError_y < 20:
        #    facebool = False
        #User can adjust the two values of P and D to detect the effect of changes in two values on the stability of the steering gear
        pwm_x = thisError_x*5+1*(thisError_x-lastError_x)
        pwm_y = thisError_y*5+1*(thisError_y-lastError_y)
        lastError_x = thisError_x
        lastError_y = thisError_y
        XP=pwm_x/100
        YP=pwm_y/100
        X_P=X_P+int(XP)
        Y_P=Y_P+int(YP)
        if X_P>670:
            X_P=650
        if X_P<0:
            X_P=0
        if Y_P>650:
            Y_P=650
        if X_P<0:
            Y_p=0
        
    
    
    #pwm.set_pwm(1,0,650-X_P)
    #pwm.set_pwm(2,0,650-Y_P)

    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break
    
cap.release()
cv2.destroyAllWindows()
