#!/usr/bin/python
# Fri 27 Sep 03:03:25 CEST 2019
# https://www.zurnal.upol.cz/nc/reflexe/zprava-int/clanek/natcomm-experimentalni-data-ziskana-kontrolnim-merenim/
# https://www.zurnal.upol.cz/nc/reflexe/zprava-int/clanek/natcomm-kalibracni-data-pro-kontrolnim-merenim/

from __future__ import print_function


import numpy as nump

import ROOT
from math import sqrt, pow, log, exp, cos, sin
import os, sys, getopt

cans = []
stuff = []


##########################################
def GetXminmax(gr):
    y = ROOT.Double(0.)
    xmin = ROOT.Double(0.)
    xmax = ROOT.Double(0.)
    gr.GetPoint(0, xmin, y)
    gr.GetPoint(gr.GetN()-1, xmax, y)
    return xmin, xmax

##########################################
def Fold(gr):
    nb = gr.GetN()
    name = gr.GetName()
    title = gr.GetTitle()
    grnew = ROOT.TGraphErrors()
    grnew.SetName(name + '_folded')
    grnew.SetTitle(title)
    for i in range(0, nb/2):
        vsum = 0.
        val = ROOT.Double(0.)
        x = ROOT.Double(0.)
        gr.GetPoint(i, x, val)
        vsum = vsum + val
        x1 = 1.*x
        gr.GetPoint(nb - i - 1, x, val)
        vsum = vsum + val
        grnew.SetPoint(i, x1, vsum)
        grnew.SetPointError(i, 0., sqrt(1.*vsum))
    return grnew

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
def MakeGraphFromGraphErrors(gre):
    nb = gre.GetN()
    name = gre.GetName()
    title = gre.GetTitle()
    gr = ROOT.TGraph()
    gr.SetName(name + '_noerr')
    gr.SetTitle(title + '_noerr')
    for i in range(0, nb):
        y = ROOT.Double(0.)
        x = ROOT.Double(0.)
        gre.GetPoint(i, x, y)
        gr.SetPoint(i, x, y)
    return gr


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
def MakeGraph(filename, col = ROOT.kBlack, mss = 1., mst = 20):

    tag = filename
    tag = tag.replace('.txt','').replace('.data','').replace('.dat','')
    canname = 'can' + tag
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)
    infile = open(filename)

    gr = ROOT.TGraphErrors()
    gr.SetName('gr_' + tag)
    stuff.append(gr)

    data = []
    for line in infile.readlines():
        sline = line[:-1]
        for item in sline.split():
            #print(item)
            if len(item) > 1:
                #data.append(int(item))
                data.append(float(item))
    ip = 0
    print(data)
    for val in data:
        gr.SetPoint(ip, ip, val)
        gr.SetPointError(ip, 0., sqrt(1.*val) )
        ip = ip+1

        gr.SetMarkerSize(mss)
    gr.SetMarkerStyle(mst)
    gr.SetMarkerColor(col)
    gr.SetLineColor(col)

    can.cd()
    gr.Draw('AP')
    
    infile.close()
    return can,gr


