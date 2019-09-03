"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        photo
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
import cv2
from PIL import Image
import sys

# Mask position
imagePath = sys.argv[1]
maskPath = "mask.png"
# Classifier
cascPath = "face.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(gray, 1.15)
background = Image.open(imagePath)

# Put the mask on the face
for (x,y,w,h) in faces:
	cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)
	cv2.imshow('face detected', image)
	cv2.waitKey(0)
	# open mask as PIL image
	mask = Image.open(maskPath)
	# resize mask according to detected face
	mask = mask.resize((w,h), Image.ANTIALIAS)
	# define offset for mask
	offset = (x,y)
	# paste mask on background
	background.paste(mask, offset, mask=mask)

# paste final thug life meme
background.save('out.png')
