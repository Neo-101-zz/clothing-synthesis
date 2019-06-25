# !/usr/bin/env python

"""Compare input images of different outfits to find same tops and
bottoms.
"""

import time

import cv2

import clothsyn.loadimg as ld

def is_same(img_1, img_2):
    """Figure out whether two images are the same or not.

    Parameters
    ----------
    img_1 : numpy.ndarray
        One image (color).
    img_2 : numpy.ndarray
        Another image (color).

    Returns
    -------
    bool
        True if `img_1` is the same with `img_2`, False otherwise.

    """
    # compare two images' shape
    if img_1.shape == img_2.shape:
        difference = cv2.subtract(img_1, img_2)
        b, g, r = cv2.split(difference)
        if (cv2.countNonZero(b) == 0 and
            cv2.countNonZero(g) == 0 and
            cv2.countNonZero(r) == 0):
            # b, g, r channels of two imgs are equal
            return True

        return False

def find_same(outfits):
    """Find the same tops and bottoms between outfits.

    Parameters
    ----------
    outfits : list of Outfit
        See the Oufit class.

    Returns
    -------
    list of ints
        List of 3 ints.  same[0] is the index of target outfit itself.
        same[1] and same[2] is the index of outfit which has the same top
        and the same bottom respectively before target outfit in
        `outfits`.  same[1] and same[2] is equal to same[0] if there is no
        outfit which has the same top and bottom before in `outfits`.

    """
    t_s = time.time()
    for i in range(len(outfits)):
        top_same = bottom_same = i
        for j in range(i):
            if (top_same == i and
                is_same(outfits[i].top, outfits[j].top)):
                top_same = j
            if (bottom_same ==i and
                is_same(outfits[i].bottom, outfits[j].bottom)):
                bottom_same = j
        outfits[i].same = [i, top_same, bottom_same]
