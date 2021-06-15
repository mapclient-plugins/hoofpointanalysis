'''
Created on Jun 24, 2015

@author: hsorby
'''
from math import pi, acos

import numpy as np

from .vectorops import sub, dot
from .vectorops import magnitude


class PointAnalyzer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def analyze(self, pts):
        if len(pts) != 7:
            return None

        pts = self._sort(pts)
        sagittal_ridge_angle = self._calculateSagittalRidgeAngle(pts)
        ridge_height = self._calculateRidgeHeight(pts)

        return sagittal_ridge_angle, ridge_height

    def _calculateRidgeHeight(self, pts):
        p4 = pts.pop(3)
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        f = np.polyfit(x, y, 1)
        mid_y = f[0] * p4[0] + f[1]

        return p4[1] - mid_y

    def _calculateSagittalRidgeAngle(self, pts):
        pt4 = pts[3]
        pt3 = pts[2]
        pt5 = pts[4]

        v1 = sub(pt4, pt3)
        v2 = sub(pt4, pt5)

        theta = acos(dot(v1, v2) / (magnitude(v1) * magnitude(v2)))

        return theta * 180.0 / pi

    def _sort(self, pts):
        if len(pts) > 2:
            copy_pts = pts[:]
            d = [0.0, 1.0]
            pt1 = copy_pts.pop(0)
            pt2 = copy_pts.pop(0)
            ab = sub(pt2, pt1)
            dot_ab = dot(ab, ab)
            while len(copy_pts):
                pt = copy_pts.pop(0)
                ac = sub(pt, pt1)
                dot_ac = dot(ac, ab)
                value = dot_ac / dot_ab
                d.append(value)

            r = sorted((e, i) for i, e in enumerate(d))

            return [pts[j] for _, j in r]

        return pts
