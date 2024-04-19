#!/usr/bin/python

# jk 24-25.2.2024

import numpy as np
from matplotlib import pyplot as plt

from math import sqrt, pow, fabs
import sys, os

######################################################################
class myMoments():
    def __init__(self, x, ex = []):
        self.x = x
        self.ex = ex
        self.moments = {}
        if len(x) > 0:
            self.moments['mean'] = sum(x) / len(x)
        if len(x) > 1:
            self.moments['var'] = sum([ pow(d - self.moments['mean'],2) for d in x]) / (len(x) - 1)
            if self.moments['var'] > 0:
                self.moments['sigma'] = sqrt(self.moments['var'])
                self.moments['meanerr'] = self.moments['sigma'] / sqrt(len(x))
    def mean(self):
        return self.moments['mean']
    def var(self):
        return self.moments['var']
    def sigma(self):
        return self.moments['sigma']
    def meanerr(self):
        return self.moments['meanerr']
    def n(self):
        return len(self.x)
    def x(self):
        return self.x
    def ex(self):
        return self.ex
    def xsq(self):
        return  [ pow(d,2) for d in x]

# to add: a test!

