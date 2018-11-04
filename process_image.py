import cv2
import numpy as np
import sys
import os.path

def rescale(img):
    newimg = cv2.resize(img,None,fx=1.2, fy=1.2, interpolation = cv2.INTER_LINEAR)
    #towt = os.path.join('/img-transfer', 're.jpg')    
    cv2.imwrite('re.jpg', newimg)

    return newimg

def binarize(img):
    newimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #towt = os.path.join('/img-transfer', 'gray.jpg')
    cv2.imwrite('gray.jpg', newimg)
    return newimg

def remove_noise(img):
    newimg = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    return newimg

def improve(input_file):
    # Load the image
    img = cv2.imread(input_file)
    #towt = os.path.join('/img-transfer', 'ori.jpg')
    cv2.imwrite('ori.jpg', img)
    img = rescale(img)
    img = binarize(img)
    #output_file = remove_noise(output_file)
    #output_file = rescale(output_file)
