import os,glob
import string
import ntpath
from random import shuffle
import random
import numpy as np
# import cv2


f = open('fbx_file.txt','w')
folder_path = '/Users/qiyang/Documents/SIGGRAPHAsia/fbx/mixamo/AJ/with_skin'
for root,d,files in os.walk(folder_path):
	for ff in files:
		if ff.endswith('.fbx'):
			save_path = os.path.join(root,ff)+'\n'
			f.write(save_path)


f.close()

f = open('/Users/qiyang/Documents/SIGGRAPHAsia/fbx/codes/fbx_file.txt','r')
models = f.readlines()
f.close()

fn , tl = os.path.split(models[0])
render_path = fn+'_img'
print(render_path)