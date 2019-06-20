def conf():
	datasets_num = 8
	inputs_num = 4

	img_names = []
	# generate input image names
	for i in range(datasets_num):
		one_dataset = []
		for j in range(inputs_num):
			name = '00' + str(i+1) \
				+ '-input' + str(j+1) \
				+ '.jpg'
			one_dataset.append(name)	
		img_names.append(one_dataset)

	channels_path = '../channels/'
	masks_path = '../masks/'

	seed_top = [0.63150289017341,
		 0.168509615384615]
	seed_input4 = [
		0.544075144508671,	
		0.277403846153846]
	seed_bottom = [0.5248, 0.440]

	thre_top = 100
	thre_input4 = 20
	thre_bottom = 90 
	thre_feet = 200

	rect_top = [			
		0.180635838150289, 	# left
		0.048076923076923,	# top
		0.794797687861272,	# right
		0.649038461538462]	# bottom
	rect_bottom = [
		0.180635838150289, 	# left
		0.240384615384615, 	# top
		0.794797687861272, 	# right
		0.919471153846154]	# bottom

	waist_line = [
		0.469653179190751,	# left	
		0.596098265895954, 	# right
		0.360576923076923]	# height
	confs = {}

	confs['datasets_num'] = datasets_num
	confs['inputs_num'] = inputs_num
	confs['img_names'] = img_names
	confs['channels_path'] = channels_path
	confs['masks_path'] = masks_path
	confs['seed_top'] = seed_top
	confs['seed_input4'] = seed_input4
	confs['seed_bottom'] = seed_bottom
	confs['thre_top'] = thre_top
	confs['thre_input4'] = thre_input4
	confs['thre_bottom'] = thre_bottom
	confs['thre_feet'] = thre_feet
	confs['rect_top'] = rect_top
	confs['rect_bottom'] = rect_bottom
	confs['waist_line'] = waist_line

	return confs
