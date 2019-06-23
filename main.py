# !/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 08:38:09
# @Description: 
"""

import time

import conf
import findsame
import segment
import calbias
import judge
import cover

def main():
    confs = conf.configure()
    same = findsame.find_same(confs, save=True)
    masks = segment.segment_gray(confs, same, save=True)
    biases = calbias.cal_bias(confs, masks, same, save=True)
    above = judge.judge_above(confs, masks, save=True)
    cover.cover_all(confs, above, biases, masks)

if __name__ ==  '__main__':
    t_s = time.time()
    main()
    t_e = time.time()
    print('Program completes in {0:.2f}s'.format(t_e - t_s))
