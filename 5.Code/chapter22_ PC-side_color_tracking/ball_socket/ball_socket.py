from __future__ import division
import cv2
import time 
import numpy as np
import socket

addr = ('192.168.1.66',7783)#Target host IP
#readdr = ('192.168.1.110',7780)#Host IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
yellow_lower=np.array([9,135,231])
yellow_upper=np.array([31,255,255])

x=0;

while 1:  
    ret,frame = cap.read()
    frame=cv2.GaussianBlur(frame,(5,5),0)
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,yellow_lower,yellow_upper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    mask=cv2.GaussianBlur(mask,(3,3),0)   
    res=cv2.bitwise_and(frame,frame,mask=mask)
    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)[-2]   
    if len(cnts)>0:
        cnt=max(cnts,key=cv2.contourArea)
        (x,y),radius=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2)
        #[Data, the (x, y) two values are combined and converted into a string type
        # the socket does not send a string string, but a binary code formed after utf-8 encoding.
        print('x',x);
        data =str(x)+','+str(y)
        s.sendto(data.encode("utf-8"),addr)
    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break     
cap.release()
cv2.destroyAllWindows()
s.close()
