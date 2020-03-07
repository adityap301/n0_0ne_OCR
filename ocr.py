# USAGE
# python ocr.py --image images/example_01.png 
# python ocr.py --image images/example_02.png  --preprocess blur

# import the necessary packages
from PIL import Image
import numpy as np
import pytesseract
import argparse
import cv2
import os
def loadimg(image):
    return image
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())
# load the image from disk
image = cv2.imread(args["image"])
#image = cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
#image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)


# convert the image to grayscale and flip the foreground
# and background to ensure foreground is now "white" and
# the background is "black"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
if angle < -45:
	angle = -(90 + angle)
# otherwise, just take the inverse of the angle to make
# it positive
else:
	angle = -angle

# rotate the image to deskew it
(h, w) = gray.shape[:2]
if h<w:
    angle=-90
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
# draw the correction angle on the image so we can validate it
# show the output image

#print("[INFO] angle: {:.3f}".format(angle))
#cv2.imshow("Input", image)
#cv2.imshow("Rotated", rotated)
cv2.waitKey(0)
# load the example image and convert it to grayscale
#image = cv2.imread(args["image"])
gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

#cv2.imshow("Image", gray)

# check to see if we should apply thresholding to preprocess the
# image
#cv2.imshow('thresh1', thresh1)

if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 240,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

ret,gray = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

# show the output images
# cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)