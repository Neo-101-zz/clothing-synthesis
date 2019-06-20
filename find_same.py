import cv2
from load_img import *
import time

def is_same(img_now, img_pre):
	# compare two images'  shape
	if img_now.shape == img_pre.shape:
		difference = cv2.subtract(img_now, img_pre)
		b, g, r = cv2.split(difference)
		if cv2.countNonZero(b) == 0 \
			and cv2.countNonZero(g) == 0 \
			and cv2.countNonZero(r) == 0:
			return True

	return False

def find_same(confs):
	t_s = time.time()	

	same = []

	for i in range(confs['datasets_num']):
		one_dataset = []
		for j in range(confs['inputs_num']):
			find_same = False
			# find same imgs
			for k in range(i):
				img_now_name = confs['img_names'][i][j] 
				img_pre_name = confs['img_names'][k][j]	
				try:
					img_now = load_img(img_now_name, 
							   cv2.IMREAD_COLOR, 
							   False, 0)
					img_pre = load_img(img_pre_name,
							   cv2.IMREAD_COLOR,
							   False, 0)
				except IOError:
					return same
				if is_same(img_now, img_pre) == True:	
					find_same = True
					one_dataset.append(k)
					print(img_now_name + ' and ' + 
					      img_pre_name + 
					     ' are completely Equal')		
					break
			if find_same == False: 
				one_dataset.append(i)
		same.append(one_dataset)

	t_e = time.time()
	print('find_same complete in ' + str(t_e - t_s))

	return same
