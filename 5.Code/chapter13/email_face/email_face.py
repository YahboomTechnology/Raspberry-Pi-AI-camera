#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file         email_face
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""

from __future__ import division
import cv2

import time  
import signal  
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#--------------------------The above is the control coding method
import smtplib                                  #Import SMTP protocol package
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart  #Create a message body with multiple parts
from email.mime.base import MIMEBase            
from email.mime.image import MIMEImage
import os.path                                  #Analysis path
from email import Encoders

sendDate=0
sender = "xxxxxxxxx@qq.com"                     #Send mailbox
password = "在这里输入刚得到的密钥"
receiver = "xxxxxxxxx@xxx.com"                  
#------------------------------------------
smtp_server = "smtp.qq.com"
smtp_port = 465                                 #SMTP port 465
msg = MIMEMultipart('related')                  



cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 320)
##Comparartor xml location
face_cascade = cv2.CascadeClassifier( '123.xml' ) 

while True:  
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale( gray )
    max_face = 0
    value_x = 0
    font=cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.putText(frame,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),(20,20),font,0.8,(255,255,255),1)
    if len(faces)>0:
        print('face found!')
        currentDate=time.time()
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)#0,255,0
            #max_face=w*h
            result = (x,y,w,h)
            x=result[0]
            y = result[1]
        
        
        if currentDate-sendDate>600:            
            cv2.imwrite("out.png",frame)
            

            img_file = open('out.png',"rb")
            img_data = img_file.read()
            img_file.close()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '0')    
            msg.attach(img)
            msg["From"] = Header("yaboom", "utf-8")
            msg["To"] = Header(receiver, "utf-8")
            msg["Subject"] = Header("face detected", "utf-8")
            #------------------------------------
            message = MIMEText("<p>careful!!!!!</p><p>human approach your device</p><img src='cid:0'/>","html","utf-8")    #plain表示纯文本
            msg.attach(message)
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)                  
            try:
                #qq must use .SMTP_SSL
                #other serverty try:.SMTP
                smtpObject = smtplib.SMTP_SSL(smtp_server , smtp_port)
                smtpObject.login(sender , password)
                #message.as_string()change the MIMEText object into a string
                smtpObject.sendmail(sender , [receiver] , msg.as_string())
                print ("发送成功")
            except smtplib.SMTPException :
                print ("发送失败！")
            smtpObject.quit()                
            sendDate=time.time()    
    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break
    
cap.release()
cv2.destroyAllWindows()
