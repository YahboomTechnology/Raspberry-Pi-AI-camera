#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file         face_tracking
    * @version      V1.0
    * @details
    * @par History
    @author: longfuSun
"""

import numpy as np
import cv2

yellow_lower=np.array([26,43,46])
yellow_upper=np.array([34,255,255])
cap=cv2.VideoCapture(0)

cap.set(3,320)
cap.set(4,240)

while 1:
    ret,frame=cap.read()
    frame=cv2.GaussianBlur(frame,(5,5),0)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,yellow_lower,yellow_upper)
    #图像学膨胀腐蚀
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.GaussianBlur(mask,(3,3),0)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    #寻找轮廓并绘制轮廓
    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
   
    if len(cnts)>0:
        #寻找面积最大的轮廓并画出其最小外接圆
        cnt=max(cnts,key=cv2.contourArea)
        (x,y),radius=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2)
        #找到物体的位置坐标
        print(int(x),int(y))
    else:
        pass
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    if cv2.waitKey(5)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
