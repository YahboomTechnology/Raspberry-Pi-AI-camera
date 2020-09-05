#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        speech recognition
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
from aip import AipSpeech
#You need to fill in your AppID and Appkey
APP_ID='14842746'
API_KEY='0L7ur1I4FvsRo3GC3ONQEt5q'
SECRET_KEY='gD6SIdDGW6bHl0SpVG5wQl1jZ5ymKWCm'
#Initialization
aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
#Read file
def get_file_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()
#Please refer to the technical documentation for the parameters. The format is amr and the language is Chinese.
#The .amr file is the recording file for the moblie device
#The test-case for this program is a Chinese .amr, so you can replace this target file by other language
#Baidu speech api also support .pcm or .wav files
result=aipSpeech.asr(get_file_content('/home/pi/yahboom/speech/8k.amr'),'amr',8000,{
        'lan':'en',
        })
print(result['result'][0])