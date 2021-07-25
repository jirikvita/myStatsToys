#!/usr/bin/python

from math import *

def sig(k, delta, up):
    delta = fabs(delta)
    fact = sqrt(k*delta + pow(delta/2.,2))
    if up > 0:
        return fact + delta/2.
    else:
        return fact - delta/2.

def sig0(k, delta, up):
    fact = sqrt(k*delta)
    return fact
    
k = 5
print sig(k, 1., 1)
print sig(k, 1., -1)

print k+sig(k, 1., 1)
print k-sig(k, 1., -1)

print
print sig0(k, 1., 1)
print sig0(k, 1., -1)

print k+sig0(k, 1., 1)
print k-sig0(k, 1., -1)
