#!/usr/bin/python

# jiri kvita, 24.3.2017

#from myAll import *
import ROOT
#filename = ''
#rfile = ROOT.TFile(filename, 'read')


# people writing down rnadom numbers, the next one is usually larger if first was also large? Check;)

data = [ [89, 85], [26, 89], [79, 85], [92, 78], [26, 80], [53, 53], [19, 82], [99, 84], [59, 78],
         [85, 80], [45, 68], [80, 70], [19, 69], [78, 89], [11, 75], [16, 80], [7, 75], [56, 73],
         [9, 73], [24, 82], [6, 80], [14, 66], [9, 89], [78, 87], [62, 80], [15, 65], [4, 78], [2, 89],
]


gr = ROOT.TGraph()
histo = ROOT.TH2D("hcorr", "hcorr", 100, 0, 100, 69, 0, 91)

j = 0
for point in data:
    gr.SetPoint(j, point[0], point[1])
    histo.Fill(point[0], point[1])
    j=j+1

name='BiasCorr'
can = ROOT.TCanvas(name, name, 0, 0, 1200, 800)
can.Divide(2,1)
can.cd(1)
gr.SetMarkerStyle(20)
gr.SetMarkerColor(2)
gr.SetMarkerSize(1)
gr.Draw('AP')

can.cd(2)
histo.Draw('colz')
val = histo.GetCorrelationFactor()
print('Number of people responded  : %i' % (len(data),))
print('Correlation                 : %f' % (val,))

ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

ROOT.gApplication.Run()

