#!/usr/bin/python

# jk 201X -- 2020

from __future__ import print_function

import ROOT
from math import fabs
kEpsilon = 1.e-4

Ltex = []
_h = []

#########################################################

def MakeVerticalLines(xs, y1, y2, col, ls = 2):
    lines = []
    for x in xs:
        line = ROOT.TLine(x, y1, x, y2)
        line.SetLineColor(col)
        line.SetLineStyle(ls)
        lines.append(line)
    return lines

#########################################################
def adjustStats(h):
    ROOT.gPad.Update()
    #st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    st.SetX1NDC(0.7)
    st.SetX2NDC(0.95)
    st.SetY1NDC(0.65)
    st.SetY2NDC(0.95)
    

#########################################################
def myround(val):
    newval = 1.*val
    #if val > 100000:
    #    newval = 10000*int(round(val/10000.))
    #el
    #if val > 10000:
    #    newval = 1000*int(round(val/1000.))
    #el
    if val > 1000:
        newval = 100*int(round(val/100.))
    elif val > 100:
        newval = 10*int(round(val/10.))
    return newval

#########################################################
def FixXaxisTitle(hdata, axis = 'x'):
    xtitle = ''
    if axis == 'x':
        xtitle = hdata.GetXaxis().GetTitle()
    else:
        xtitle = hdata.GetYaxis().GetTitle()
    newxtitle = xtitle + ''
    if 'DiTop' in xtitle:
        if 'DiTop m ' in xtitle:
            newxtitle = newxtitle.replace('DiTop m ','m^{t#bar{t}} ')
        if 'DiTop p_{T} ' in xtitle:
            newxtitle = newxtitle.replace('DiTop p_{T} ','p_{T}^{t#bar{t}} ')
        if 'DiTop ' in xtitle:
            newxtitle = newxtitle.replace('DiTop ',' ')
    if newxtitle != xtitle:
        if axis == 'x':
            hdata.GetXaxis().SetTitle(newxtitle)
        else:
            hdata.GetYaxis().SetTitle(newxtitle)
#########################################################


def MakeLegHeader(name):
    tag = name.split('/')[0]
    return 'Selection: {}'.format(tag)

def MakeTopoTag(name):
    tag = name.split('/')[0]
    return '{}'.format(tag)

#########################################################
    
def GetChi2(h1, h2):
    chi2 = 0.
    ndf = 0
    for i in range(1, h2.GetNbinsX()+1):
        e1 = h1.GetBinError(i)
        e2 = h2.GetBinError(i)
        ee = e1**2 + e2**2
        v1 = h1.GetBinContent(i)
        v2 = h2.GetBinContent(i)
        if ee > 0. and v1 > 0. and v2 > 0.:
            val = (v2-v1)**2 / ee
            chi2 = chi2 + val
            ndf = ndf + 1
    return ndf,chi2

#########################################################

def DrawArrowForPointsOutsideYAxisRange(ratio, shisto, xmin = 1, xmax = -1, alen = 0.12, size = 0.012, opt = '|>', ac = ROOT.kRed+1, sf = 0.01):
    arrows = []
    ymax = shisto.GetYaxis().GetXmax()
    ymin = shisto.GetYaxis().GetXmin()
    for i in range(1, ratio.GetNbinsX()+1):
        y = ratio.GetBinContent(i)
        x = ratio.GetBinCenter(i)
        # skip if zoomed
        if xmin < xmax and ( x < xmin or x > xmax):
            continue
        delta = ymax - ymin
        ll = delta*alen
        if y > ymax or (y < ymin and fabs(y) > kEpsilon):
            y1 = ymax - ll
            y2 = ymax - sf*delta
            if y < ymin:
                y1 = ymin + ll
                y2 = ymin + sf*delta
            arr = ROOT.TArrow(x, y1, x, y2, size, opt)
            arrows.append(arr)
            arr.SetFillColor(ac)
            arr.SetLineColor(ac)
            arr.Draw()
    return arrows
    
#########################################################

def IsUniformlyBinned(h):
    lastw = -1
    for i in range(1,h.GetXaxis().GetNbins()+1):
        bw = h.GetBinWidth(i)
        if i > 1:
            if fabs(bw - lastw) > 1.e-4:
                return False
        lastw = bw
    return True

