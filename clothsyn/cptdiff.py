#! /usr/bin/env python

"""Compute the relative position difference of model with
respect to camera between input1 and input2.
"""

def central_x(mask, rect):
    """Compute the x value of vertically central axis of top or bottom.

    Parameters
    ----------
    mask : numpy.ndarray
        Two-value mask of top image or bottom image.
    rect : list of floats
        Rectangle boundary of top image or bottom image.

    Returns
    -------
    axis : int
        x value of vertically central axis of top or bottom.

    """
    # There may be holes in the mask.  So boundingRect() may return
    # the boudning of a hole rather than the whole bounding of top or
    # bottom.
    row, col = mask.shape[0:2]
    left = col-1
    right = 0
    left_bound = int(rect[0] * col)
    right_bound = int(rect[2] * col)
    top_bound = int(rect[1] * row)
    bottom_bound = int(rect[3] * row)

    for y in range(top_bound, bottom_bound):
        for x in range(left_bound, right_bound):
            if mask[y, x] == 0:
                continue
            else:
                if x < left:
                    left = x
                if x > right:
                    right = x

    axis = int((left + right) / 2.0)

    return axis

def cpt_x_diff(top_mask, bottom_mask, top_rect, bottom_rect):
    """Compute difference along x axis.

    Parameters
    ----------
    top_mask : numpy.ndarray
        Mask of top .
    bottom_mask : numpy.ndarray
        Mask of bottom .
    top_rect : list of floats
        Rectangle boundary of top.
    bottom_rect : list of floats
        Rectangle boundary of bottom.

    Returns
    -------
    x_diff : int
        Difference along x axis.

    """
    top_cen_axis = central_x(top_mask, top_rect)
    bottom_cen_axis = central_x(bottom_mask, bottom_rect)
    # 1.25 is an empirical coefficient to precisely adjust the
    # diff between top and bottom
    x_diff = int((float(bottom_cen_axis - top_cen_axis)) * 1.25)

    return x_diff

def cpt_y_diff(top, bottom, thre):
    """Compute difference along y axis.

    Parameters
    ----------
    top : 
        Top image (green channel).
    bottom : 
        Bottom image (green channel).
    thre : 
        Threshold for distinguish model's feet from background.

    Returns
    -------
    y_diff : int
        Difference along y axis.

    """

    # Search from bottom
    row, col = top.shape[0:2]
    feet_top = 0
    feet_bottom = 0

    for y in range(row):
        for x in range(col):
            # Search model's feet in top image
            if feet_top == 0 and top[row-1-y, x] > thre:
                feet = True
                # Verify the feet
                for i in range(20):
                    if x+i < col and top[row-1-y, x+i] > thre:
                        pass
                    else:
                        feet = False
                if feet:
                    feet_top = row-1-y
            # Search model's feet in bottom image
            if feet_bottom == 0 and bottom[row-1-y, x] > thre:
                feet = True
                # Verify the feet
                for i in range(20):
                    if x+i < col and bottom[row-1-y, x+i] > thre:
                        pass
                    else:
                        feet = False
                if feet:
                    feet_bottom = row-1-y
            # End if have found both feet in top and bottom image
            if feet_top > 0 and feet_bottom > 0:
                y_diff = feet_bottom - feet_top
                return y_diff

    y_diff = feet_bottom - feet_top
    return y_diff
