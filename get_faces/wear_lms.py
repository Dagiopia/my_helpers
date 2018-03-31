#!/usr/bin/env python

'''
  Read the csv file from created by get_faces.py and the face images 
  then put the landmark points on them for verification
      ./wear_lms.py DIR CSV
'''

import csv
import cv2
import os
import numpy as np
import sys


if len(sys.argv) != 3:
    exit()

dir_name = sys.argv[1]
csv_file = dir_name+'/'+sys.argv[2]

cf = csv.reader(open(csv_file, 'r'))
new_dir = dir_name+'_lms'
os.mkdir(new_dir)

for l in cf:
    f_name = l[0]
    img = cv2.imread(f_name)
    for p in range(3, len(l)-3, 2):
	img = cv2.circle(img, (int(l[p]), int(l[p+1])), 1, (0, 255, 0), 1)
    cv2.imwrite(f_name.replace(dir_name, new_dir), img)
