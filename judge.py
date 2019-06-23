#! /usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 00:47:37
# @Description: 
"""

import os
import time

import cv2

import saveres as sv

# extract waist line of mask
def extract(mask, judge_line):
    row, col = mask.shape[0:2]
    left = int(judge_line[0] * col)
    right = int(judge_line[1] * col)
    height = int(judge_line[2] * row)

    line = []
    y = height

    for x in range(right-left):
        line.append(mask[y, x+left])

    return line, len(line)

# judge whether top is above 
# with the extracted line
def top_above(line, length):
    for i in range(length):
        if line[i] != 0: # top above
            return True 
    return False # bottom above 

def judge_above(confs, masks, save):
    above = []
    # extract line from input1
    for i in range(confs['datasets_num']):
        # read mask of input4
        try:
            mask_input4 = masks[i]['4']
        except IndexError:
            if save:
                sv.save_res(confs['above_path'], above)
            return above
        t_s = time.time()
        # extract line from mask of input4
        line, length = extract(mask_input4, confs['waist_line'])
        if top_above(line, length):
            above.append('top')
        else:
            above.append('bottom')
        t_e = time.time()
        print('00{0:d} judgement completed in {1:.2f}s'\
              .format(i+1, t_e - t_s)) 

    if save:
        sv.save_res(confs['above_path'], above)
    return above
