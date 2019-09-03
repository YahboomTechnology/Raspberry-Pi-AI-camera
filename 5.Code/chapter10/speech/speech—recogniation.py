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
#这里需要填你自己的id和密钥
APP_ID='xxxxxx'
API_KEY='xxxxxx'
SECRET_KEY='xxxxxxx'
#初始化
aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
#读文件
def get_file_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()
#参数请查阅技术文档，格式是amr，语言是中文
result=aipSpeech.asr(get_file_content('/home/pi/yahboom/speech/8k.amr'),'amr',8000,{
        'lan':'zh',
        })
print(result['result'][0])