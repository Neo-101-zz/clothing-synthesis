import time

import cv2

import loadimg as ld
import saveres as sv

def is_same(img_now, img_pre):
    # compare two images' shape
    if img_now.shape == img_pre.shape:
        difference = cv2.subtract(img_now, img_pre)
        b, g, r = cv2.split(difference)
        if (cv2.countNonZero(b) == 0 and 
            cv2.countNonZero(g) == 0 and 
            cv2.countNonZero(r) == 0):
            # b, g, r channels of two imgs are equal
            return True

        return False

def find_same(confs, save):
    t_s = time.time()
    same = []
    for i in range(confs['datasets_num']):
        one_dataset = []
        for j in range(confs['inputs_num']):
            find_same = False
            # find same imgs
            for k in range(i):
                img_now_name = confs['input_path'][i][j] 
                img_pre_name = confs['input_path'][k][j] 
                try:
                    img_now = ld.load_img(img_now_name, 
                                       cv2.IMREAD_COLOR, 
                                       False, 0)
                    img_pre = ld.load_img(img_pre_name,
                                       cv2.IMREAD_COLOR,
                                       False, 0)
                except IOError:
                    if save:
                        sv.save_res(confs['same_path'], same)
                    t_e = time.time()
                    print('find same completed in {0:.2f}s'.format(t_e - t_s))
                    return same
                if is_same(img_now, img_pre):
                    find_same = True
                    one_dataset.append(k)
                    print('{0} and {1} are completely equal.'\
                          .format(img_now_name, img_pre_name))
                    break
            if not find_same: 
                one_dataset.append(i)

        same.append(one_dataset)

    t_e = time.time()
    print('find same completed in {0:.2f}s'.format(t_e - t_s))

    if save:
        sv.save_res(confs['same_path'], same)
    return same
