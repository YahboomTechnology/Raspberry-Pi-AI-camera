#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        speech conpound
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
from aip import AipSpeech
import pygame
import time
from time import perf_counter
import os
#You need to iput your Appid and Appkey
APP_ID='20059657'
API_KEY='AOAFsdeeCwbQrEVDbSGjNjFE'
SECRET_KEY='8NzZdG1AZw8Q0G1mnqgAfh5RLbbTGzZv'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
#Adjust the speech rate, volume, and vocals in the parameters. The girl who feels ‘per’ is 0 is the most natural and clear.
t=perf_counter()
result = aipSpeech.synthesis(text = 'Yahboom technology apply speech API to process speech conpound', 
                             options={'spd':3,'vol':9,'per':1,})
#Write synthesized speech to a file
if not isinstance(result,dict):
    with open('audio.mp3','wb') as f:
        f.write(result)
        
else:print(result)
#We use pygame of Raspberry Pi
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/yahboom/speech/audio.mp3')
pygame.mixer.music.play()
time.sleep(10)
t2=perf_counter()
print(t2-t)