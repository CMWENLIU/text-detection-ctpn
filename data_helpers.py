import os
import numpy as np
import pandas as pd
import re
import itertools
from collections import Counter
import pyocr
import pyocr.builders
import PIL
from PIL import Image

def clean_str(string):

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def process_raw(string):    
    string = string.replace('\n', ' ') #replace line break with space
    string = re.sub(' +',' ', string) #replace all extra white spaces
    #return string.strip().lower()
    return string

def ext_txt(imgf, languages, record, tool):
    record['file'] = imgf
    for l in languages:
        txt = tool.image_to_string(Image.open(imgf), lang=l, builder=pyocr.builders.TextBuilder())
        clean = process_raw(txt).encode('utf-8')
        record[l] = clean
    return record

def similarity(a, b):
    tokens_a = a.split()
    tokens_b = b.split()
    inter_len = len(list(set(tokens_a) & set(tokens_b)))
    ratio = inter_len/min(len(tokens_a), len(tokens_b))
    return ratio
def image_crop(imagepath):
    imagename = os.path.basename(imagepath)
    crop_file = 'data/results/res_' + os.path.splitext(imagename)[0] + '.txt'
    crop_list = []
    image_obj = Image.open(imagepath)
    with open(crop_file, 'r') as crops:
      for line in crops:
        crop = line.split(',')
        crop = map(int, crop)
        crop_list.append(crop)
    crop_list = sorted(crop_list, key=lambda x: x[3]-x[1])
    crop_list.reverse()
    for idx, val in enumerate(crop_list[:9]):
      if (val[2]-val[0]) > 3*(val[3]-val[1]):
        cropped_image = image_obj.crop(val)
        cropped_image.save('data/results/' + os.path.splitext(imagename)[0] + '_cro_pped_' + str(idx+10) + '.jpg')

def compare_gt(result):
    df = pd.read_csv(result)
    fnames = df['file'].tolist()
    content = df['eng'].tolist()
    newfnames, tessract, rec_tess = [],[],[]
    index = 0
    s = ''
    for idx, val in enumerate(fnames):
      if '_cro_pped_' not in val:
        if s!='':
          rec_tess.append(s)
          s = ''
        newfnames.append(val)
        tessract.append(content[idx])
      else:
        s += (str(content[idx])+' ')
    rec_tess.append(s)
    odf = pd.DataFrame()
    odf['file'] = newfnames
    odf['tess'] = tessract
    odf['rec_tess'] = rec_tess
    odf.to_csv('compare_gt.csv', encoding='utf_8_sig', index=False)
                      
def filter_images(result, filters):
		with open(filters) as todelist:
				content = todelist.readlines()
		content = [x.strip() for x in content]
		df = pd.read_csv(result)
		englist = df['eng']
		mylist = []
		for l in englist:
				ll = re.sub(' +',' ', l)
				mylist.append(ll)
		df['eng'] = mylist
		
		count = 0
		for index, row in df.iterrows():
#				if any(map(row['eng'].startswith, content)):
				if any(s in row['eng'] for s in content):
						count += 1
						print(row['file'])
						#os.remove(row['file'])		

#for s in content:
#						if row['eng'].startswith(s):
#								print(s)
#								count += 1
#								break
		print(len(content))
		print(df.count())		
		print(count)
		#dedf = df[df['eng'].str.startswith('> 2 ere th, three times daily or as directed by phy')]
		#print(dedf.count())

#filter_images('result.csv', 'todelete.txt')

compare_gt('result.csv')

    
