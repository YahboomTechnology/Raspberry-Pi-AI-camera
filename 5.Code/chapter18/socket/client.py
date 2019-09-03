#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        socket_client
    * @version      V1.0
    * @details
    * @par History
    @author: longfuSun
"""

import socket
import threading

#Set mode of socket is tcp/ip
#You can modify the port according to the actual situation
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.1.109',9999))                    #wifi
true=True

def rec(s):
    global true
    while true:
        t=s.recv(1024).decode('utf8')
        if t=='exit':
            true=False
        print('client recieved: '+t)
trd=threading.Thread(target=rec,args=(s,))

trd.start()
while true:
    
    t=raw_input()
    #send
    s.send("client said: "+t.encode('utf8'))
    if t=='exit':
        true=False
s.close()
