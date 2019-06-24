#! /usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 00:47:37
# @Description: 
"""

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
