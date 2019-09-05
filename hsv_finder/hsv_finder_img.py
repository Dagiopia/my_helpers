#!/usr/bin/env python 

'''
Helper script to find HSV ranges of colors.
Uses OpenCV

Dagim Sisay
'''

import cv2
import numpy as np
import time
import sys

hue_h = 0
saturation_h = 0
value_h = 0

hue_l = 255
saturation_l = 255
value_l = 179


WIDTH = 500
HEIGHT = 500

QUADS = {1 : [0, HEIGHT/2, 0, WIDTH/2],
2 : [0, HEIGHT/2, WIDTH/2, WIDTH], 
3 : [HEIGHT/2, HEIGHT, WIDTH/2, WIDTH],
4 : [HEIGHT/2, HEIGHT, 0, WIDTH/2]}


def hue_trackbar_handler(pos):
    global hue_h
    if pos>255:
        pos=255
    hue_h = pos
    update_images()
    
def sat_trackbar_handler(pos):
    global saturation_h
    if pos>255:
        pos=255
    saturation_h = pos
    update_images()
    
def val_trackbar_handler(pos):
    global value_h
    if pos>255:
        pos=255
    value_h = pos
    update_images()

def hue_trackbar_handler2(pos):
    global hue_l
    if pos<0:
        pos=0
    hue_l = pos
    update_images()
    
def sat_trackbar_handler2(pos):
    global saturation_l
    if pos<0:
        pos=0
    saturation_l = pos
    update_images()
    
def val_trackbar_handler2(pos):
    global value_l
    if pos<0:
        pos=0
    value_l = pos
    update_images()
        

def create_empty_image(height, width, color):
    global img_color
    img_color = np.array(np.ones((height, width, 3), np.uint8) * color, dtype=np.uint8)
    
def color_a_quad(quad_no, color, color_format='bgr'):
    if color_format == 'rgb':
        color.reverse()
    for h in range(QUADS[quad_no][0], QUADS[quad_no][1]):
        for w in range(QUADS[quad_no][2], QUADS[quad_no][3]):
            img_color[h][w] = np.uint8(color)

def pick_color(event,x,y,flags,param):
    global hue_l,hue_h,saturation_l,saturation_h,value_l,value_h
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = img_hsv[y,x]

        #you might want to adjust the ranges(+-10, etc):
        if pixel[0] <hue_l: 
            hue_l=pixel[0]-10
            hue_trackbar_handler2(hue_l)
        if pixel[1] <saturation_l: 
            saturation_l=pixel[1]-10
            sat_trackbar_handler2(saturation_l)
        if pixel[2] <value_l: 
            value_l=pixel[2]-20
            val_trackbar_handler2(value_l)
        if pixel[0] >hue_h: 
            hue_h=pixel[0]+10
            hue_trackbar_handler(hue_h)
        if pixel[1] >saturation_h: 
            saturation_h=pixel[1]+10
            sat_trackbar_handler(saturation_h)
        if pixel[2] >value_h: 
            value_h=pixel[2]+20
            val_trackbar_handler(value_h)


def update_images():
    #print "Position Changes"
    cv2.setTrackbarPos('Hue Lower', 'yo_hsv_bars',hue_l)
    cv2.setTrackbarPos('Saturation Lower', 'yo_hsv_bars',saturation_l)
    cv2.setTrackbarPos('Value Lower', 'yo_hsv_bars',value_l)
    cv2.setTrackbarPos('Hue Upper', 'yo_hsv_bars',hue_h)
    cv2.setTrackbarPos('Saturation Upper', 'yo_hsv_bars',saturation_h)
    cv2.setTrackbarPos('Value Upper', 'yo_hsv_bars',value_h)
    hsv_upper = np.array([hue_h, saturation_h, value_h], np.uint8)
    hsv_lower = np.array([hue_l, saturation_l, value_l], np.uint8)
    hsv_color_h = cv2.cvtColor(np.uint8([[[hue_h, saturation_h, value_h]]]), cv2.COLOR_HSV2BGR)
    hsv_color_l = cv2.cvtColor(np.uint8([[[hue_l, saturation_l, value_l]]]), cv2.COLOR_HSV2BGR)
    color_a_quad(1, hsv_color_h)
    color_a_quad(3, hsv_color_l)
    img_range = cv2.inRange(img_hsv, hsv_lower, hsv_upper)
    bgr_val = str(hsv_color_h[0][0][0]) + ',' + str(hsv_color_h[0][0][1]) + ',' + str(hsv_color_h[0][0][2])
    rgb_val = str(hsv_color_h[0][0][2]) + ',' + str(hsv_color_h[0][0][1]) + ',' + str(hsv_color_h[0][0][0])
    cv2.putText(img_color, 'BGR: '+bgr_val, (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
    cv2.putText(img_color, 'RGB: '+rgb_val, (350, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
    cv2.imshow('Colors', img_color)
    cv2.imshow('Image', img_range)


   
if __name__ == "__main__":
    cv2.namedWindow('yo_hsv_bars')
    cv2.namedWindow('hsv')
    cv2.createTrackbar('Hue Lower', 'yo_hsv_bars', 0, 179, hue_trackbar_handler2)
    cv2.createTrackbar('Saturation Lower', 'yo_hsv_bars', 0, 255, sat_trackbar_handler2)
    cv2.createTrackbar('Value Lower', 'yo_hsv_bars', 0, 255, val_trackbar_handler2)
    cv2.createTrackbar('Hue Upper', 'yo_hsv_bars', 0, 179, hue_trackbar_handler)
    cv2.createTrackbar('Saturation Upper', 'yo_hsv_bars', 0, 255, sat_trackbar_handler)
    cv2.createTrackbar('Value Upper', 'yo_hsv_bars', 0, 255, val_trackbar_handler)
    cv2.setMouseCallback('hsv', pick_color)
    create_empty_image(HEIGHT, WIDTH, [0, 0, 255])
    np.shape(img_color)
    img_bk = img_color.copy()
    cv2.imshow('Colors', img_color)
    img_f = cv2.imread(sys.argv[1])
    cv2.imshow('hsv',img_f)
    img_hsv = cv2.cvtColor(img_f, cv2.COLOR_BGR2HSV)
    update_images()
    while 'q' != chr(cv2.waitKey(0) & 0xFF):
        pass
    
