# !/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 08:36:10
# @Description: 
"""

import numpy as np

def gray_region_growing(img, seed_rate, threshold, rect):
    img = np.float32(img)
    row, col = img.shape[0:2]
    seed = [0, 0]
    seed[0] = int(row * seed_rate[1])  # y 
    seed[1] = int(col * seed_rate[0])  # x
    reg = np.zeros((row, col), np.float32)
    orient = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    growX = []
    growY = []
    growX.append(seed[1]) 
    growY.append(seed[0]) 
    check = np.zeros((row, col))
    left = rect[0] * col
    top = rect[1] * row
    right = rect[2] * col
    bottom = rect[3] * row

    label = 255 
    reg[seed[0], seed[1]] = label
    size = 1
    mean_reg = img[seed[0], seed[1]]

    while(growX != []):
        curX = growX.pop(0)
        curY = growY.pop(0)
        sumTemp = 0
        count = 0

        for m in range(4):
            tempY = curY + orient[m][0]
            tempX = curX + orient[m][1]
            if (tempY < bottom and tempY >= top and 
                tempX < right and tempX >= left):
                # calculate the distance between pixel and region
                dist = abs(img[tempY, tempX] - mean_reg)
                if dist < threshold and check[tempY, tempX] == 0:
                    # update the region
                    check[tempY, tempX] = 1
                    reg[tempY, tempX] = label
                    growY.append(tempY)
                    growX.append(tempX)
                    sumTemp += img[tempY, tempX]
                    count += 1

        mean_reg = (mean_reg * size + float(sumTemp)) \
                 / (size + count)
        size += count

    reg = np.uint8(reg)

    return reg
