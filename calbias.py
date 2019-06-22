#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 00:47:06
# @Description: 
"""

import os
import time

import cv2

import loadimg as ld
import saveres as sv

def get_axis(mask, rect):
    # there may be holes in the mask
    # So boundingRect() may return
    # the boudning of a hole rather than
    # the whole bounding of top or bottom
    row, col = mask.shape[0:2]
    left = col-1
    right = 0
    left_bound = int(rect[0] * col)
    right_bound = int(rect[2] * col)
    top_bound = int(rect[1] * row)
    bottom_bound = int(rect[3] * row)

    for y in range(top_bound, bottom_bound):
        for x in range(left_bound, right_bound):
            if mask[y, x] == 0:
                continue
            else:
                if x < left:
                    left = x
                if x > right:
                    right = x

    axis = int((left + right) / 2.0)

    return axis

def cal_x_bias(top_mask, bottom_mask, top_rect, bottom_rect):
    top_cen_axis = get_axis(top_mask, top_rect)
    bottom_cen_axis = get_axis(bottom_mask, bottom_rect) 
    # 1.25 is an empirical coefficient to precisely adjust the
    # bias between top and bottom
    x_bias = int((float(bottom_cen_axis - top_cen_axis)) * 1.25) 

    return x_bias

def cal_y_bias(top, bottom, thre):
    # search from bottom
    row, col = top.shape[0:2]
    feet_top = 0
    feet_bottom = 0

    for y in range(row):
        for x in range(col):
            # search model's feet in top image
            if feet_top == 0 and top[row-1-y, x] > thre:
                feet = True
                # verify the feet
                for i in range(20):
                    if x+i < col and top[row-1-y, x+i] > thre:
                        pass
                    else:
                        feet = False
                if feet:
                    feet_top = row-1-y
            # search model's feet in bottom image
            if feet_bottom == 0 and bottom[row-1-y, x] > thre:
                feet = True
                # verify the feet
                for i in range(20):
                    if x+i < col and bottom[row-1-y, x+i] > thre:
                        pass
                    else:
                        feet = False
                if feet:
                    feet_bottom = row-1-y
            # end if have found both feet in top and bottom image
            if feet_top > 0 and feet_bottom > 0:
                return feet_bottom - feet_top

    return feet_bottom - feet_top

def cal_bias(confs, masks, same, save):
    biases = []

    for i in range(confs['datasets_num']):
        top_bottom_same = False
        # find same
        for j in range(i):
            try:
                # find whether top and bottom is same or not
                if same[i][0] == same[j][0] and same[i][1] == same[j][1]:
                    top_bottom_same = True
                    break
            except IndexError:
                if save:
                        sv.save_res(confs['bias_path'], biases)
                return biases

        if top_bottom_same:
            single_bias = biases[j]
            biases.append(single_bias)
            continue

        single_bias = {}
        top_name = confs['input_path'][i][0]
        bottom_name = confs['input_path'][i][1]

        # cal x bias
        try:
            top_mask = masks[i]['1'] 
            bottom_mask = masks[i]['2'] 
        except IndexError:
            if save:
                sv.save_res(confs['bias_path'], biases)
            return biases

        t_s = time.time()
        x_bias = cal_x_bias(top_mask, bottom_mask, 
                            confs['rect_top'], confs['rect_bottom'])
        t_e = time.time()
        print('00{0:d} bias compution along x axis completed in {1:.2f}s'\
              .format(i+1, t_e - t_s))
        single_bias['x'] = x_bias

        # cal y bias
        try:
            top_green = ld.load_img(top_name, cv2.IMREAD_COLOR, True, 1)
            bottom_green = ld.load_img(bottom_name, 
                                    cv2.IMREAD_COLOR, True, 1)
        except IOError:
            if save:
                sv.save_res(confs['bias_path'], biases)
            return biases

        t_s = time.time()
        y_bias = cal_y_bias(top_green, bottom_green,
                                confs['thre_feet'])
        t_e = time.time()
        print('00{0:d} bias compution along y axis completed in {1:.2f}s'\
              .format(i+1, t_e - t_s))
        single_bias['y'] = y_bias

        biases.append(single_bias)

    if save:
        sv.save_res(confs['bias_path'], biases)
    return biases
