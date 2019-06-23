#! /usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 00:48:18
# @Description: 
"""

import os
import time

import cv2
import numpy as np

import loadimg as ld

def cover_single(top, bottom, mask_top, 
                 mask_bottom, above, offset):
    row, col = top.shape[0:2]
    res = np.zeros((row, col, 3), np.float32)
    # use input1 as background
    for x in range(col):
        for y in range(row):
            # Because in the segment part, the masks have been 
            # restricted in the rectangle area of top and bottom, 
            # when query the value of mask by the coordinate
            # adding offset, it may be needn't to judge whether
            # x+offset['x'] or y+offset['y'] has out of range of 
            # image. But to insure the correction of program, 
            # these judgement are kept.
            if above == 'top':
                # Through observation, the output image is based on 
                # top image. The poisition of model to the model in
                # the top image is the same as output image.
                # So use top image as background.
                if (x+offset['x'] < col and 
                    y+offset['y'] < row and 
                    mask_top[y, x] == 0 and 
                    mask_bottom[y+offset['y'], x+offset['x']] == 255):
                    # draw the part that top does not cover the bottom
                    res[y, x] = bottom[y+offset['y'], x+offset['x']]
                else:
                    # Copy the rest part of top img 
                    # because top image is used as 
                    # backgound of output image.
                    res[y, x] = top[y, x]
            elif above == 'bottom':
                if (x+offset['x'] < col and 
                    y+offset['y'] < row and 
                    mask_bottom[y+offset['y'], x+offset['x']] == 255):
                    # draw the bottom
                    res[y, x] = bottom[y+offset['y'], x+offset['x']]
                else:
                    # copy the top
                    res[y, x] = top[y, x]
    return res 

def cover_all(confs, above, offsets, masks):
    for i in range(confs['datasets_num']):
        # load top and bottom 
        top_name = confs['input_path'][i][0]
        bottom_name = confs['input_path'][i][1]
        try:
            top = ld.load_img(top_name, cv2.IMREAD_COLOR, False, 0)
            bottom= ld.load_img(bottom_name, cv2.IMREAD_COLOR, False, 0)
        except IOError:
            return

        try:
            mask_top = masks[i]['1']
            mask_bottom = masks[i]['2']
        except IndexError:
            return

        t_s = time.time()
        res = cover_single(top, bottom, mask_top, mask_bottom,
                           above[i], offsets[i])
        t_e  = time.time()

        print('00{0:d} cover completed in {1:.2f}s'\
              .format(i+1, t_e - t_s)) 

        cv2.imwrite(confs['output_path'][i], res)
