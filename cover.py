import cv2
import os
import numpy as np
import time
from load_img import *

def cover_single(top, bottom, mask_top, \
		 mask_bottom, above, offset):
	row, col = top.shape[0:2]
	res = np.zeros((row, col, 3), np.float32)

	# use input1 as background
	for x in range(col):
		for y in range(row):
			if above == 'top':
				if x+offset['x'] < col \
				and y+offset['y'] < row \
				and mask_bottom[y+offset['y'], \
						x+offset['x']] \
					== 255 \
				and mask_top[y, x] == 0:
					res[y, x] = bottom[\
						y+offset['y'], \
						x+offset['x']]
				else:
					res[y, x] = top[y, x]
			elif above == 'bottom':
				if x+offset['x'] < col \
				and y+offset['y'] < row \
				and mask_bottom[y+offset['y'], \
					x+offset['x']] == 255:
					res[y, x] = bottom[\
						y+offset['y'], \
						x+offset['x']]
				else:
					res[y, x] = top[y, x]

	return res 

def cover_all(confs, above, offsets, masks):
	for i in range(confs['datasets_num']):
		# load top and bottom 
		top_name = confs['img_names'][i][0]
		bottom_name = confs['img_names'][i][1]
		try:
			top = load_img(top_name, cv2.IMREAD_COLOR, False, 0)
			bottom= load_img(bottom_name, cv2.IMREAD_COLOR, False, 0)
		except IOError:
			return
	
		try:
			mask_top = masks[i]['1']
			mask_bottom = masks[i]['2']
		except IndexError:
			return

		t_s = time.time()
		res = cover_single(top, bottom, mask_top, mask_bottom, above[i], offsets[i])
		t_e  = time.time()
		print('00' + str(i+1) + ' cover complete in '  + str(t_e - t_s))

		write_name = (top_name.split('input'))[0] + 'output.jpg'
		cv2.imwrite(write_name, res)