##########################################
def MakeCorrelogram(gr, col = ROOT.kBlue, mss = 0.5, mst = 20):
    gr2 = ROOT.TGraph()
    gr2.SetName('gr2corr_' + gr.GetName())
    x1 = ROOT.Double(0.)
    y1 = ROOT.Double(0.)
    x2 = ROOT.Double(0.)
    y2 = ROOT.Double(0.)
    n = gr.GetN()
    for i in range(0,n):
        j = i+1
        if j > n-1: j = j - n + 1
        gr.GetPoint(i, x1, y1)
        gr.GetPoint(j, x2, y2)
        #print(i,j,x1,y1,x2,y2)
        gr2.SetPoint(i, y1, y2)

    gr2.SetMarkerSize(mss)
    gr2.SetMarkerStyle(mst)
    gr2.SetMarkerColor(col)
    gr2.SetLineColor(col)
    
    canname = 'cancorr_' + gr.GetName()
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)
    can.cd()
    gr2.Draw('AP')
    rho = gr2.GetCorrelationFactor()
    txt = ROOT.TLatex(0.15, 0.80, '#rho=' + '{:1.2f}'.format(rho))
    txt.SetNDC()
    txt.Draw()
    stuff.append(txt)
    

    return can,gr2

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

    # real data by Jakub Navarik:
    can,grfull = MakeGraph('data_navarik.txt', ROOT.kRed)
    gr = Fold(grfull)
    #cancalib,grcalib = MakeGraph('calib_navarik.txt', ROOT.kBlack)
    
    # pseudodata generated by JK:
    #can,gr = MakeGraph('pseudodata_add6pct_vals.txt', ROOT.kRed)
    #can,gr = MakeGraph('pseudodata_std_vals.txt', ROOT.kRed)

    # doublet
    # can,gr = MakeGraph('pseudodata_doublet_add6ptcl_vals.txt', ROOT.kRed)
    # mpre pro[er:
    can,gr = MakeGraph('can2_add6ptcl_vals.txt', ROOT.kRed)

    cancorr,gr2corr = MakeCorrelogram(gr, ROOT.kBlue)

    tag = gr.GetName()
    tag = tag.replace('.txt', '').replace('_vals','').replace('gr_','')
    
    gr_array = MakeYArrayFromGraph(gr)
    fft_array = nump.fft.fft(gr_array)
    print(fft_array)
    a_mag = nump.abs(fft_array)
    a_ph = nump.angle(fft_array)
    print(a_mag)
    gr_m = MakeGraphFromArray(a_mag, 'magnitude')
    gr_ph = MakeGraphFromArray(a_ph, 'phase')
    stuff.append([gr_m, gr_ph])

    canname = 'FFT_' + tag
    fftcan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 1200)
    fftcan.Divide(2,2)
    cans.append(fftcan)
    fftcan.cd(1)
    gr.Draw('AP')
    fftcan.cd(3)
    gr_m.Draw('APL')
    ROOT.gPad.SetLogy(1)
    fftcan.cd(4)
    gr_ph.Draw('APL')
    fftcan.Update()
    
    fft_cplx_array = nump.array([0.]*len(fft_array))
    decayC =  128. / 512. * len(fft_array) # 32., 128. default: 64
    print('Will use an exponential freq. filter with the decay constant 1./{:3.1f}'.format(decayC))
    for ii in xrange(0, len(fft_array)):
        #if ii < 64:
        #    fft_cplx_array[ii] = a_mag[ii]*( cos(a_ph[ii]) + sin(a_ph[ii])*(1j) )
        #else:
        
        ihalf = len(fft_array) / 2
        kk = -ii
        if ii > ihalf:
            kk = ii - ihalf 

        fft_cplx_array[ii] = exp(kk/decayC)*a_mag[ii]*( cos(a_ph[ii]) + sin(a_ph[ii])*(1j) )

    ifft_array = nump.fft.fft(fft_cplx_array)
    ia_mag = nump.abs(ifft_array)
    ia_ph = nump.angle(ifft_array)
    igr_m = MakeGraphFromArray(ia_mag, 'magnitude')
    igr_ph = MakeGraphFromArray(ia_ph, 'phase')
    stuff.append([igr_m, igr_ph])

    
    canname = 'iFFT_' + tag + '_filt{:}'.format(int(decayC))
    ifftcan = ROOT.TCanvas(canname, canname, 0, 0, 1200, 800)
    ifftcan.Divide(2,1)

    cans.append(ifftcan)
    ifftcan.cd(2)
    igr_m.SetMarkerSize(0.5)
    igr_m.SetTitle('Filtered')
    igr_m.SetMarkerStyle(20)
    igr_m.Draw('AP')
    ifftcan.cd(1)
    grnoErr = MakeGraphFromGraphErrors(gr)
    grnoErr.SetTitle('Original')
    grnoErr.SetMarkerSize(0.5)
    grnoErr.SetMarkerStyle(20)
    grnoErr.Draw('AP')
    #igr_ph.SetMarkerSize(0.5)
    #igr_ph.SetMarkerStyle(20)
    #igr_ph.Draw('AP')
    
    
    for cc in cans:
        cc.Update()
        cc.Print(cc.GetName() + '.png')
        cc.Print(cc.GetName() + '.pdf')

        
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

