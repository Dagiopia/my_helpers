#!/usr/bin/env python

'''
  Read the csv file from created by get_faces.py and the face images 
  then put the landmark points on them for verification
      ./wear_lms.py DIR CSV [extension]
'''

import csv
import cv2
import os
import numpy as np
import sys


if [3,4].count(len(sys.argv)) == 0:
    exit()

dir_name = sys.argv[1]
csv_file = dir_name+'/'+sys.argv[2]
f_ext = 'jpg'
if len(sys.argv) == 4:
    f_ext = sys.argv[3].replace('.', '')

#imgs = glob.glob(dir_name+'/*.'+f_ext)

cf = csv.reader(open(csv_file, 'r'))
new_dir = dir_name+'_lms'
os.mkdir(new_dir)

for l in cf:
    f_name = dir_name+'/'+l[0]+'.'+f_ext
    img = cv2.imread(f_name)
    for p in range(1, len(l)-1, 2):
        img = cv2.circle(img, (int(l[p]), int(l[p+1])), 1, (0, 255, 0), 1)
    cv2.imwrite(f_name.replace(dir_name, new_dir), img), f_name
