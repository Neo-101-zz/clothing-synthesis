from conf import *
from find_same import *
from segment import *
from cal_offset import *
from judge import *
from cover import *
import time

def main():
	confs = conf()
	same = find_same(confs)
	masks = segment_gray(confs, same, save=False)
	offsets = cal_all_offset(confs, masks, same)
	above = judge(confs, masks)
	cover_all(confs, above, offsets, masks)

if __name__ ==  '__main__':
	t_s = time.time()
	main()
	t_e = time.time()
	print('Program completes in ' + str(t_e - t_s))
