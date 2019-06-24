#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Jingze Lu
# @Created Time : 2019-06-22 18:47:18
# @Description : 
    """

import timeit
import time

datasets_num = 8
inputs_num = 4
input_path_prefix = './input/'
output_path_prefix = './output/'

start = time.time()
for i in range(10000):
    for i in range(datasets_num):
        for j in range(inputs_num):
            input_name = input_path_prefix + '00' + str(i+1) \
                       + '-input' + str(j+1) \
                       + '.jpg'
end = time.time()
print(input_name)
print('plus con: ' + str(end-start))

start = time.time()
for i in range(10000):
    for i in range(datasets_num):
        for j in range(inputs_num):
            input_name = \
                    '{0}00{1:d}-input{2:d}.jpg'.format(
                        input_path_prefix, i+1, j+1)
end = time.time()
print(input_name)
print('format con: ' + str(end-start))
