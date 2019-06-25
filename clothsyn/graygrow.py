# !/usr/bin/env python

"""Segment gray image by region growing."""

import numpy as np

def gray_region_growing(img, seed_rate, thre, rect):
    """Region growing based on gray image.

    Parameters
    ----------
    img : numpy.ndarray
        Gray image to be segmented.
    seed_rate : list of floats
        Seed point for inital growing.  A list of 2 floats in form of
        [x_ratio, y_ratio].  x_ratio is the ratio of seed's x coordinate
        to image's width.  y_ratio is the ratio of seed's y coordinate
        to image's height.
    thre : int
        Threshold for growing termination.
    rect : list of floats
        Rectangle boundary of top or bottom to be extracted.  A list of
        4 floats in form of [left/width, top/height, right/width,
        bottom/height].  left and top is the x coordinate and y coordinate
        of rectangle's top-left point, respectively.  right and bottom is 
        the x coordinate and y coordinate of rectangle's bottom-right
        point, respectively.  width and height is the amount of image's 
        pixels along x axis and y aixs, respectively.

    Returns
    -------
    reg : numpy.ndarray
        Two-value gray mask of top or bottom.  In the mask, value 255
        represents the region of top or bottom, while value 0 represents
        the region of background.

    """
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
