# !/usr/bin/env python

"""Main function to synthesize top and bottom into one image."""

import cv2

import conf
import outfit as ot
import findsame as fs

def main():
    """Main function."""
    # Configure parameters for clothing synthesis
    confs = conf.configure()
    # Create outfit objects.
    #
    # Each object represents one group of input consists of 4 images:
    # input1.jpg: top image
    # input2.jpg: bottom image
    # input3.jpg: match of top and bottom (wear top into bottom or not)
    # input4.jpg: match of top and bottom (wear top into bottom or not)
    outfits = [ot.Outfit(path[0], path[1], path[3])
              for path in confs['input_path']]
    # Delete outfits that without top imag
    outfits = [outfit for outfit in outfits if hasattr(outfit, 'top')]
    # Find the same tops and bottoms between different outfits
    fs.find_same(outfits)
    print('Finding same completed.')

    for i, outfit in enumerate(outfits):
        # Segment top, bottom and input4 to extract their masks
        same = outfit.same
        # same is a 3 elements list.  See module findsame.
        #
        # same[0]: index of outfit itself
        # same[1]: index of outfit which has the same top
        # same[2]: index of outfit which has the same bottom
        #
        # same[1] and same[2] is equal to same[0] if there is no
        # outfit which has the same top and bottom before in the
        # list of outfits.
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
        # Compute bias
        if same[0] != same[1] and same[1] == same[2]:
            outfit.bias = outfits[same[1]].bias
        else:
            outfit.cpt_bias(confs['rect_top'], confs['rect_bottom'],
                            confs['thre_feet'])
        print('{0:d} bias computation completed.'.format(i+1))
        # Judge whether top or bottom is above
        outfit.judge_above(confs['waist_line'])
        print('{0:d} match judgement completed.'.format(i+1))
        # Generate output
        outfit.gen_res(confs['output_path'][i])
        print('{0:d} output completed.'.format(i+1))

if __name__ ==  '__main__':
    main()
