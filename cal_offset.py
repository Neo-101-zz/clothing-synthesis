import os
import cv2
import time
from load_img import *

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

def cal_x_offset(top_mask, bottom_mask, top_rect, bottom_rect):
    top_cen_axis = get_axis(top_mask, top_rect)
    bottom_cen_axis = get_axis(bottom_mask, bottom_rect) 
    x_offset = int((float(bottom_cen_axis - top_cen_axis)) * 1.25) 

    return x_offset

def cal_y_offset(top, bottom, thre):
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

def cal_all_offset(confs, masks, same):
    offsets = []

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
                return offsets

        if top_bottom_same:
            single_offset = offsets[j]
            offsets.append(single_offset)
            continue

        single_offset = {}
        top_name = confs['img_names'][i][0]
        bottom_name = confs['img_names'][i][1]

        # cal x offset
        try:
            top_mask = masks[i]['1'] 
            bottom_mask = masks[i]['2'] 
        except IndexError:
            return offsets

        t_s = time.time()
        x_offset = cal_x_offset(top_mask, bottom_mask, 
                                confs['rect_top'], confs['rect_bottom'])
        t_e = time.time()
        print('00' + str(i+1) + ' x calculation completed in ' 
                   + str(t_e - t_s))
        single_offset['x'] = x_offset

        # cal y offset
        try:
            top_green = load_img(top_name, cv2.IMREAD_COLOR, True, 1)
            bottom_green = load_img(bottom_name, cv2.IMREAD_COLOR, True, 1)
        except IOError:
            return offsets

        t_s = time.time()
        y_offset = cal_y_offset(top_green, bottom_green, confs['thre_feet'])
        t_e = time.time()
        print('00' + str(i+1) + ' y calculation completed in ' 
                   + str(t_e - t_s))
        single_offset['y'] = y_offset

        offsets.append(single_offset)

    return offsets
