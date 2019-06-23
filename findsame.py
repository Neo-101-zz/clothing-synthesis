# !/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 16:22:44
# @Description: 
"""

import time

import cv2

import loadimg as ld
import saveres as sv

def is_same(img_now, img_pre):
    # compare two images' shape
    if img_now.shape == img_pre.shape:
        difference = cv2.subtract(img_now, img_pre)
        b, g, r = cv2.split(difference)
        if (cv2.countNonZero(b) == 0 and 
            cv2.countNonZero(g) == 0 and 
            cv2.countNonZero(r) == 0):
            # b, g, r channels of two imgs are equal
            return True

        return False

def find_same(outfits):
    t_s = time.time()
    for i in range(len(outfits)):
        top_same = bottom_same = i 
        for j in range(i):
            if (top_same == i and 
                is_same(outfits[i].top, outfits[j].top)):
                top_same = j 
            if (bottom_same ==i and
                is_same(outfits[i].bottom, outfits[j].bottom)):
                bottom_same = j 
        # i represents the index
        outfits[i].same = [i, top_same, bottom_same]