#########################################################

def DivideByBinWidth(h):
    # WAS:
    # for i in range(1,h.GetXaxis().GetNbins()+1):
    # FIX 10.6.2021!!!
    for i in range(0,h.GetXaxis().GetNbins()+2):        
        bw = h.GetBinWidth(i)
        if bw > 0:
            h.SetBinContent(i, h.GetBinContent(i)/bw)
            h.SetBinError(i, h.GetBinError(i)/bw)
        else:
            print('ERROR: in DivideByBinWidth of histo {} bin width is {}!'.format(h.GetName(), bw))
        h.Scale(1.)

#########################################################

def DivideByBinArea(h2):
    for i in range(1,h2.GetXaxis().GetNbins()+1):
        for j in range(1,h2.GetYaxis().GetNbins()+1):
            bwx = h2.GetXaxis().GetBinWidth(i)
            bwy = h2.GetYaxis().GetBinWidth(j)
            area = bwx*bwy
            if area > 0:
                h2.SetBinContent(i,j, h2.GetBinContent(i,j) / area)
                h2.SetBinError(i,i, h2.GetBinError(i,j) / area)
            else:
                print('ERROR: in DivideByBinWidth of histo {} bin {},{} area is {}!'.format(h2.GetName(), i,j, area))
    h2.Scale(1.)

#########################################################

def MakeOneWithErrors(hist):
    ratio = hist.Clone(hist.GetName() + '_ratio')
    ratio.Reset()
    for i in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(i) > 0.:
            ratio.SetBinContent(i, 1.)
            ratio.SetBinError(i, hist.GetBinError(i) / hist.GetBinContent(i))
        else:
            ratio.SetBinContent(i, 1.)
            ratio.SetBinError(i, 0.)
    ratio.Scale(1.)
    return ratio

#########################################################

def MakeOneWithoutErrors(hist):
    ratio = hist.Clone(hist.GetName() + '_1noerrs')
    ratio.Reset()
    for i in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(i) > 0.:
            ratio.SetBinContent(i, 1.)
            ratio.SetBinError(i, 0.)
    ratio.Scale(1.)
    return ratio

#########################################################

def MakeNiceLegendEntry(name, isptcl = 0):
    ###!!! name = name.replace('ljets_ttj_nocuts', 't#bar{t}, ')
    name = name.replace('ljets_ttj_nocuts', 't#bar{t}, ')
    name = name.replace('analyzed_histos_all', '')
    name = name.replace('analyzed_all', '')
    name = name.replace('analyzed', '')
    name = name.replace('14TeV', '')
    #name = name.replace('ljets_ttj_nocuts', 't#bar{t} NLO, ')
    name = name.replace('ljets_tt_nocuts', 't#bar{t} LO, ')

    name = name.replace('CloseMt', 'closest m_{t}')
    name = name.replace('SameMt', 'same m_{t}')
    name = name.replace('Standard', 'standard')
    name = name.replace('BestBsAndNu', 'best m_{t}')

    name = name.replace('_', ' ') ### !!!
    
    name = name.replace('zp ttbarj', "pp #rightarrow Z' #rightarrow t#bar{t}, m_{Z'} = ")
    name = name.replace('pp2xdxdtt y0 1000GeV xd ', 'pp #rightarrow #chi_{D}#bar{#chi}_{D} t#bar{t}, m_{y_{0}} = 1 TeV, m_{#chi_{0}} = ')
    name = name.replace('pp2y02tt y0 ', 'pp #rightarrow y_{0} #rightarrow t#bar{t}, m_{y_{0}} = ')
    name = name.replace('pp 2b2j', 'pp #rightarrow b#bar{b}+jets')

    name = name.replace('ttbarj', 't#bar{t}j')
    name = name.replace('ttbar', 't#bar{t}')
    name = name.replace('tt', 't#bar{t}')
    name = name.replace('2tt', 'tt')
    name = name.replace('pp2t', 'pp #rightarrow t#bar{t}')
    name = name.replace('pp 2tj', 'pp #rightarrow t#bar{t}')
    name = name.replace('700_ljets', "m_{Z'} = 700 GeV, ")
    name = name.replace('1000_ljets', "m_{Z'} = 1000 GeV, ")

    name = name.replace('1000 GeV', '1 TeV')
    name = name.replace('1500 GeV', '1.5 TeV')
    name = name.replace('1250 GeV', '1.25 TeV')
    
    name = name.replace('_ljets_', '')
    name = name.replace('NLO', '')
    
    
    name = name.replace('  ', ' ')
    name = name.replace('ptheavy', 'p_{T}^{heavy} > ')
    name = name.replace('ptj1min60 ptj2min60', ', p_{T}^{j1,j2} > 60 GeV')
    name = name.replace('GeV', ' GeV')
    name = name.replace('y0', 'y_{0}')
    #name = name.replace('xd', '#chi_{D}')
    name = name.replace(' allhad', '')
    name = name.replace(' all', '')
    name = name.replace('pp2', 'pp #rightarrow ')
    #if isptcl == 0:
    name = name.replace('ATLAS', '')
    name = name.replace('CMS', '')
    name = name.replace('Py8 ATLAS', '')
    name = name.replace('Py8 CMS', '')
    name = name.replace('Py8', '')

    name = name.replace('newWrange', '')
    name = name.replace('Prelim', '')
    name = name.replace('NEW ', '')
    name = name.replace('P4', '')
    name = name.replace('newJES', '')
    name = name.replace('newNewJES', 'new')
    name = name.replace('run 1X', '')
    name = name.replace('  ', ' ')    
    name = name.replace('ALL weighted', '(control)')
    name = name.replace('LO matched (control)', '(QCD bckg.)')
    
    #else:
    #    name = name.replace(' ATLAS', ' (ATLAS card), ')
    #    name = name.replace(' CMS', ' (CMS card), ')
    #    name = name.replace(' Py8 ATLAS', ' (ATLAS card), ')
    #    name = name.replace(' Py8 CMS', ' (CMS card), ')
    #    name = name.replace(' Py8', '')
    return name

