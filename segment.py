import os
import time

import cv2
import numpy as np

from load_img import *
from grow_gray import *

def segment_gray(confs, same, save):
    masks = []
    for i in range(confs['datasets_num']):
        one_dataset = {}
        for j in range(confs['inputs_num']):
            # skip input3
            if j == 2:
                continue
            read_name = confs['input_path'][i][j]
            # find same
            try:
                if same[i][j] != i:
                    # there are previous same input image
                    origin = same[i][j]
                    one_dataset[str(j+1)] = masks[origin][str(j+1)] 
                else:
                    # read red channel of input1 and input2
                    # to segment the top and the bottom
                    if j == 0:
                        img = load_img(read_name, 
                                       cv2.IMREAD_COLOR, 
                                       True, 2)
                        seed = confs['seed_top']
                        thre = confs['thre_top']
                        rect = confs['rect_top']
                    elif j == 1:
                        img = load_img(read_name, 
                                       cv2.IMREAD_COLOR, 
                                       True, 2)
                        seed = confs['seed_bottom']
                        thre = confs['thre_bottom']
                        rect = confs['rect_bottom']
                        # read blue channel of input4 to decide
                        # whether the top or the bottom is above
                    elif j == 3:
                        img = load_img(read_name, 
                                       cv2.IMREAD_COLOR, 
                                       True, 0)
                        seed = confs['seed_input4']
                        thre = confs['thre_input4']
                        rect = confs['rect_top']

                    t_s = time.time()
                    res = gray_region_growing(img, seed, thre, rect)
                    t_e = time.time()
                    print(read_name + ' segmentation completed in ' + str(t_e - t_s))
                    one_dataset[str(j+1)] = res
            except IndexError:
                return masks
            if save:
                cv2.imwrite(confs['mask_path'][i][j], one_dataset[str(j+1)])

        masks.append(one_dataset)

    return masks
