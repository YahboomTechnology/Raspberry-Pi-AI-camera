#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
    * @file        socket server
    * @version      V1.0
    * @details
    * @par History
    
    @author: longfuSun
"""
import socket
import threading
#Set mode of socket is tcp/ip
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#You can modify the port and ip according to the actual situation
address='192.168.1.66'        #wifi
port =9902
#Bind address and port
s.bind((address,port))
#Set the number of servers allowed to access
s.listen(2)
sock,addr=s.accept()
true=True

#For avoid congestion, write receive into threads
def rec(sock):
    global true
    while true:
        #Set encoding format utf-8
        t=sock.recv(1024).decode('utf8')
        #Exit when the input 'exit'
        if t=='exit':
            true=False
        print('recieve: '+t)
trd=threading.Thread(target=rec,args=(sock,))
trd.start()
while true:
    t=raw_input()
    sock.send(t.encode('utf8'))
    if t=='exit':
        true=False
s.close()
