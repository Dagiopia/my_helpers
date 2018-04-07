#!/usr/bin/env python

"""
  Get faces from video files or camera also landmarks if arg l is given
  cmd params:
  	get_faces.py video_file collection_name [extension] [l]
	get_faces.py -v video_file/camera_id -i image_dir -c collection_name [-nd] [-x extension] [-l]
  landmarks will be in a single csv file with the follwing format
        face_file_abspath, w, h, x, y, x, y, x, y...
  where the first w,h pair is the width and height of the image and the following 
  x,y pairs are the 0th , the 1st, the 2nd....  shape points.
  the landmarks are using the file shape_predictor_68_face_landmarks.dat model from dlib
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
import glob


if 5 > len(sys.argv) or 9 < len(sys.argv):
    print "get_faces.py -v video_file/camera_id -i image_dir -c collection_name [-nd] [-x extension] [-l]" 
    exit()

from_video = True
image_src = ""
coll_name = ""
file_ext = "jpg"
get_lms = False
no_fd = False

cap = None
img_glob = None
img_glob_idx = 0
no_images = 0
get_img = None
face_detect = None


i = 1
while i < len(sys.argv):
    if sys.argv[i] == "-v":
        image_src = sys.argv[i+1]
	i += 2
    elif sys.argv[i] == "-i":
        image_src = sys.argv[i+1]
	from_video = False
	i += 2
    elif sys.argv[i] == "-c":
        coll_name = sys.argv[i+1]
	i += 2
    elif sys.argv[i] == "-x":
        file_ext = sys.argv[i+1]
	i += 2
    elif sys.argv[i] == "-l":
        get_lms = True
	i += 1
    elif sys.argv[i] == "-nd":
        no_fd = True
	i+= 1
    else:
        print "Unknown Option: ", sys.argv[i]
	exit()
    

def get_video_frame():
    global cap
    _, img = cap.read()
    if not _: 
       exit()
    return img

def get_image_from_dir():
    global img_glob
    global img_glob_idx
    if img_glob_idx == no_images:
        exit()
    img = cv2.imread(img_glob[img_glob_idx])
    img_glob_idx += 1
    return img

def face_d(img):
    global face_detect
    if len(np.shape(img)) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_detect.detectMultiScale(img, 1.1, minSize=(55,55), flags=cv2.CASCADE_SCALE_IMAGE)

def get_video_frame_fd():
    global cap
    _, img = cap.read()
    if not _:
        exit()
    return img, face_d(img)

def get_image_from_dir_fd():
    global img_glob
    global img_glob_idx
    if img_glob_idx == no_images:
        exit()
    img = cv2.imread(img_glob[img_glob_idx])
    img_glob_idx += 1
    return img, face_d(img)


coll_dir_name = coll_name
d = os.listdir('.')
if d.count(coll_dir_name) > 0:
    coll_dir_name = coll_name+str(int(time.time()))

os.mkdir(coll_dir_name)

save_ext = file_ext.replace(".", "")

if from_video:
    if image_src.isdigit() and len(image_src) == 1:
        image_src = int(image_src)
    cap = cv2.VideoCapture(image_src)
    get_img = get_video_frame if no_fd else get_video_frame_fd
else:
    if image_src[-1] == '/':
        image_src = image_src[:-1]
    img_glob = glob.glob(image_src+'/*.'+file_ext)
    no_images = len(img_glob)
    if no_images > 0:
        get_img = get_image_from_dir if no_fd else get_video_frame_fd
    else:
        print "No Images in Dir: ", 

face_detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
face_count = 0
first_face = np.ndarray((200, 200, 3), dtype=np.uint8)
pred = None
lm_csv = None
if get_lms:
   pred = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
   lm_csv = csv.writer(open(coll_dir_name+"/"+coll_name+'_lms.csv', 'w'))



while not no_fd:
    img, faces = get_img()
    for (x, y, w, h) in faces:
        cimg = img[y:y+h+int(h*0.1), x:x+w+int(w*0.1)]
        first_face = cv2.resize(first_face, (np.shape(cimg)[1], np.shape(cimg)[0]),
                               cv2.INTER_LINEAR )
        if cv2.absdiff(first_face, cimg).mean() > 15:
            save_file_path = os.getcwd() + '/' + coll_dir_name+"/"+coll_name+str(face_count)+"."+save_ext
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
	
while no_fd:
    img = get_img()
    w, h, _ = np.shape(img)
    print img_glob_idx
    f_path = os.getcwd() + '/' + img_glob[img_glob_idx-1]
    if get_lms:
        drect = dlib.rectangle(0, 0, np.long(w), np.long(h))
	shape = pred(img, drect)
	l = [f_path]
	l.append(w)
	l.append(h)
	for i in shape.parts():
            l.append(i.x)
            l.append(i.y)
        lm_csv.writerow(l)
    face_count+=1
	
