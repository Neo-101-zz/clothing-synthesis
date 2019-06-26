# !/usr/bin/env python

"""Main function to synthesize top and bottom into one image."""

import cv2

import conf as cf
import outfit as ot
import findsame as fs

def main():
    """Main function."""
    # Configure parameters for clothing synthesis
    confs = cf.configure()
    # Create outfit objects
    outfits = [ot.Outfit(path[0], path[1], path[3])
              for path in confs['input_path']]
    # Delete outfits that without top imag
    outfits = [outfit for outfit in outfits if hasattr(outfit, 'top')]
    # Find the same tops and bottoms between different outfits
    fs.find_same(outfits)
    print('Finding same completed.')

    for i, outfit in enumerate(outfits):
        # Find same tops and bottoms
        same = outfit.same
        with open(confs['same_path'], 'a') as f:
            f.write(str(same))
        # Segment top
        if same[0] != same[1]:
            outfit.top_mask = outfits[same[1]].top_mask
            cv2.imwrite(confs['mask_path'][i][0], outfit.top_mask)
        else:
            outfit.segment('top', confs['seed_top'],
                           confs['thre_top'], confs['rect_top'],
                           confs['mask_path'][i][0])
        # Segment bottom
        if same[0] != same[2]:
            outfit.bottom_mask = outfits[same[2]].bottom_mask
            cv2.imwrite(confs['mask_path'][i][1], outfit.bottom_mask)
        else:
            outfit.segment('bottom', confs['seed_bottom'],
                           confs['thre_bottom'], confs['rect_bottom'],
                           confs['mask_path'][i][1])
        # Segment input4
        outfit.segment('input4', confs['seed_input4'],
                       confs['thre_input4'], confs['rect_top'],
                       confs['mask_path'][i][3])
        print('{0:d} segmentation completed.'.format(i+1))
        # Compute realtively position difference
        if same[0] != same[1] and same[1] == same[2]:
            outfit.diff = outfits[same[1]].diff
        else:
            outfit.cpt_diff(confs['rect_top'], confs['rect_bottom'],
                            confs['thre_feet'])
        with open(confs['diff_path'], 'a') as f:
            f.write(str(outfit.diff))
        print('{0:d} diff computation completed.'.format(i+1))
        # Judge whether top or bottom is above
        outfit.judge_above(confs['waist_line'], confs['above_path'])
        print('{0:d} match judgement completed.'.format(i+1))
        # Generate output
        outfit.gen_res(confs['output_path'][i])
        print('{0:d} output completed.'.format(i+1))

if __name__ ==  '__main__':
    main()
