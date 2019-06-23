#! /usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 00:44:19
# @Description: 
"""

import os

import cv2

def load_img(img_path, flag, decom, chan):
    if os.path.exists(img_path):    
        img = cv2.imread(img_path, flag)
        if decom == True:
            return img[:, :, chan]
        else:
            return img
    else:
        print(img_path + ' does not exists')
        raise IOError   
