#! /usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 00:47:06
# @Description: 
"""

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

def cpt_x_bias(top_mask, bottom_mask, top_rect, bottom_rect):
    top_cen_axis = get_axis(top_mask, top_rect)
    bottom_cen_axis = get_axis(bottom_mask, bottom_rect)
    # 1.25 is an empirical coefficient to precisely adjust the
    # bias between top and bottom
    x_bias = int((float(bottom_cen_axis - top_cen_axis)) * 1.25)

    return x_bias

def cpt_y_bias(top, bottom, thre):
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
