#! /usr/bin/env python

"""Synthesize top and bottom into output image."""

import numpy as np

def cover_single(top, bottom, mask_top,
                 mask_bottom, above, diff):
    """Cover top over bottom or bottom over top.

    Parameters
    ----------
    top : numpy.ndarray
        Top image (color).
    bottom : numpy.ndarray
        Bottom image (color).
    mask_top : numpy.ndarry
        Two-value gray mask of top.
    mask_bottom : numpy.ndarray
        Two-value gray mask of bottom.
    above : str
        'top' if top is above bottom, 'bottom' otherwise.
    diff : dict of ints
        Relative position differnce in form of {'x': x_diff, 'y': y_diff}.
        x_diff and y diff is difference along x axis and y axis, 
        respectively.

    Returns
    -------
    res : numpy.ndarray
        Result of clothing synthesis.

    """
    row, col = top.shape[0:2]
    res = np.zeros((row, col, 3), np.float32)
    # Use input1 as background
    for x in range(col):
        for y in range(row):
            if above == 'top':
                # Through observation, the output image is based on
                # top image. The poisition of model to the model in
                # the top image is the same as output image.  
                # So use top image as background.
                if (x + diff['x'] < col and
                    y + diff['y'] < row and
                    mask_top[y, x] == 0 and
                    mask_bottom[y+diff['y'], x+diff['x']] == 255):
                    # Draw the part that top does not cover the bottom
                    res[y, x] = bottom[y+diff['y'], x+diff['x']]
                else:
                    # Copy the rest part of top img because top image
                    # is used as backgound of output image.
                    res[y, x] = top[y, x]
            elif above == 'bottom':
                if (x + diff['x'] < col and
                    y + diff['y'] < row and
                    mask_bottom[y+diff['y'], x+diff['x']] == 255):
                    # Draw the bottom
                    res[y, x] = bottom[y+diff['y'], x+diff['x']]
                else:
                    # Copy the top
                    res[y, x] = top[y, x]
    return res