#########################################################

def MakePrettyTitle(name):
    name = name.replace('_ptcl', ' particle')
    name = name.replace('_det', ' detector')
    name = name.replace('And', ' and ')
    name = name.replace('Particle', 'particle')
    name = name.replace('Detector', 'detector')

    name = name.replace('Parton', 'parton')
    name = name.replace('Match', ' match')
    name = name.replace('pseudo', 'pseudo-')
    name = name.replace('ttbar', 't#bar{t}')
    name = name.replace('pseudo-toplepton', 'leptonic pseudo-top' )
    name = name.replace('pseudo-tophadron', 'hadronic pseudo-top' )

    name = name.replace('and particle matched', 'matched')
    name = name.replace('detector matched', 'matched')
    
    return name

#########################################################
def NormalizeByColumns(hist, thr = 0.01):
    for i in range(1,hist.GetNbinsX()+1):
        sum = 0.
        for j in range(1,hist.GetNbinsX()+1):
            sum = sum + hist.GetBinContent(i,j)
        for j in range(1,hist.GetNbinsY()+1):
            if sum > 0.:
                hist.SetBinContent(i,j,  hist.GetBinContent(i,j) / sum)
                hist.SetBinError(i,j,  hist.GetBinError(i,j) / sum)
            if hist.GetBinContent(i,j) <= thr:
                hist.SetBinContent(i,j,  0.)
                hist.SetBinError(i,j,  0.)

    hist.Scale(1.)

