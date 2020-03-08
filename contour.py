# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 21:30:36 2020

@author: siddh
"""

import cv2
import numpy as np
#from PIL import Image
#
#import pytesseract
#import argparse
#import cv2
#import os
#import shutil



#ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--preprocess", type=str, default="thresh",
#	help="type of preprocessing to be done")
#img = vars(ap.parse_args())

image=cv2.imread(r"C:\Users\siddh\Desktop\Train-data\29.jpg")
scale_percent = 70 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)#cv2.imshow('image', image)
#cv2.waitKey()
#height,width,channel = img.shape
#blur = cv2.GaussianBlur(img,(5,5),0)
#cv2.imshow('sample image',img)
#cv2.waitKey(0) # waits until a key is pressed
#cv2.destroyAllWindows()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=4)

#cv2.imshow('sample image',thresh)
#cv2.waitKey(0) # waits until a key is pressed
#cv2.destroyAllWindows()

# Find contours and draw rectangle
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#for c in cnts:
#    x,y,w,h = cv2.boundingRect(c)
#    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
for c in cnts:
    rect = cv2.boundingRect(c)
    if rect[2] < 60 or rect[3] < 60 : continue

    print (cv2.contourArea(c))
    x,y,w,h = rect
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

#cv2.imshow('thresh', thresh)
#cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.waitKey()