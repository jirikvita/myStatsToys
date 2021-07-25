#!/usr/bin/python

# Thu  5 Sep 12:36:45 CEST 2019
# what about year average temperatures?
# 5y averages?

from __future__ import print_function

import numpy as nump

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

nMonths = 12
statError = 0.05
Year0 = 1961

# dictionary on month names, entered manualy, uff!! ;-)
dMonths = {1: 'Jan',
           2: 'Feb',
           3: 'Mar',
           4: 'Apr',
           5: 'May',
           6: 'Jun',
           7: 'Jul',
           8: 'Aug',
           9: 'Sep',
           10: 'Oct',
           11: 'Nov',
           12: 'Dec' }

cans = []
stuff = []

  

##########################################
def SetMonthLabels(hh):
    nb = hh.GetNbinsX()
    if nb != nMonths: return
    for i in range(0, nb):
        hh.GetXaxis().SetBinLabel(i+1, dMonths[i+1])

##########################################
def GetXminmax(gr):
    y = ROOT.Double(0.)
    xmin = ROOT.Double(0.)
    xmax = ROOT.Double(0.)
    gr.GetPoint(0, xmin, y)
    gr.GetPoint(gr.GetN()-1, xmax, y)
    return xmin, xmax

##########################################
def MakeHistoFromGraph(gr):
    # support of only equidistant binning!
    nb = gr.GetN()
    xmin,xmax = GetXminmax(gr)
    half = 0.5 * (xmax - xmin) / nb
    name = gr.GetName()
    title = gr.GetTitle()
    hh = ROOT.TH1D(name, title, nb, xmin-half, xmax+half)
    for i in range(0, nb):
        y = ROOT.Double(0.)
        x = ROOT.Double(0.)
        gr.GetPoint(i, x, y)
        hh.SetBinContent(i+1, y)
        hh.SetBinError(i+1, gr.GetErrorY(i))
    return hh

##########################################
def MakeYArrayFromGraph(gr):
    nb = gr.GetN()
    xmin,xmax = GetXminmax(gr)
    half = 0.5 * (xmax - xmin) / nb
    name = gr.GetName()
    title = gr.GetTitle()
    a = []
    for i in range(0, nb):
        y = ROOT.Double(0.)
        x = ROOT.Double(0.)
        gr.GetPoint(i, x, y)
        a.append(y)
    return a
  
##########################################
# todo: add support of x values?
def MakeGraphFromArray(a, name = 'gr', title = ''):
    gr = ROOT.TGraph()
    gr.SetName(name)
    gr.SetTitle(title)
    for i in range(0,len(a)):
        gr.SetPoint(i, i, a[i])
    return gr


##########################################