#########################################################
def MakeMultiSubPads(can, ratios, PadSeparation = 0.0, UpperPadTopMargin = 0.07, LowestPadBottomMargin = 0.40,  UpperPadBottomMargin = 0.0):
    x0 = 0.01
    x1 = 0.99
    tag = can.GetName()
    pads = []
    y0 = 1.
    nr = len(ratios)
    for i in range(0,nr):
        y1 = y0 - ratios[i] + PadSeparation/2
        pad = ROOT.TPad("p1" + tag,"p1" + tag, x0, y1, x1, y0 - PadSeparation/2)
        print( x0, y1, x1, y0 + PadSeparation/2)
        y0 = 1.*y1
        pad.SetTopMargin(0.07)
        if i == 0:
            pad.SetTopMargin(UpperPadTopMargin)
            pad.SetBottomMargin(UpperPadBottomMargin)
        elif i == nr - 1:
            pad.SetTopMargin(0.)
            pad.SetBottomMargin(LowestPadBottomMargin)
        else:
            pad.SetTopMargin(0.)
            pad.SetBottomMargin(0.)
        #pad.SetBorderSize(1)
        #pad.SetFillColor(i+1)
        pad.Draw()
        pads.append(pad)
  
    xx = 0.5
    width = 0.39
    height = 0.42
    yy = 0.5
    pad_inset = ROOT.TPad("pad_inset" + tag,"pad_inset" + tag,xx, yy, xx + width, yy + height);
    pad_inset.SetTopMargin(0.05);
    pad_inset.SetRightMargin(0.05);
    pad_inset.SetBottomMargin(0.12);
    #pad_inset.Divide(2,1)
    pad_inset.cd()
    
    
    return pads,pad_inset

#########################################################
def MakePadsStack(can, side, ratio_size = 0.35, PadSeparation = 0.0, UpperPadBottomMargin = 0.0, LowerPadTopMargin = 0.0):

    x0 = 0.01
    x1 = 0.49
    y0 = 0.01
    y1 = 0.99
    if side == 'right':
        x0 = 0.51
        x1 = 0.99
    if side == 'centre':
        x0 = 0.01
        x1 = 0.99
        
    tag = can.GetName()
    
    pad1 = ROOT.TPad("p1" + tag,"p1" + tag,x0,ratio_size + PadSeparation/2,x1,y1)
    pad1.Draw()
    pad1.SetTopMargin(0.07)
    pad1.SetBottomMargin(UpperPadBottomMargin)
    #pad1.SetLineColor(ROOT.kRed)
    #pad1.SetBorderSize(1)
    #pad1.SetFillColor(ROOT.kYellow)
    pad1.Draw()
    
    pad2 = ROOT.TPad("p2" + tag,"p2" + tag,x0,y0,x1,ratio_size - PadSeparation/2)
    pad2.Draw()
    pad2.SetTopMargin(LowerPadTopMargin)
    pad2.SetBottomMargin(0.25)
    #pad2.SetLineColor(ROOT.kRed)
    #pad2.SetBorderSize(1)
    #pad2.SetFillColor(ROOT.kGray)
    pad2.Draw()
    
    xx = 0.195
    width = 0.28
    height = 0.41
    yy = 0.345
    pad_inset = ROOT.TPad("pad_inset" + tag,"pad_inset" + tag,xx, yy, xx + width, yy + height);
    pad_inset.SetTopMargin(0.15);
    pad_inset.SetBottomMargin(0.20);
    #pad_inset.Draw();
          
    return pad1,pad2,pad_inset

#########################################################

def MakePads(can, side, ratio_size = 0.35, PadSeparation = 0.045, UpperPadBottomMargin = 0.07, LowerPadTopMargin = 0.0):

    x0 = 0.01
    x1 = 0.49
    y0 = 0.01
    y1 = 0.99
    if side == 'right':
        x0 = 0.51
        x1 = 0.99
    elif side == 'full':
        x0 = 0.01
        x1 = 0.99
        
    tag = can.GetName()
        
    pad1 = ROOT.TPad("p1"+tag,"p1"+tag,x0,ratio_size + PadSeparation/2,x1,y1)
    pad1.Draw()
    pad1.SetTopMargin(0.07)
    pad1.SetBottomMargin(UpperPadBottomMargin)
    pad1.SetLineColor(ROOT.kRed)
    #pad1.SetBorderSize(1)
    #pad1.SetFillColor(ROOT.kYellow)
    pad1.Draw()
    
    pad2 = ROOT.TPad("p2"+tag,"p2"+tag,x0,y0,x1,ratio_size - PadSeparation/2)
    pad2.Draw()
    pad2.SetTopMargin(LowerPadTopMargin)
    pad2.SetBottomMargin(0.25)
    pad2.SetLineColor(ROOT.kRed)
    #pad2.SetBorderSize(1)
    #pad2.SetFillColor(ROOT.kGray)
    pad2.Draw()
    
    xx = 0.195
    width = 0.28
    height = 0.41
    yy = 0.345
    pad_inset = ROOT.TPad("pad_inset"+tag,"pad_inset"+tag,xx, yy, xx + width, yy + height);
    pad_inset.SetTopMargin(0.15);
    pad_inset.SetBottomMargin(0.20);
    #pad_inset.Draw();
          
    return pad1,pad2,pad_inset

