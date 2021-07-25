#!/usr/bin/python

# jk 2.3.2018

from __future__ import print_function

import ROOT

from math import fabs, pow, sqrt

"""
source:
https://root.cern.ch/root/html524/TMath.html

Student:
http://www.sjsu.edu/faculty/gerstman/StatPrimer/
http://onlinestatbook.com/2/estimation/t_distribution.html
http://www.sjsu.edu/faculty/gerstman/StatPrimer/t-table.pdf
http://onlinestatbook.com/2/calculators/t_dist.html
https://en.wikipedia.org/wiki/Student%27s_t-distribution
https://root.cern.ch/root/html524/TMath.html#TMath:StudentI

"""

print('Checks:')
nsigs = [1, 2, 3, 5]
sigmas = [1., 5., 10.]
for sigma in sigmas:
    print('Sigma: {:}'.format(sigma))
    for n in nsigs:
        shift = n*sigma
        pvalGaus = ROOT.TMath.Erfc(shift/sigma/sqrt(2.))
        print('n={:}: pval={:1.9f} 1-p={:1.9f}'.format(n, pvalGaus, 1.-pvalGaus) )


data = [
    # 7 TeV sigma(pp->X)=95.35 \pm 0.38(stat.) \pm 1.25(exp.) \pm 0.37(extr.) mb
    # https://arxiv.org/abs/1408.5778
    [95.35, 0.38, 1.25, 0.37],
    # 8 TeV :  sigma(pp->X)=96.07 \pm 0.18(stat.) \pm 0.85(exp.) \pm 0.31(extr.) mb
    # https://arxiv.org/abs/1607.06605
    [ 96.07, 0.18, 0.85, 0.31 ]
]

print('ALFA comparison:')

diff = fabs(data[0][0] - data[1][0])

stat = sqrt( pow(data[0][1],2) + pow(data[1][1],2.))
sig = diff/stat
pvalGaus_stat = ROOT.TMath.Erfc(sig/sqrt(2.))
probChi2_stat = ROOT.TMath.Prob(pow(sig,2),1)
pvalStudent_stat = 2*(1. - ROOT.TMath.StudentI(sig,1))

statsyst = sqrt( pow(stat,2) + pow(data[0][2],2) + pow(data[1][2],2))
sig = diff/statsyst
pvalGaus_statsyst = ROOT.TMath.Erfc(sig/sqrt(2.))
probChi2_statyst = ROOT.TMath.Prob(pow(sig,2),1)
pvalStudent_statsyst = 2*(1. - ROOT.TMath.StudentI(sig,1))


#print('Stat+syst errors: {:f1.2} {:1.2f}'.format())

print('Significance in terms of stat:      {:2.2f}, gaussian p-val: {:1.3f}, 1-p={:1.3f}, chi2 p-val: {:1.5f}, p-val Student: {:1.3f}'.format(diff/stat, pvalGaus_stat, 1-pvalGaus_stat, probChi2_stat, pvalStudent_stat) )
print('Significance in terms of stat+syst: {:2.2f}, gaussian p-val: {:1.3f}, 1-p={:1.3f}, chi2 p-val: {:1.5f}, p-val Student: {:1.3f}'.format(diff/statsyst, pvalGaus_statsyst, 1-pvalGaus_statsyst, probChi2_statyst, pvalGaus_statsyst) )
