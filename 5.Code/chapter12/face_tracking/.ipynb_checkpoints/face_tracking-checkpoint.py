#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file         face_tracking
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
from __future__ import division
import cv2
#import Adafruit_PCA9685

import time  

#This is a version without servo

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 320)
#The location of face.xml should be in the same folder as the program.
face_cascade = cv2.CascadeClassifier( '123.xml' ) 
#loop
while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #First,convert each frame into a grayscale image and look it up in the grayscale image.
    faces = face_cascade.detectMultiScale( gray )
    max_face = 0
    value_x = 0
    if len(faces)>0:
        #print('face found!')
        for (x,y,w,h) in faces:
            #The parameters are "target frame", "rectangle", "rectangular size", "line color", "width"
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            #max_face=w*h
            result = (x,y,w,h)
            x=result[0]
            y = result[1]

    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==27:
        break
    
cap.release()
cv2.destroyAllWindows()