#########################################################

def MakeRatio( data, prediction, setgr = False ):
    ratio = ROOT.TGraphAsymmErrors()
    
    if setgr:
        SetTH1FStyle( ratio, color=data.GetMarkerColor(), markerstyle=data.GetMarkerStyle(), markersize=data.GetMarkerSize() )
    
    #if data.Class() in [ TGraph().Class(), TGraphErrors.Class(), TGraphAsymmErrors().Class() ]:
    #   nbins = data.GetN()
    #else:
    nbins = data.GetNbinsX()
    print('nbins: %i' % (nbins,))
    i = 0
    for n in range( nbins ):
        x_mc = ROOT.Double()
        y_mc = ROOT.Double()
        x_data = ROOT.Double()
        y_data = ROOT.Double()

        #if prediction.Class() in [ TGraph().Class(), TGraphErrors.Class(), TGraphAsymmErrors().Class() ]:
        #   prediction.GetPoint( n, x_mc, y_mc )
        #else:
        x_mc = prediction.GetBinCenter( n+1 )
        y_mc = prediction.GetBinContent( n+1 )   
        print(x_mc, y_mc)
        if y_mc == 0.: continue

        #if data.Class() in [ TGraph().Class(), TGraphErrors.Class(), TGraphAsymmErrors().Class() ]:
        #   data.GetPoint( n, x_data, y_data )
        #   bw = data.GetErrorXlow(n) + data.GetErrorXhigh(n)
        #   dy_u = data.GetErrorYhigh(n)
        #   dy_d = data.GetErrorYlow(n)
        #else:    
        x_data = data.GetBinCenter( n+1 )
        y_data = data.GetBinContent( n+1 )
        bw = data.GetBinWidth( n+1 )
        dy_u = data.GetBinError( n+1 )
        dy_d = data.GetBinError( n+1 ) 
        
        print('    setting point %i: %f' % (i,y_data/y_mc,))
        #ratio.Divide(data,prediction,"cl=0.683 b(1,1) mode")
        for n in range( nbins):
          #      print("Bin %i: err = %f" % (n, ratio.GetErrorYhigh(n) ))
                ratio.SetPoint( i, x_data, y_data/y_mc )
                ratio.SetPointError( i, bw/2, bw/2, dy_d/y_mc, dy_u/y_mc )
        
        i += 1
    return ratio


#########################################################

def SetStyle(corr, xtitle, ytitle, size=0.045, offset = 1.2):

    corr.GetYaxis().SetTitle(ytitle)
    corr.GetYaxis().SetTitleSize(size);
    corr.GetYaxis().SetTitleOffset(offset)

    corr.GetXaxis().SetTitle(xtitle)
    corr.GetXaxis().SetTitleSize(size);
    corr.GetXaxis().SetTitleOffset(offset)

#########################################################

def PrintBinContent2D(h2):
    print('Content of TH2 {}'.format(h2.GetName()))
    for i in range(1,h2.GetXaxis().GetNbins()+1):
        for j in range(1,h2.GetYaxis().GetNbins()+1):
            val = h2.GetBinContent(i,j)
            print('{} '.format(val), end='')
        print('')

#########################################################`
    
def PrintBinContent(histo):
    nx = histo.GetXaxis().GetNbins()
    line=''
    prefix = ''
    for binx in range(0,nx+2):
        line = '%s%s %4.1f' % (line, prefix, histo.GetBinContent(binx),)
        prefix=','
    print(line)

#########################################################

def next_tmp(xmin, xmax, title = 'tmp', ymin=0., ymax=1.1,):
    print(xmin, xmax)
    h = ROOT.TH2D("tmp%i" % (len(_h),), title, 100, xmin, xmax, 100, ymin, ymax) 
    h.SetStats(0)
    h.Draw()
    _h.append(h)
    return h

#########################################################