def MakeFitResiduals(gr, fun):
    name = fun.GetName() + '_res'
    xx = 12.
    nb = 24
    hh = ROOT.TH1D(name, name, nb, -xx, xx)
    x = ROOT.Double(0.)
    val = ROOT.Double(0.)
    for ip in range(0, gr.GetN()):
        gr.GetPoint(ip, x, val)
        fitval = fun.Eval(x)
        diff = fitval - val
        hh.Fill(diff)
    return hh

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

    ROOT.gStyle.SetOptTitle(0)
    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    filename = 'data/O1LYSA01.txt'
    infile = open(filename, 'read')
    
    debug = 0
    
    years = {}
    lastyear = ''
    for xline in infile.readlines():
        line = xline[:-1]
        if len(xline) < 3 : continue
        if debug: print(line)
        items = xline.split()
        if len(items) < nMonths : continue
        year = items[0]
        if debug:
            print('"{:}"'.format(year[:2],))
        cent = year[:2]
        if not (cent == '19' or cent == '20') : continue
        iyear = int(year)
        if lastyear != year:
            years[iyear] = {}
            lastyear = year
        if lastyear == '': lastyear = year
        month = items[1]
        imonth = int(month)
        if debug:
            print('Month: {}'.format(imonth))
        years[iyear][imonth] = []
        if debug: print(years)
        for item in items[2:]:
            data = float(item.replace(',', '.'))
            years[iyear][imonth].append(data)

        if debug:
            print('Inserted:')
            print(years[iyear][imonth])
            print(years)

    if debug :
        print('Grand data:')
        print(years)

    gr_GrandDay = ROOT.TGraph()
    gr_MonthAver = ROOT.TGraph()
    gr_Months = [ ROOT.TGraphErrors() for i in range(0, nMonths) ]

    gr_EveryMonth = {}
       
    ip = 0
    im = 0
    for year in years:
        gr_EveryMonth[year] = {}
        for month in years[year]:
            monthT = 0.
            jmonth = month - 1
            print(jmonth)
            nm = 0
            for dayT in years[year][month]:
                gr_GrandDay.SetPoint(ip, ip, dayT)
                ip = ip+1
                monthT = monthT + dayT
                nm = nm + 1
                np = 0
                try:
                    np = gr_EveryMonth[year][jmonth].GetN()
                except:
                    gr_EveryMonth[year][jmonth] = ROOT.TGraphErrors()
                print('Seting point {} with dayly temp {}'.format(np, dayT))    
                gr_EveryMonth[year][jmonth].SetPoint(np, np, dayT)
                gr_EveryMonth[year][jmonth].SetPointError(np, 0., statError)
    
            monthT = monthT / nm

            gr_MonthAver.SetPoint(im, im, monthT)
            im = im + 1

            np = gr_Months[jmonth].GetN()
            print('Seting point {} with month temp {}'.format(np, monthT))
            gr_Months[jmonth].SetPoint(np, np, monthT)
            

        

 

    canname = 'residuals'
    rcan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 1000)
    rcan.Divide(4,3)
    cans.append(rcan)

    canname = 'fits'
    fcan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 1000)
    #fcan.Divide(27,27)
    cans.append(fcan)

    
    residuals = {}
    funs = []
    stuff.append([residuals, funs])

    opt = ['' for i in range(0, nMonths)]
    igr = 0
    h_chi2s = ROOT.TH1D('chi2ndfs', 'chi2ndfs;#chi^{2}/1000;slope of fits in each month', 50, 0, 15)
    stuff.append(h_chi2s)
    #h_chi2s.SetStats(0)
    for year in gr_EveryMonth:
        residuals[year] = {}
        for jmonth in gr_EveryMonth[year]:
            gr = gr_EveryMonth[year][jmonth]
            funname = 'linfit_{}_{}'.format(year,jmonth)
            grxmin, grxmax = GetXminmax(gr)
            fun = ROOT.TF1(funname, '[0] + [1]*x', grxmin, grxmax)
            fun.SetLineColor(year - Year0 + 1 + jmonth)
            x = ROOT.Double(0.)
            midpoint = ROOT.Double(0.)
            gr.GetPoint(gr.GetN()/2, x, midpoint)
            fun.SetParameters(midpoint, 0.)
            #fun.FixParameter(1, 0.)
            #fcan.cd(igr+1)
            fcan.cd()
            igr = igr + 1
            if igr == 1:
                temp = ROOT.TH2D('tmp', 'tmp;Day in moth', 100, 0, 32, 100, -25, 25)
                stuff.append(temp)
                temp.SetStats(0)
                temp.Draw()
                #gr.Draw('AP')
            #else:
            gr.SetMarkerColor(fun.GetLineColor())
            gr.SetMarkerSize(0.5)
            gr.SetMarkerStyle(jmonth+1)
            gr.SetLineColor(fun.GetLineColor())
            gr.Draw('P')
            gr.Fit(funname)
            chi2 = fun.GetChisquare()
            ndf = fun.GetNDF()
            if ndf > 0:
                print(chi2/ndf)
                h_chi2s.Fill(chi2/ndf/1000.)
            
            funs.append(fun)
            stuff.append(gr)

            histo = MakeFitResiduals(gr, fun)
            residuals[year][jmonth] = histo
            rcan.cd(jmonth+1)
            histo.SetStats(0)
            histo.SetLineColor(year - Year0 + 1)
            histo.SetMaximum(2.5*histo.GetMaximum())
            histo.Draw('C' + opt[jmonth])
            opt[jmonth] = 'same'
            text = '{}'.format(dMonths[jmonth+1])
            txt = ROOT.TLatex(0.14, 0.84, text)
            txt.SetNDC()
            stuff.append(txt)
            txt.Draw()

    # set monthly error bars to lin fit residuals width of every month!
    for year in years:
        gr_EveryMonth[year] = {}
        for month in years[year]:
            monthT = 0.
            jmonth = month - 1
            for np in range(0, gr_Months[jmonth].GetN()):
                stat = residuals[year][jmonth].GetRMS()
                gr_Months[jmonth].SetPointError(np, 0., stat)

    canname = 'DayMonth'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1200, 600)
    can.Divide(2,1)
    cans.append(can)
    can.cd(1)
    gr_GrandDay.GetXaxis().SetTitle('Day since Jan {}'.format(Year0))
    gr_GrandDay.GetYaxis().SetTitle('Aver. day temp. [#circC]')
    gr_GrandDay.SetMarkerStyle(20)
    gr_GrandDay.SetMarkerSize(0.5)
    gr_GrandDay.SetMarkerColor(ROOT.kRed)
    gr_GrandDay.Draw("AP")
    stuff.append(gr_GrandDay)

    can.cd(2)
    gr_MonthAver.SetMarkerStyle(20)
    gr_MonthAver.GetXaxis().SetTitle('Month since Jan {}'.format(Year0))
    gr_MonthAver.GetYaxis().SetTitle('Aver. month temp. [#circC]')
    
    gr_MonthAver.SetMarkerSize(0.5)
    gr_MonthAver.SetMarkerColor(ROOT.kBlue)
    gr_MonthAver.Draw("AP")
    stuff.append(gr_MonthAver)

    canname = 'monthly'
    mcan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 1000)
    mcan.Divide(4,3)
    cans.append(mcan)

    h_slopes = ROOT.TH1D('monthslopes', 'monthslopes;month;aver. temp. slope / year', 12, 0.5, 12.5)
    h_slopes.SetStats(0)
    stuff.append(h_slopes)
    h_slopeSig = ROOT.TH1D('monthslopeSig', 'monthslopeSig;month;signif. of aver. temp. slope / year', 12, 0.5, 12.5)
    h_slopeSig.SetStats(0)
    stuff.append(h_slopeSig)
    
    
    for im in range(0, nMonths):
        gr = gr_Months[im]
        mcan.cd(im+1)
        gr.GetXaxis().SetTitle('Year - {}'.format(Year0))
        gr.GetYaxis().SetTitle('Aver. month temp. [#circC]')
        gr.SetMarkerStyle(20)
        gr.SetMarkerSize(0.5)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.Draw("APE1")

        funname = 'linfit_{}_{}'.format(gr.GetName(), im)
        grxmin, grxmax = GetXminmax(gr)
        fun = ROOT.TF1(funname, '[0] + [1]*x', grxmin, grxmax)
        x = ROOT.Double(0.)
        midpoint = ROOT.Double(0.)
        gr.GetPoint(gr.GetN()/2, x, midpoint)
        fun.SetParameters(midpoint, 0.)
        gr.Fit(funname)
        
        text = '{}'.format(dMonths[im+1])
        txt = ROOT.TLatex(0.14, 0.84, text)
        txt.SetNDC()
        stuff.append(txt)
        txt.Draw()

        slope = fun.GetParameter(1)
        slopeError = fun.GetParError(1)
        signif = slope / slopeError
        
        h_slopes.SetBinContent(im+1, slope)
        h_slopes.SetBinError(im+1, slopeError)
        h_slopeSig.SetBinContent(im+1, signif)
        
        chi2 = fun.GetChisquare()
        ndf = fun.GetNDF()
        text = '#chi^{2}/ndf=' + '{:2.2f}'.format(chi2/ndf) + ' a={:1.3f}'.format(slope) + '#pm' + '{:1.3f}'.format(slopeError) + ' S={:1.2f}'.format(signif)
        txt = ROOT.TLatex(0.14, 0.14, text)
        txt.SetNDC()
        stuff.append(txt)
        txt.Draw()


    canname = 'MonthSlopes'
    scan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 1200)
    scan.Divide(2,2)
    cans.append(scan)
    scan.cd(1)
    SetMonthLabels(h_slopes)
    #h_slopes.SetFillStyle(1)
    h_slopes.SetFillColor(ROOT.kAzure+10)
    h_slopes.SetMarkerColor(ROOT.kRed-4)
    h_slopes.SetLineColor(ROOT.kRed-4)
    h_slopes.SetMarkerSize(1)
    h_slopes.SetMarkerStyle(20)
    h_slopes.Draw('bar e1 x0')
    ROOT.gPad.SetLeftMargin(0.15)

    scan.cd(2)
    SetMonthLabels(h_slopeSig)
    h_slopeSig.SetFillColor(ROOT.kGreen+2)
    h_slopeSig.SetMarkerColor(ROOT.kGreen+2)
    h_slopeSig.SetLineColor(ROOT.kGreen+2)
    h_slopeSig.SetMarkerSize(1)
    h_slopeSig.SetMarkerStyle(20)
    h_slopeSig.Draw('bar P')

    scan.cd(3)
    
    h_chi2s.Draw('hist')
    
 

    # convert tgraph to histogram
    #h_GrandDay = MakeHistoFromGraph(gr_GrandDay)
    #ROOT.TVirtualFFT.SetTransform(0);
    # magnitude of the FFT
    #hm = ROOT.TH1D()
    #hm = h_GrandDay.FFT(hm, "MAG");
    #hm.SetName('FFT_mag' + h_GrandDay.GetName())
    # phase of the FFT
    #hm.SetTitle('FFT_mag_' + h_GrandDay.GetTitle())
    #hph = ROOT.TH1D()
    #hph = h_GrandDay.FFT(hph, "PH");
    #hph.SetName("FFT_ph_" + h_GrandDay.GetName());
    #hph.SetTitle("FFT_ph_" + h_GrandDay.GetTitle());
    # convert tgraph to array
    a_GrandDay = MakeYArrayFromGraph(gr_GrandDay)
    #print(a_GrandDay)
    # https://docs.scipy.org/doc/numpy/reference/routines.fft.html
    fft_GrandDay = nump.fft.fft(a_GrandDay)
    #print(fft_GrandDay)
    a_mag = nump.abs(fft_GrandDay)
    a_ph = nump.angle(fft_GrandDay)
    #print(a_mag)
    gr_m = MakeGraphFromArray(a_mag, 'magnitude')
    gr_ph = MakeGraphFromArray(a_ph, 'phase')
    stuff.append([gr_m, gr_ph])
    
    canname = 'YearlyFFT'
    fftcan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 1200)
    fftcan.Divide(2,2)
    cans.append(fftcan)
    fftcan.cd(1)
    gr_GrandDay.Draw('AP')
    fftcan.cd(3)
    gr_m.Draw('APL')
    fftcan.cd(4)
    gr_ph.Draw('APL')

    
    for can in cans:
        can.Update()
        can.Print(can.GetName() + '.png')
        can.Print(can.GetName() + '.pdf')
    
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

