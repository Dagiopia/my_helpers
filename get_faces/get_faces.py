#!/usr/bin/env python

"""
  Get faces from video files or camera also landmarks if arg l is given
  cmd params:
  	get_faces.py video_file collection_name [extension] [l]
  landmarks will be in a single csv file with the follwing format
        face_file_name, x, y, x, y, x, y...
  where the first x,y pair are the 0th point and the second the 1st and so on...
  the landmarks are using the file shape_predictor_face_landmarks.dat model from dlib
  didn't upload the shape predictor model cuz it's too big
  it can be found here: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
"""

import cv2
import numpy as np
import sys
import os
import time
import dlib
import csv


def equalize(img, img2):
    r1, c1, _ = np.shape(img)
    r2, c2, _ = np.shape(img2)
    return img[:min(r1, r2), :min(c1, c2)], img2[:min(r1, r2), :min(c1, c2)]



if [3, 4, 5].count(len(sys.argv)) == 0: 
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
get_lms = False
if len(sys.argv) > 3:
    for i in range(3, len(sys.argv)):
        if sys.argv[i] == 'l':
            get_lms = True
        else:
            save_ext = sys.argv[i].replace(".", "")

cap = cv2.VideoCapture(video_src)
face_detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
face_count = 0
first_face = np.ndarray((200, 200, 3), dtype=np.uint8)
pred = None
lm_csv = None
if get_lms:
   pred = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
   lm_csv = csv.writer(open(dir_name+"/"+coll_name+'_lms.csv', 'w'))

while True:
    ret, img = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, 1.1, minSize=(55, 55))
    for (x, y, w, h) in faces:
    	cimg = img[y:y+h+int(h*0.1), x:x+w+int(w*0.1)]
	first_face, cimg = equalize(first_face, cimg)
	if cv2.absdiff(first_face, cimg).mean() > 15:
		save_file_path = os.getcwd() + '/' + dir_name+"/"+coll_name+str(face_count)+"."+save_ext
		cv2.imwrite(save_file_path, cimg)
		first_face = cimg
		cimg = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
		if get_lms:
		    drect = dlib.rectangle(0, 0, np.long(w), np.long(h))
		    shape = pred(cimg, drect)
		    l = [save_file_path]
		    l.append(w)
		    l.append(h)
		    for i in shape.parts():
		    	l.append(i.x)
			l.append(i.y)
		    lm_csv.writerow(l)

		face_count+=1
	
