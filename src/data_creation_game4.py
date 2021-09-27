#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:00:24 2020

@author: djoghurt
"""

import cv2
import numpy as np
import dlib
from math import hypot
import pyautogui
import random
import subprocess
import json
import threading
import time
import os

receiveBuffer = ""
receiveStatus = 0
DATA = ""
stopReader = False

class screenShape:
    width = 0
    height = 0

def create_dot(screen, screenSize):
    screen.fill(255)
    x = random.randint(1, screenSize.width)
    y = random.randint(1, screenSize.height)
    cv2.circle(screen, (x,y), 10, (0,0,255), -1)
    return (x,y)
    
def dotGreen(screen, targetLoc):
    #print("dotGreen")
    screen.fill(255)
    cv2.circle(screen, targetLoc, 10, (0,255,0), -1)
    
def save_data():
    pass


def game_init(screenSize, fullScreen=True):
    screen = np.zeros([screenSize.height,screenSize.width,3],dtype=np.uint8)
    screen.fill(255)
    targetLoc = (int(screenSize.width/2),int(screenSize.height/2))
    cv2.circle(screen, targetLoc, 10, (0,0,255), -1)
    if fullScreen==True:
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    return screen, screenSize, targetLoc

def dataReceiver(process):
    global receiveBuffer, receiveStatus, DATA, stopReader
    
    newData = False
    while(stopReader==False and process.poll()==None):
        
        outputRaw = process.stdout.readline()
        output = str(outputRaw.strip())[2:-1]
        
        index = output.find("<data>")
        if index > -1:
            #print("start!")
            receiveBuffer = ""
            output = output[index+6:]
            if receiveStatus==1:
                print("WARNING: I received a data start key without finishing my previous data read, data might be corrupted!")
            receiveStatus = 1
            
        index = output.find("</data>")    
        if index > -1:
            #print("stop!")
            receiveBuffer = receiveBuffer+output[:index]
            #print(receiveBuffer)
            receiveStatus = 0
            DATA = receiveBuffer
            newData = True
            
        if receiveStatus==1:
            receiveBuffer = receiveBuffer+output
        
    process.kill()

def startupRecognition():
    global DATA, stopReader
    #process = subprocess.Popen(['echo', '"Hello stdout"'], stdout=subprocess.PIPE)
    #process = subprocess.Popen(["python", "testPrinter.py"], stdout=subprocess.PIPE)
    process = subprocess.Popen(["python", "featureGrabber.py"], stdout=subprocess.PIPE)
    
    threadReader = threading.Thread(target=dataReceiver, args=(process,)) 
    threadReader.start()

    print("waiting for the recognition model to start up, this can take a minute")
    print("please make sure privacy cover is away from the camera")
    t=0
    timer=0
    while process.poll() is None and len(DATA)==0: # wait untill first data is received
        t=t+1
        if t>100000:
            print(".", end='')
            t=0
            timer=timer+1
            
    assert len(DATA)>0,"ERROR: something went wrong, couldn't have communication with the recognition model"
    print("took us",timer)
    print("\nlets goooo!!!")
    
    return process

def storeDatapoint(targetLoc):
    global DATA
    
    print("targetLoc:",targetLoc,"DATA:",DATA)
    data = DATA
    DATA=""             
    data = json.loads(data)     
    

def main():
    global stopReader
    started=False
    
    process = startupRecognition()
    screenSize = pyautogui.size()
    screenSize = screenShape()
    screenSize.width = 100
    screenSize.height = 100
    screen, screenSize, targetLoc = game_init(screenSize, fullScreen=False)
    
    while True:    
        cv2.imshow('window', screen)
        
        if len(DATA)>0:
            dotGreen(screen, targetLoc)
        
        key = cv2.waitKey(1)
        if key == 32:
            if len(DATA)>0:
                if started:
                    storeDatapoint(targetLoc)
                else:
                    started=True
                targetLoc = create_dot(screen, screenSize)
            else:
                print("no new data")
    
        #cv2.putText(screen, 'face', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2, cv2.LINE_AA)
        
        if key == 27:
            stopReader=True
            print("quitting")
            break
        
        if process.poll() is not None:
            print("the model stopped, will quit now too")
            stopReader=True
            break
    cv2.destroyAllWindows()
    
main()
