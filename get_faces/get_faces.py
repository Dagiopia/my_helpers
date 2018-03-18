#!/usr/bin/env python

"""
  Get faces from video files or camera
  cmd params:
  	get_faces.py video_file collection_name [extension]
"""

import cv2
import numpy as np
import sys
import os
import time

if 3 > len(sys.argv) or 4 < len(sys.argv): 
    exit()

video_src = sys.argv[1]
if video_src.isdigit() and len(video_src) == 1:
    video_src = int(video_src)
coll_name = sys.argv[2]
dir_name = coll_name
d = os.listdir('.')
if d.count(dir_name) > 0:
    dir_name = coll_name+str(int(time.time()))
os.mkdir(dir_name)

save_ext = "jpg"
if len(sys.argv) == 4:
    save_ext = sys.argv[3].replace(".", "")

cap = cv2.VideoCapture(video_src)
face_detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
face_count = 0
while True:
    ret, img = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, 1.1, minSize=(55, 55))
    for (x, y, w, h) in faces:
    	cimg = img[y:y+h, x:x+w]
	cv2.imwrite(dir_name+"/"+coll_name+str(face_count)+"."+save_ext, cimg)
	face_count+=1
