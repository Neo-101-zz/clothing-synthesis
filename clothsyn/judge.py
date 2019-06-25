#! /usr/bin/env python

"""Judge whether top is waered into bottom or not with extracted waist 
line."""

def extract(mask, judge_line):
    """
    Extract waist line of mask.

    Parameters
    ----------
    mask : numpy.ndarray
        Mask of top or bottom.
    judge_line : list of floats
        Horizontal line for extract at the height of waist in form of
        [left_ratio, right_ratio, height_ratio].  left is the ratio of
        line's left endpoint's x coordinate to the width of image.  right
        is the ratio of line's right endpoint's x coordiante to the
        width of image.  height_ratio is the ratio of line's y coordinate
        to the height of image.

    Returns
    -------
    line : list of ints
        Extracted waist line.
    int
        Length of waist line.

    """
    row, col = mask.shape[0:2]
    left = int(judge_line[0] * col)
    right = int(judge_line[1] * col)
    height = int(judge_line[2] * row)

    line = []
    y = height

    for x in range(right-left):
        line.append(mask[y, x+left])

    return line, len(line)

def top_above(line, length):
    """
    Judge whether top is weared into bottom.

    Parameters
    ----------
    line : list of ints
        Extracted waist line.
    length : int
        Length of waist line.

    Returns
    -------
    bool
        True if top weared into bottom, False otherwise.

    """
    for i in range(length):
        if line[i] != 0: # top above
            return True
    return False # bottom above 
