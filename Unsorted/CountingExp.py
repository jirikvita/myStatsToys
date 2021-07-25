#!/usr/bin/python

from math import *


def fact(k):
    f = 1
    if k < 2:
        return f
    for i in range(1,k+1):
        f=f*i
    return f


def Pois(k,nu):
    p = exp(-nu) * pow(nu,k) / fact(k)
    return p


def Sum(nu,k1,k2):
    sum = 0.
    for i in range(k1,k2+1):
        sum = sum+Pois(i,nu)
    return sum


nc=3

nub = 1.3
alfa = 1. - Sum(nub,0,nc-1)
print alfa

nus = 2
beta = Sum(nub+nus,0,nc-1)
print beta
print 1.-beta
