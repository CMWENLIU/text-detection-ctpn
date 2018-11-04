# import all tools and libraries
import os
import re
#import cv2
import glob
#import spacy
import time
import datetime
import data_helpers
import process_image
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#import PIL
#from PIL import Image
from random import randint
#import matplotlib
#import matplotlib.pyplot as plt
#import pillowfight
#import numpy as np
#import pandas as pd
import sys
import pyocr
import pyocr.builders

print('All tools are imported successfully')

# Next is to prepare Tesseract OCR tools
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print('There are 130 languages available!')
print('We will use following languages:')
print(', '.join(langs))

# build globle variables:
all_res = [] 
dic = {'file': '-'}
for l in langs:
    dic[l] = '-'
files_grabbed = [] #create list for all files

# Load all type of available image files
ext = ['jpg', 'png','bmp', 'jpeg','JPG', 'PNG', 'BMP', 'JPEG']

for root, dirs, files in os.walk("images/"):
    for file in files:
        if file.endswith(tuple(ext)):
             files_grabbed.append(os.path.join(root, file))
print ('There are ' + str(len(files_grabbed)) + ' images loaded')

#Following we recognize all images and write to database.
print('Following we recognize all images and write all text to database.')
i = 1
for f in files_grabbed:
    try:
      result = data_helpers.ext_txt(f, langs, dic, tool)
    except ValueError:
      print('Error for: ' + f)
    time_str = datetime.datetime.now().isoformat()
    if i % 10 == 0 or i > (len(files_grabbed)//10)*10:
        print("{}: {}/{} processed".format(time_str, i, len(files_grabbed),))
    all_res.append(result.copy())
    i += 1


df = pd.DataFrame(all_res)
df.to_csv('result.csv', header=True, columns=['file', 'eng', 'fra', 'spa','chi_sim'], index=False)
print('All images have been recognized and saved to result.csv')

with open('result.html', 'w') as outf:
    with open('htmlhead.txt', 'r') as fh:
        for line in fh:
            outf.write(line)
    imghead = '<img src="'
    imgtail = '" onclick="changesize(this)">'
    for item in all_res:
        outf.write(imghead + item['file'] + imgtail)
        outf.write('<p>--English:' + item['eng'] + '</p>' + '\n')
        outf.write('<p>--French:' + item['fra']+ '</p>' + '\n')
        outf.write('<p>--Spanish:' + item['spa'] + '</p>' + '\n')
        outf.write('<p>--Chinese:' + item['chi_sim'] + '</p>' + '\n')
        outf.write('<hr>' + '\n')
    with open('htmltail.txt', 'r') as ft:
        for line in ft:
            outf.write(line)
print('All images have been recognized and saved to result.html')
