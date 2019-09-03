#!/usr/bin/env python2
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
from time import time
#You need to input your APPid and APPkey
APP_ID='14842692'
API_KEY='d06L3VtQCXr0qyL9PWGySGf0'
SECRET_KEY='ScxR7ObkPQ1blfGzZGDGkBe5oobfOlDc'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

t=time()
result = aipSpeech.synthesis(text = 'Yahboom technology apply speech API to process speech conpound', 
                             options={'spd':5,'vol':9,'per':1,})
#Wirte synthesized speech to a file
if not isinstance(result,dict):
    with open('audio.mp3','wb') as f:
        f.write(result)
        
else:print(result)
#We use pygame of Raspberry Pi
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/yahboom/speech/audio.mp3')
pygame.mixer.music.play()
t2=time()
print(t2-t)