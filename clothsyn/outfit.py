#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Jingze Lu
# @Created Time : 2019-06-22 15:33:26
# @Description : 
"""

import cv2

import loadimg as ld
import graygrow as ggrow
import cptbias as cb
import judge as je
import cover as cr

class Outfit():
    
    def __init__(self, top_path, bottom_path, input4_path):
        try:
            self.top = ld.load_img(top_path, cv2.IMREAD_COLOR, False, 0)
            self._top_r = self.top[:,:,2]
            self._top_g = self.top[:,:,1]
            self.bottom = ld.load_img(bottom_path, cv2.IMREAD_COLOR,
                                       False, 0)
            self._bottom_r = self.bottom[:, :, 2]
            self._bottom_g = self.bottom[:, :, 1]
            self._input4_b = ld.load_img(input4_path, cv2.IMREAD_COLOR,
                                        True, 0)
        except IOError:
            return

    def segment(self, cloth, seed, thre, rect, save_path):
        if cloth == 'top':
            res = self.top_mask = ggrow.gray_region_growing(
                self._top_r, seed, thre, rect)
        elif cloth == 'bottom':
            res = self.bottom_mask = ggrow.gray_region_growing(
                self._bottom_r, seed, thre, rect)
        elif cloth == 'input4':
            res = self.input4_mask = ggrow.gray_region_growing(
                self._input4_b, seed, thre, rect)
        else:
            print('Segment error: wrong input of cloth.')
        if len(save_path) > 0:
            cv2.imwrite(save_path, res)

    def cpt_bias(self, rect_top, rect_bottom, thre_feet):
        self.bias = {}
        self.bias['x'] = cb.cpt_x_bias(self.top_mask, self.bottom_mask,
                                       rect_top, rect_bottom)
        self.bias['y'] = cb.cpt_y_bias(self._top_g, self._bottom_g,
                                       thre_feet)

    def judge_above(self, waist_line):
        line, length = je.extract(self.input4_mask, waist_line)
        if je.top_above(line, length):
            self.above = 'top'
        else:
            self.above = 'bottom'

    def gen_res(self, output_path):
        self._output = cr.cover_single(self.top, self.bottom,
                                       self.top_mask, self.bottom_mask,
                                       self.above, self.bias)
        cv2.imwrite(output_path, self._output)
