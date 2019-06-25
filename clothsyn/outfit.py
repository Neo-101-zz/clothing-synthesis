#!/usr/bin/env python

"""Represent outfit and synthesize clothing."""

import cv2

import clothsyn.loadimg as ld
import clothsyn.graygrow as ggrow
import clothsyn.cptdiff as cb
import clothsyn.judge as je
import clothsyn.cover as cr

class Outfit():
    """Represent outfit and operate it to synthesize top and bottom into
    a outfit image.

    Parameters
    ----------
    top_path : str
        Path of top image (input1.jpg).
    bottom_path : str
        Path of bottom image (input2.jpg).
    input_path : str
        Path of input4 image (input4.jpg).

    """
    def __init__(self, top_path, bottom_path, input4_path):
        try:
            self.top = ld.load_img(top_path, cv2.IMREAD_COLOR, False, 0)
            self._top_r = self.top[:,:,2]
            self._top_g = self.top[:,:,1]
            self.bottom = ld.load_img(bottom_path, cv2.IMREAD_COLOR,
                                       False, 0)
            self._bottom_r = self.bottom[:, :, 2]
            self._bottom_g = self.bottom[:, :, 1]
            self._input4_b = ld.load_img(input4_path, cv2.IMREAD_COLOR,
                                        True, 0)
        except IOError:
            return

    def segment(self, cloth, seed, thre, rect, save_path):
        """Segment a image into a two-value mask.  See clothsyn.graygrow.

        Parameters
        ----------
        cloth : str
            Type of image.  'top' for top image, 'bottom' for
            bottom image and 'input_4' for input4 image.
        seed : list of floats
            Seed point for region growing.
        thre : list of floats
            Rectangle boundary for region growing.
        save_path : str
            Path of mask to be saved.

        Returns
        -------
        None
            Nothing returned by this function.

        """
        if cloth == 'top':
            res = self.top_mask = ggrow.gray_region_growing(
                self._top_r, seed, thre, rect)
        elif cloth == 'bottom':
            res = self.bottom_mask = ggrow.gray_region_growing(
                self._bottom_r, seed, thre, rect)
        elif cloth == 'input4':
            res = self.input4_mask = ggrow.gray_region_growing(
                self._input4_b, seed, thre, rect)
        else:
            print('Segment error: wrong input of cloth.')
        if len(save_path) > 0:
            cv2.imwrite(save_path, res)

    def cpt_diff(self, rect_top, rect_bottom, thre_feet):
        """Compute the relative position difference of model with
        respect to camera between input1 and input2.
        See clothsyn.cptdiff.

        Parameters
        ----------
        rect_top : list of floats
            Rectangle boundary of top.
        bottom_top : list of floats
            Rectangle boundary of bottom.
        thre_feet : int
            Threshold for computing relative position difference along
            y axis.

        Returns
        -------
        None
            Nothing returned by this function.

        """
        self.diff = {}
        self.diff['x'] = cb.cpt_x_diff(self.top_mask, self.bottom_mask,
                                       rect_top, rect_bottom)
        self.diff['y'] = cb.cpt_y_diff(self._top_g, self._bottom_g,
                                       thre_feet)

    def judge_above(self, waist_line):
        """Judge whether top is weared into bottom or not.
        See clothsyn.judge.

        Parameters
        ----------
        waist_line : list of floats
            Line at the height of waist for judgement.

        Returns
        -------
        None
            Nothing returned by this function.

        """
        line, length = je.extract(self.input4_mask, waist_line)
        if je.top_above(line, length):
            self.above = 'top'
        else:
            self.above = 'bottom'

    def gen_res(self, output_path):
        """Generate the final result of clothing synthesis.
        See clothsyn.cover.

        Parameters
        ----------
        output_path : str
            Path to save the final result.

        Returns
        -------
        None
            Nothing returns by this function.

        """
        self._output = cr.cover_single(self.top, self.bottom,
                                       self.top_mask, self.bottom_mask,
                                       self.above, self.diff)
        cv2.imwrite(output_path, self._output)
