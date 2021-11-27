#!/usr/bin/python

import ROOT
import sys, os

#from myAll import *
from MakeCorrTools import *

N = 16


        

#########################################
#########################################
#########################################

#
# DATA 2015 !!!
#

spotreba = [ [ 'Zdarilova', [11, 7, 5.9, 6.4, 8.2, 3.9, 5.35, 7.07, 7.18, 5.6, 7.5] ],
             [ 'Skacelik', [9.6, 4.1, 5.7, 1.4, 0, 0, 0, 0, 0.60, 5.1, 4.9] ],
             [ 'Kvitovi', [24.4, 13.8, 13.2, 5.4, 9.7, 14, 11.47, 12.73, 13.59, 11.56, 13.05] ],
             [ 'Koldas', [9.6, 4.9, 4.7, 7.1, 5.3, 9.4, 4.59, 3.91, 4.40, 4.8, 3.9] ],
             [ 'Koutni', [16, 8.8, 8, 7.2, 9, 8, 9.31, 8.89, 8.76, 8.08, 8.86] ],
             [ 'Zborilovi', [11, 5, 6, 7, 6, 8, 5, 6, 5, 5.50, 6.] ],
             [ 'Nemeckova', [15, 6.5, 6, 5.9, 8.1, 5.3, 5.05, 5.40, 4.45, 4.3, 2.4] ],
             [ 'Salkova', [3.9, 1.7, 2, 1.9, 2.4, 2.2, 2.54, 2.04, 3.98, 2.47, 2.27] ],

             [ 'Kusnikovi', [16.4, 8.1, 7.9, 7.5, 8, 6, 9.67, 9.6, 10.04, 7.97, 7.02] ],
             [ 'Horylova', [12.6, 7.4, 7, 8, 8, 10, 9.63, 8.07, 8, 5.3, 5.] ],
             [ 'Navratilovi', [13.1, 5.4, 7.7, 3.5, 4.1, 7.5, 5.78, 6.23, 7.46, 6.07, 7.08] ],
             [ 'Dvorakova', [9, 6.2, 4.3, 4.2, 4.3, 4.1, 4.3, 3.7, 3.2, 2.8, 2.1] ],
             [ 'Leibnerovi', [12.5, 7, 6, 6, 6, 8, 8.41, 5.79, 6.4, 8., 7.] ],
             [ 'Sommerova', [3, 2, 2, 2.2, 2.5, 4.3, 1.53, 2.47, 1, 2.6, 2.1] ],
             [ 'Dolezel', [23.1, 12.8, 12, 12.5, 13, 11.4, 11.26, 10.94, 12, 14.2, 9.8] ],
             [ 'Haluza/Hamplova', [4.8, 2.2, 3.3, 2.9, 3.1, 2.9, 2.44, 2.56, 2.80, 2., 2.8 ] ],

             [ 'Uklid', [0.13, 0.17, 0.17, 0.14, 0.10, 0.18, 0.12, 0.12, 0.15, 0.13, 0.10] ], # LAST CCA!
             [ 'Suma', [] ],
             [ 'Hlavni', [206, 109, 108, 97, 101, 107, 107, 101, 104, 101, 101] ],
]

# print lengths:
for item in spotreba:
    print(item[0], len(item[1]))

# divide first by 2:
for item in spotreba:
    if len(item[1]) > 0:
        item[1][0] = item[1][0] / 2.
    
# compute the sum:

for im in range(0,len(spotreba[0][1])):
    sum = 0.
    for iu in range(0,len(spotreba)-2):
        sum = sum + spotreba[iu][1][im]
    spotreba[-2][1].append(sum)

print(spotreba)

#Compute the diff
diff = []
for im in range(0,len(spotreba[0][1])):
    sum =  spotreba[-2][1][im]
    hlavni = spotreba[-1][1][im]
    idiff = hlavni - sum
    diff.append(idiff)
spotreba.append(['Rozdil', diff])
print(diff)

print(spotreba)

histo = Make2D(spotreba, len(spotreba)-4, 'Spotreba', 'mesice 2015')
histoAll = Make2D(spotreba, len(spotreba), 'SpotrebaAll')

Cov = MakeCov(histoAll)
Corr = MakeCorr(Cov)

grs = []
for i in range(0, len(spotreba)):
    gr = MakeGraph(spotreba, i)
    grs.append(gr)


#############################
# Draw:

can = ROOT.TCanvas('Voda', 'Voda', 0, 0, 1000, 1000)
objs.append(can)
can.Divide(2,2)
can.cd(1)
#ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()
histo.Draw("colz")

can.cd(2)
leg = ROOT.TLegend(0.75, 0.17, 0.98, 0.90)
tmp = ROOT.TH2D('tmp', 'tmp;mesice 2015', 14, 0, 14, 100, 0, 15.)
tmp.SetStats(0)
objs.append(tmp)
tmp.Draw()
opt = 'PL'
for gr in grs:
    if gr.GetName().find('Sum') >= 0 or gr.GetName().find('Hlavni') >= 0:
        continue
    gr.Draw(opt)
    opt = 'PL'
    leg.AddEntry(gr, gr.GetName().replace('_gr', ''), 'PL')
leg.Draw()

can.cd(3)
Cov.Draw('colz')
can.cd(4)
Corr.Draw('colz')

ROOT.gApplication.Run()
