import time

from conf import *
from find_same import *
from segment import *
from cal_offset import *
from judge import *
from cover import *

def main():
    confs = conf()
    same = find_same(confs, save=True)
    masks = segment_gray(confs, same, save=True)
    offsets = cal_all_offset(confs, masks, same, save=True)
    above = judge(confs, masks, save=True)
    cover_all(confs, above, offsets, masks)

if __name__ ==  '__main__':
    t_s = time.time()
    main()
    t_e = time.time()
    print('Program completes in ' + str(t_e - t_s))
