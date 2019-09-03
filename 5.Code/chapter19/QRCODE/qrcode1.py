#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        qr code
    * @version      V1.0
    * @details
    * @par History
    @author: longfuSun
"""

from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

ap=argparse.ArgumentParser()

ap.add_argument("-o","--output",type=str,default="content.csv",
                help="path to output csv file containing barcode")
args=vars(ap.parse_args())

print('starting video stream....')
#Command of using web camera
vs=VideoStream(src=0).start()
#Command of using Raspberry Pi’s own camera
#vs=VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#Write content to csv
csv=open(args["output"],"w")
found=set()
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
        
        
        
        
        
        
        
