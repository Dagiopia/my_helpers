#!/usr/bin/env python 

import cv2
import numpy as np
import time
import sys

hue_h = 0
saturation_h = 0
value_h = 0

hue_l = 0
saturation_l = 0
value_l = 0


WIDTH = 500
HEIGHT = 500

QUADS = {1 : [0, HEIGHT/2, 0, WIDTH/2],
2 : [0, HEIGHT/2, WIDTH/2, WIDTH], 
3 : [HEIGHT/2, HEIGHT, WIDTH/2, WIDTH],
4 : [HEIGHT/2, HEIGHT, 0, WIDTH/2]}



def hue_trackbar_handler(pos):
	global hue_h
	#print "Hue Position at %d" % pos
	hue_h = pos
	
def sat_trackbar_handler(pos):
	global saturation_h
	#print "Saturation Position at %d" % pos
	saturation_h = pos
	
def val_trackbar_handler(pos):
	global value_h
	#print "Value Position at %d" % pos
	value_h = pos

def hue_trackbar_handler2(pos):
	global hue_l
	#print "Hue Position at %d" % pos
	hue_l = pos
	
def sat_trackbar_handler2(pos):
	global saturation_l
	#print "Saturation Position at %d" % pos
	saturation_l = pos
	
def val_trackbar_handler2(pos):
	global value_l
	#print "Value Position at %d" % pos
	value_l = pos
		

def create_empty_image(height, width, color, color_format='bgr'):
	global img_color
	if color_format == 'rgb':
		color.reverse()
	img_color = []
	for h in xrange(height):
		img_color.append([])
		for w in xrange(width):
			img_color[-1].append(np.uint8(color))
	img_color = np.array(img_color)
	
def color_a_quad(quad_no, color, color_format='bgr'):
	if color_format == 'rgb':
		color.reverse()
	for h in range(QUADS[quad_no][0], QUADS[quad_no][1]):
		for w in range(QUADS[quad_no][2], QUADS[quad_no][3]):
			img_color[h][w] = np.uint8(color)
			

	
if __name__ == "__main__":
	cv2.namedWindow('yo_hsv_bars')
	cv2.createTrackbar('Hue Upper', 'yo_hsv_bars', 0, 179, hue_trackbar_handler)
	cv2.createTrackbar('Saturation Upper', 'yo_hsv_bars', 0, 255, sat_trackbar_handler)
	cv2.createTrackbar('Value Upper', 'yo_hsv_bars', 0, 255, val_trackbar_handler)
	cv2.createTrackbar('Hue Lower', 'yo_hsv_bars', 0, 179, hue_trackbar_handler2)
	cv2.createTrackbar('Saturation Lower', 'yo_hsv_bars', 0, 255, sat_trackbar_handler2)
	cv2.createTrackbar('Value Lower', 'yo_hsv_bars', 0, 255, val_trackbar_handler2)
	create_empty_image(HEIGHT, WIDTH, [0, 0, 255])
	np.shape(img_color)
	img_bk = img_color.copy()
	cv2.imshow('Colors', img_color)
	img_f = cv2.imread(sys.argv[1])
	while(1):
		hsv_upper = np.array([hue_h, saturation_h, value_h], np.uint8)
		hsv_lower = np.array([hue_l, saturation_l, value_l], np.uint8)
		print hsv_upper
		hsv_color_h = cv2.cvtColor(np.uint8([[[hue_h, saturation_h, value_h]]]), cv2.COLOR_HSV2BGR)
		hsv_color_l = cv2.cvtColor(np.uint8([[[hue_l, saturation_l, value_l]]]), cv2.COLOR_HSV2BGR)
		img_color = img_bk.copy()
		color_a_quad(1, hsv_color_h)
		color_a_quad(3, hsv_color_l)
		img_hsv = cv2.cvtColor(img_f, cv2.COLOR_BGR2HSV)
		img_bin = cv2.inRange(img_hsv, hsv_upper, hsv_lower)
		bgr_val = str(hsv_color_h[0][0][0]) + ',' + str(hsv_color_h[0][0][1]) + ',' + str(hsv_color_h[0][0][2])
		rgb_val = str(hsv_color_h[0][0][2]) + ',' + str(hsv_color_h[0][0][1]) + ',' + str(hsv_color_h[0][0][0])
		cv2.putText(img_color, 'BGR: '+bgr_val, (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
		cv2.putText(img_color, 'RGB: '+rgb_val, (350, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
		cv2.imshow('Colors', img_color)
		cv2.imshow('image', img_bin)
		cv2.waitKey(20)
		#time.sleep(0.01)
	
