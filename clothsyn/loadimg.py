#! /usr/bin/env python

"""Load image with optional function of channel decomposition."""
import os

import cv2

def load_img(img_path, flag, decom, chan):
    """Load image with optional function of channel decomposition.

    Parameters
    ----------
    img_path : str
        Path of image.
    flag : str
        The way image should be read.  
        cv2.IMREAD_COLOR : Loads a color image. Any transparency of
        image will be neglected. It is the default flag.
        cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode.
        cv2.IMREAD_UNCHANGED : Loads image as such including alpha
        channel.
    decom : bool
        Whether to decomposite image or not.
    chan : int
        Channel to be extracted.
        Blue : 0, 
        Green : 1, 
        Red : 2.
    
    Returns
    -------
    img : numpy.ndarray
        Image loaded.

    """

    if os.path.exists(img_path):
        img = cv2.imread(img_path, flag)
        if decom:
            return img[:, :, chan]
        else:
            return img
    else:
        print(img_path + ' does not exists')
        raise IOError
