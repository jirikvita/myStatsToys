#!/usr/bin/python
# Mon 26 Jul 21:43:41 CEST 2021

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

import numpy as np

import random

cans = []
stuff = []

##########################################

def ScaleHistosMaxima(hsx, hsy):
    mmax = 1.2 * max(hsx.GetMaximum(), hsy.GetMaximum())
    hsx.SetMaximum(mmax)
    hsy.SetMaximum(mmax)


##########################################

def getRandomWalkGraph(nSteps,
                       xmin, xmax, ymin, ymax,
                       stepxmin, stepxmax, stepymin, stepymax):
    gr = ROOT.TGraph()
    oldx = (xmin+xmax)/2.
    oldy = (ymin+ymax)/2.
    mydata = []
    suml = 0.
    for i in range(0,nSteps):
        dx,dy = random.uniform(stepxmin, stepxmax), random.uniform(stepymin, stepymax)
        newx, newy = oldx + dx, oldy + dy
        dl2 = pow(oldx - newx, 2) + pow(oldy - newy, 2)
        if dl2 > 0:
            suml = suml + sqrt(dl2)
        gr.SetPoint(i, newx, newy)
        mydata.append([1.*newx, 1.*newy])
        oldx,oldy = 1.*newx,1.*newy
    data = np.array(mydata)
    return gr, data, suml


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

    canname = 'RandomWalkAll'
    allcan = ROOT.TCanvas(canname, canname, 100, 100, 1000, 1000)
    canname = 'RandomWalkAnalysis'
    analysiscan = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1000)
    analysiscan.Divide(2, 2)
    canname = 'RandomWalk'
    can = ROOT.TCanvas(canname, canname, 200, 100, 1000, 1000)
    cans.append(allcan)
    cans.append(analysiscan)
    cans.append(can)
    #filename = 'foo.root'
    #rfile = ROOT.TFile(filename, 'read')
    #hname = 'histo_h'
    #h1 = rfile.Get(hname)
    #stuff.append(h1)

    nSteps = 1000
    xmin,xmax = -1., 1.
    ymin,ymax = -1., 1.
    step = 0.1
    stepxmin,stepxmax = -step, step
    stepymin,stepymax = -step, step
    results = []

    ROOT.gStyle.SetPalette(ROOT.kCool)
    
    nbx, nby = 100, 100
    SF = 6
    h2 = ROOT.TH2D('tmp', 'tmp', nbx, SF*xmin, SF*xmax, nby, SF*ymin, SF*ymax)

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    can.cd()
    h2.Draw('')
    stuff.append(h2)

    hsx = ROOT.TH1D('hsx', 'hsx;#sigma', 30, 0, 4*SF*step)
    hsy = ROOT.TH1D('hsy', 'hsy;#sigma', 30, 0, 4*SF*step)
    hdx = ROOT.TH1D('hdx', 'hdx;#Delta', 30, -9*SF*step, 9*SF*step)
    hdy = ROOT.TH1D('hdy', 'hdy;#Delta', 30, -9*SF*step, 9*SF*step)
    hdr = ROOT.TH1D('hdr', 'hdr;#DeltaR', 50, 0, 12*SF*step)
    dd = 0.35
    hsuml = ROOT.TH1D('hsuml', 'hsuml;Sum of #Deltal', 100, (1. - dd) * nSteps*step, (1.-0.3*dd) * nSteps*step)
    
    nWalks = 500
    nx, ny = 5, 5
    allcan.Divide(nx, ny)
    opt = 'PL PMC PLC'
    for j in range(0, nWalks):
        gr,data, suml = getRandomWalkGraph(nSteps,
                                            xmin, xmax, ymin, ymax,
                                            stepxmin, stepxmax, stepymin, stepymax)
        results.append([gr, data])

        can.cd()
        gr.SetMarkerStyle(24)
        gr.SetMarkerSize(0.3)
        gr.Draw(opt)
        opt = 'PL PLC PMC'

        stds = np.std(data, axis = 0)
        #print(stds)
        stdx = stds[0]
        stdy = stds[1]
        hsx.Fill(stdx)
        hsy.Fill(stdy)

        deltax = data[-1][0] - data[0][0]
        deltay = data[-1][1] - data[0][1]
        deltar = pow(deltax, 2) + pow(deltay, 2)
        if deltar > 0:
            deltar = sqrt(deltar)
        hdx.Fill(deltax)
        hdy.Fill(deltay)
        hdr.Fill(deltar)
        hsuml.Fill(suml)
        
        #print('sigmax={}, sigmay={}'.format(sigmax, sigmay))

    j = 0
    for result in results:
        gr = result[0]
        if j < nx*ny:
            allcan.cd(j+1)
            gr.Draw('A' + opt)
        j = j + 1
        

        
    analysiscan.cd(1)
    leg = ROOT.TLegend(0.65, 0.65, 0.88, 0.88)
    leg.SetBorderSize(0)
    ScaleHistosMaxima(hsx,hsy)
    hss = [hsx, hsy]
    for hs in hss:
        hs.SetLineWidth(2)
    analysiscan.cd(1)
    hsx.Draw('hist PLC')
    hsy.Draw('hist PLC same')   
    leg.AddEntry(hsx, '#sigma_{x}', 'L')
    leg.AddEntry(hsy, '#sigma_{y}', 'L')
    leg.Draw()

    analysiscan.cd(2)
    ScaleHistosMaxima(hdx,hdy)
    leg2 = ROOT.TLegend(0.65, 0.65, 0.88, 0.88)
    leg2.SetBorderSize(0)    
    hss = [hdx, hdy]
    for hs in hss:
        hs.SetLineWidth(2)    
    hdx.Draw('hist PLC')
    hdy.Draw('hist PLC same')
    leg2.AddEntry(hdx, '#Delta_{x}', 'L')
    leg2.AddEntry(hdy, '#Delta_{y}', 'L')
    leg2.Draw()
    

    analysiscan.cd(3)
    hdr.SetLineWidth(2)
    hdr.SetLineColor(ROOT.kRed)
    hdr.SetMaximum(1.2*hdr.GetMaximum())
    hdr.Draw('hist')
    text1 = ROOT.TLatex(0.13, 0.84, '#mu = {:1.2f} #sigma = {:1.2f}'.format(hdr.GetMean(), hdr.GetStdDev()))
    text1.SetNDC()
    text1.Draw()
    stuff.append(text1)

    analysiscan.cd(4)
    hsuml.SetLineWidth(2)
    hsuml.SetLineColor(ROOT.kBlack)
    hsuml.SetMaximum(1.2*hsuml.GetMaximum())
    hsuml.Draw('hist')
    text2 = ROOT.TLatex(0.13, 0.84, '#mu = {:1.2f} #sigma = {:1.2f}'.format(hsuml.GetMean(), hsuml.GetStdDev()))
    text2.SetNDC()
    text2.Draw()


    
    analysiscan.Update()
    allcan.Update()
    can.Update()

    for can in cans:
        can.Print(can.GetName() + '_{}.png'.format(nWalks))
        can.Print(can.GetName() + '_{}.pdf'.format(nWalks))
    
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

