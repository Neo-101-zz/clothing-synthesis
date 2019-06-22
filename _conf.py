import os

def configure():
    datasets_num = 8
    inputs_num = 4
    input_path_prefix = './input/'
    output_path_prefix = './output/'
    analysis_path_prefix = './analysis/'
    # make dirs
    if not os.path.exists(output_path_prefix):
        os.system('mkdir ' + output_path_prefix)
    if not os.path.exists(analysis_path_prefix):
        os.system('mkdir ' + analysis_path_prefix)
    mask_path_prefix = analysis_path_prefix + 'mask/'
    same_path = analysis_path_prefix + 'same.txt'
    bias_path = analysis_path_prefix + 'bias.txt'
    above_path = analysis_path_prefix + 'above.txt' 

    # generate paths 
    input_path = []
    mask_path = []
    output_path = []
    for i in range(datasets_num):
        input_path_set = []
        mask_path_set = []
        for j in range(inputs_num):
            input_name = '{0}00{1:d}-input{2:d}.jpg'.format(
                         input_path_prefix, i+1, j+1)
            mask_name = '{0}00{1:d}-input{2:d}_mask.jpg'.format(
                         mask_path_prefix, i+1, j+1)
            input_path_set.append(input_name) 
            mask_path_set.append(mask_name)
        input_path.append(input_path_set)
        mask_path.append(mask_path_set)
        output_name = '{0}00{1:d}-output.jpg'.format(
                      output_path_prefix, i+1)
        output_path.append(output_name)

    seed_top = [
        0.63150289017341,
        0.168509615384615,
    ]
    seed_input4 = [
        0.544075144508671,
        0.277403846153846,
    ]
    seed_bottom = [0.5248, 0.440]

    thre_top = 100
    thre_input4 = 20
    thre_bottom = 90
    thre_feet = 200

    rect_top = [
        0.180635838150289,      # left
        0.048076923076923,      # top
        0.794797687861272,      # right
        0.649038461538462,      # bottom
    ]
    rect_bottom = [
        0.180635838150289,      # left
        0.240384615384615,      # top
        0.794797687861272,      # right
        0.919471153846154,      # bottom
    ]
    waist_line = [
        0.469653179190751,      # left
        0.596098265895954,      # right
        0.360576923076923,      # height
    ]
    confs = {}

    confs['datasets_num'] = datasets_num
    confs['inputs_num'] = inputs_num
    confs['input_path'] = input_path 
    confs['mask_path'] = mask_path
    confs['same_path'] = same_path
    confs['bias_path'] = bias_path
    confs['above_path'] = above_path
    confs['output_path'] = output_path
    confs['seed_top'] = seed_top
    confs['seed_input4'] = seed_input4
    confs['seed_bottom'] = seed_bottom
    confs['thre_top'] = thre_top
    confs['thre_input4'] = thre_input4
    confs['thre_bottom'] = thre_bottom
    confs['thre_feet'] = thre_feet
    confs['rect_top'] = rect_top
    confs['rect_bottom'] = rect_bottom
    confs['waist_line'] = waist_line

    return confs
