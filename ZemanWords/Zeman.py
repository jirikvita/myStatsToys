#!/usr/bin/python
# Wed 30 Oct 08:15:56 CET 2019
# jk

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
    try:
        # options that require an argument should be followed by a colon (:).
        opts, args = getopt.getopt(argv[2:], 'hbt:', ['help','batch','tag='])

        print('Got options:')
        print(opts)
        print(args)
    except getopt.GetoptError:
        print('Parsing...')
        print ('Command line argument error!')
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.format(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.format(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.format(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.format(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))


    # Projevy prezidenta Milose Zemana 28.rijna:
    # Petr Honzejk
    # https://twitter.com/PetrHonzejk/status/1188931264037961733
    # pocet slov:
    words = {2016: 1473,
             2017: 1283,
             2018: 1155,
             2019: 996.,
             2020 : 426.,
             2021 : 0,
    }
    canname = 'ZemanovaSlova'
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)
    #filename = 'foo.root'
    #rfile = ROOT.TFile(filename, 'read')
    #hname = 'histo_h'
    #h1 = rfile.Get('hname')
    #stuff.append(h1)

    gr = ROOT.TGraphErrors()
    gr.SetName('Zemanova slova')
    ip = 0
    for year in words:
        gr.SetPoint(ip, year, words[year])
        gr.SetPointError(ip, 0, sqrt(words[year]))
        ip = ip+1
    stuff.append(gr)

    h2 = ROOT.TH2D('tmp', 'Pocet slov v projevech prezidenta Milose Zemana 28.rijna', 100, 2015, 2028, 100, 0, 2000)
    stuff.append(h2)
    h2.SetStats(0)
    h2.Draw()
    gr.SetMarkerColor(ROOT.kBlack)
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(1)
    gr.Draw('P')
    fun = ROOT.TF1('fun', '[0]+[1]*x', 2015, 2028)
    fun.SetParameter(314200, -155)
    gr.Fit(fun, '', '', 2015., 2019.5)
    fun.Draw('same')

    text = '#chi^{2}' + '/ndf = {:2.2f} '.format(fun.GetChisquare() / fun.GetNDF()) + 'Y_{0}' + ' = {:3.1f}'.format(-fun.GetParameter(0) / fun.GetParameter(1)) 
    txt = ROOT.TLatex(0.15, 0.8, text)
    txt.SetNDC()
    txt.Draw()
    stuff.append(txt)
    
    leg = ROOT.TLegend(0.55, 0.45, 0.88, 0.75)
    leg.SetHeader('Zdroj: Petr Honzejk, twitter')
    leg.SetBorderSize(0)
    leg.AddEntry(gr, 'Data', 'P')
    leg.AddEntry(fun, 'Linear fit', 'L')
    leg.Draw()
    stuff.append(leg)
    
    ROOT.gPad.Update()
    
    
    can.Print(canname + '.png')
    can.Print(canname + '.pdf')
    
    ROOT.gApplication.Run()
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

