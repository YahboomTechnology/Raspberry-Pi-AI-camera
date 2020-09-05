#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        sevo_ball_nosocket
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
pwm.set_pwm(1,0,320)
pwm.set_pwm(2,0,240)
time.sleep(1)
#Initialize the camera and set the threshold
#If you feel the lag is serious, please adjust the two codes "1" and "2"
cap = cv2.VideoCapture(0)
#"1", the resolution of the camera, the center point is (320, 240)
cap.set(3, 320)
cap.set(4, 240)
yellow_lower=np.array([26,43,46])
yellow_upper=np.array([34,255,255])
#Each degree of freedom requires 4 variables
x=0;
thisError_x=500       #Current error value
lastError_x=100       #last error value
thisError_y=500
lastError_y=100
Y_P=425
X_P = 425           #Rotation angle
flag=0
y=0
def xx(X_P,Y_P):
    pwm.set_pwm(1,0,650-X_P)
    pwm.set_pwm(2,0,650-Y_P)
while True:    
    ret,frame = cap.read()

    frame=cv2.GaussianBlur(frame,(5,5),0)
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    mask=cv2.inRange(hsv,yellow_lower,yellow_upper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    mask=cv2.GaussianBlur(mask,(3,3),0)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    #When the ball is found
    if len(cnts)>0:
        #print('face found!')
        cnt=max(cnts,key=cv2.contourArea)
        (x,y),radius=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2)
        #“2”, error value
        thisError_x=x-160
        thisError_y=y-120
        #PID controlling
        pwm_x = thisError_x*3+1*(thisError_x-lastError_x)
        pwm_y = thisError_y*3+1*(thisError_y-lastError_y)
        #Iterate two error values
        lastError_x = thisError_x
        lastError_y = thisError_y
        #Adafruit_PCA9685
        XP=pwm_x/100
        YP=pwm_y/100
        X_P=X_P+int(XP)
        Y_P=Y_P+int(YP)
        #Keep the steering gear rotation pulse within a safe range
        if X_P>670:
            X_P=650
        if X_P<0:
            X_P=0
        if Y_P>650:
            Y_P=650
        if X_P<0:
            Y_p=0
        print('x',x,X_P);
    tid=threading.Thread(target=xx,args=(X_P,Y_P,))
    tid.setDaemon(True)
    tid.start()

    #pwm.set_pwm(1,0,650-X_P)
    #pwm.set_pwm(2,0,650-Y_P)

    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==27:
        break
    
cap.release()
cv2.destroyAllWindows()
