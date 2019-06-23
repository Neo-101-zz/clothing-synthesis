# !/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author: Jingze Lu
# @Created Time: 2019-06-23 16:13:37
# @Description: 
"""

import cv2

import conf
import outfit as ot
import findsame as fs

def main():
    confs = conf.configure()
    outfits = [ot.Outfit(path[0], path[1], path[3])
              for path in confs['input_path']]
    # find same input
    fs.find_same(outfits)
    print('Finding same completed.')
    for i, outfit in enumerate(outfits):
        # segment
        same = outfit.same
        if same[0] != same[1]:
            outfit.top_mask = outfits[same[1]].top_mask
            cv2.imwrite(confs['mask_path'][i][0], outfit.top_mask)
        else:
            outfit.segment('top', confs['seed_top'], 
                           confs['thre_top'], confs['rect_top'],
                           confs['mask_path'][i][0])
        if same[0] != same[2]:
            outfit.bottom_mask = outfits[same[2]].bottom_mask
            cv2.imwrite(confs['mask_path'][i][1], outfit.bottom_mask)
        else:
            outfit.segment('bottom', confs['seed_bottom'], 
                           confs['thre_bottom'], confs['rect_bottom'],
                           confs['mask_path'][i][1])
        outfit.segment('input4', confs['seed_input4'],
                       confs['thre_input4'], confs['rect_top'],
                       confs['mask_path'][i][3])
        print('{0:d} segmentation completed.'.format(i+1))
        # compute bias
        outfit.cpt_bias(confs['rect_top'], confs['rect_bottom'],
                        confs['thre_feet'])
        print('{0:d} bias computation completed.'.format(i+1))
        # judge whether top or bottom is above
        outfit.judge_above(confs['waist_line'])
        print('{0:d} match judgement completed.'.format(i+1))
        # generate output
        outfit.gen_res(confs['output_path'][i])
        print('{0:d} output completed.'.format(i+1))

if __name__ ==  '__main__':
    main()
