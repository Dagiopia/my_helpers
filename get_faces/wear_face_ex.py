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
from matplotlib import pyplot as plt


RBI = 21
RBO = 17
LBI = 22
LBO = 26

X = 0
Y = 1


if len(sys.argv) != 3:
    exit()

dir_name = sys.argv[1]
csv_file = dir_name+'/'+sys.argv[2]

cf = csv.reader(open(csv_file, 'r'))
new_dir = dir_name+'_face'
os.mkdir(new_dir)


REH1S = []
REH2S = []
LEH1S = []
LEH2S = []
DS = []
DLS = []
DRS = []
MH1S = []
MH2S = []


for l in cf:
    f_name = l[0]
    img = cv2.imread(f_name)
    pts = []
    for p in range(3, len(l), 2):
        pts.append((int(l[p]), int(l[p+1])))

    REB = np.average([pts[36][Y], pts[39][Y]])
    LEB = np.average([pts[42][Y], pts[45][Y]])
    REH1 = np.abs(REB - np.average([pts[37][Y], pts[38][Y]]))
    REH2 = np.abs(REB - np.average([pts[40][Y], pts[41][Y]]))
    LEH1 = np.abs(LEB - np.average([pts[43][Y], pts[44][Y]]))
    LEH2 = np.abs(LEB - np.average([pts[46][Y], pts[47][Y]]))

    LEBYAVG = np.average([pts[46][Y], pts[47][Y]]) # LEFT EYE BOTTOM AVERAGE Y LEVEL
    REBYAVG = np.average([pts[40][Y], pts[41][Y]]) # RIGHT EYE BOTTOM AVERAGE Y LEVEL
    D = np.abs(np.sqrt(pts[RBI][X] + np.sqrt(pts[RBI][Y])) - np.sqrt(pts[LBI][X] + np.sqrt(pts[LBI][Y]))) # DISTANCE BETWEEN INNER BROW
    DL = np.abs(LEBYAVG - pts[48][Y]) # D LEFT
    DR = np.abs(REBYAVG - pts[54][Y]) # D RIGHT
    MM = np.average([pts[48][Y], pts[54][Y]]) # MOUTH MIDDLE LINE
    MH1 = np.abs(np.average([pts[50][Y], pts[51][Y], pts[52][Y]]) - MM)
    MH2 = np.abs(np.average([pts[56][Y], pts[57][Y], pts[58][Y]]) - MM)

    REH1S.append(REH1);REH2S.append(REH2)
    LEH1S.append(LEH1);LEH2S.append(LEH2)
    DS.append(D)
    DLS.append(DL);DRS.append(DR)
    MH1S.append(MH1)
    MH2S.append(MH2)

    #eye level
    cv2.line(img, pts[36], pts[45], (0, 255, 0), 2, cv2.LINE_8)
    #mouth level
    cv2.line(img, pts[48], pts[54], (0, 255, 0), 2, cv2.LINE_8)
    cv2.imwrite(f_name.replace(dir_name, new_dir), img)


print "REH1 Average: ", np.average(REH1S)
print "REH2 Average: ", np.average(REH2S)
print "LEH1 Average: ", np.average(LEH1S)
print "LEH2 Average: ", np.average(LEH2S)
print "D Average: ", np.average(DS)
print "DL Average: ", np.average(DLS)
print "DR Average: ", np.average(DRS)
print "MH1 Average: ", np.average(MH1S)
print "MH2 Average: ", np.average(MH2S)

fig, ax = plt.subplots(3, 3)

ax[0][0].scatter(REH1S, range(len(REH1S)), c='red', s=5.0, label='REH1S')
ax[0][1].scatter(REH2S, range(len(REH2S)), c='red', s=5.0, label='REH2S')
ax[0][2].scatter(LEH1S, range(len(LEH1S)), c='red', s=5.0, label='LEH1S')
ax[1][0].scatter(LEH2S, range(len(LEH2S)), c='red', s=5.0, label='LEH2S')
ax[1][1].scatter(DS, range(len(DS)), c='red', s=5.0, label='DS')
ax[1][2].scatter(DLS, range(len(DLS)), c='red', s=5.0, label='DLS')
ax[2][0].scatter(DRS, range(len(DRS)), c='red', s=5.0, label='DRS')
ax[2][1].scatter(MH1S, range(len(MH1S)), c='red', s=5.0, label='MH1S')
ax[2][2].scatter(MH2S, range(len(MH2S)), c='red', s=5.0, label='MH2S')
#ax.legend()
#ax.grid(True)
#fig.add_subplot(ax)
plt.show()
