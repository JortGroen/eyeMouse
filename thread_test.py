#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 17:09:56 2020

@author: djoghurt
"""

import threading
import time

import cv2 as cv
import numpy as np

def pizza():
    for i in range(10):
        x = 0
        for j in range(10000000):
            x = x+j
        print("pizza")
    return

def patat():
    for i in range(10):
        x = 0
        for j in range(10000000):
            x = x+j
        print("patat")
    return

def show_colour(name):
    print("starting", name)
    #name = "1"
    colour = (255,0,0)
    
    screenSize = (20, 10)
    screen = np.zeros([screenSize[1],screenSize[0],3],dtype=np.uint8)
    screen.fill(255)
    
    i=0
    while(True):
        
        cv.imshow(name, screen)
        
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     cv.destroyAllWindows()
        #     break
        
    return

# pizza()
# patat()
# thread1 = threading.Thread(target=pizza, name="pizza")
# thread2 = threading.Thread(target=patat, name="patat")
# thread1.start()
# thread2.start()


# thread1 = threading.Thread(target=show_colour("1"), name="1")
thread1 = threading.Thread(target=pizza, name="1")
thread1.daemon = True


#thread2 = threading.Thread(target=show_colour("2"), name="2")
thread2 = threading.Thread(target=patat, name="2")
thread2.daemon = True

thread3 = threading.Thread(target=show_colour, args=("3",), name="3")
thread3.deamon = True

thread1.start()
thread3.start()
thread2.start()
#thread3.start()

i = 0
while(True):
    # print(i)
    # i = i+1
    
    if not thread1.isAlive():
        break
    
    