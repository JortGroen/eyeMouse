#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:54:57 2020

@author: djoghurt
"""

import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("src/3rdparty/shape_predictor_68_face_landmarks.dat")

mapping = [45, 42, 36, 39, 33]

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    if len(faces)>0:
            face = faces[0]
            landmarks = predictor(gray, face)
            for i in range(landmarks.num_parts):
                p = landmarks.part(i)
                cv2.circle(frame, (p.x, p.y), 3, (0,0,255), -1)
                cv2.putText(frame, str(i), (p.x, p.y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 1, cv2.LINE_AA)
                
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()