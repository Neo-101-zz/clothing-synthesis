#! /usr/bin/env python

import os

def configure():
    confs = {}

    outfits_num = int(input('Enter the number of outfits: '))
    confs['outfits_num'] = outfits_num
    confs['inputs_num'] = inputs_num = 4
    input_dir = '../input/'
    output_dir = '../output/'
    analysis_dir = '../analysis/'

    suffix = ['mask/', 'same.txt', 'diff.txt', 'above.txt']
    ans_path = (analysis_dir + s for s in suffix)
    mask_dir = next(ans_path)
    confs['same_path'] = same = next(ans_path)
    confs['diff_path'] = diff = next(ans_path)
    confs['above_path'] = above = next(ans_path)

    # Delete existed files
    for f in [same, diff, above]:
        if os.path.exists(f):
            os.system('rm ' + f)

    # Make directories
    for dir_ in [output_dir, analysis_dir, mask_dir]:
        if not os.path.exists(dir_):
            os.system('mkdir ' + dir_)

    confs['input_path'] = [[
        '{0}{1:d}-input{2:d}.jpg'.format(input_dir, i+1, j+1) \
        for j in range(inputs_num)] for i in range(outfits_num)]
    confs['mask_path'] = [[
        '{0}{1:d}-mask{2:d}.jpg'.format(mask_dir, i+1, j+1) \
        for j in range(inputs_num)] for i in range(outfits_num)]
    confs['output_path'] = [
        '{0}{1:d}-output.jpg'.format(output_dir, i+1) \
        for i in range(outfits_num)]

    confs['thre_top'] = 100
    confs['thre_input4'] = 20
    confs['thre_bottom'] = 90
    confs['thre_feet'] = 200

    row = 4160
    col = 2768
    confs['seed_top'] = [1748.0/col, 701.0/row]
    confs['seed_input4'] = [1506.0/col, 1154.0/row]
    confs['seed_bottom'] = [1453.0/col, 1830.0/row]
    # rect = [left, top, right, bottom]
    confs['rect_top'] = [500.0/col, 200.0/row, 2200.0/col, 2700.0/row]
    confs['rect_bottom'] = [500.0/col, 1000.0/row, 2200.0/col, 3825.0/row]
    # waist_line = [left, right, height]
    confs['waist_line'] = [1300.0/col, 1650.0/col, 1500.0/row]

    return confs
