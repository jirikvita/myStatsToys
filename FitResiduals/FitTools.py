#!/usr/bin/python

# jk 201X -- 2020; 2024

import ctypes

from math import sqrt, pow, log

import ROOT
from math import fabs
kEpsilon = 1.e-4

Ltex = []
_h = []

#########################################################
def CopyStyle(h1, h2, copyFillAtts = True):
    h2.SetLineColor(h1.GetLineColor())
    h2.SetLineStyle(h1.GetLineStyle())
    h2.SetMarkerColor(h1.GetMarkerColor())
    h2.SetMarkerSize(h1.GetMarkerSize())
    h2.SetMarkerStyle(h1.GetMarkerStyle())
    if copyFillAtts:
        h2.SetFillStyle(h1.GetMarkerStyle())
        h2.SetFillColor(h1.GetMarkerStyle())

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

def MakeVerticalLines(xs, y1, y2, col, ls = 2):
    lines = []
    for x in xs:
        line = ROOT.TLine(x, y1, x, y2)
        line.SetLineColor(col)
        line.SetLineStyle(ls)
        lines.append(line)
    return lines
#########################################################


#########################################################
#########################################################
#########################################################

def DrawHistFitResidualsSignif(h1, fun, can):
    #spad1,spad2,spad_inset = MakePadsStack(can, 'centre', 0.40, 0., 0., 0.)
    pads, inset = MakeMultiSubPads(can,  [0.60, 0.20, 0.20], 0.0,0.07, 0.4, 0.15)
    pads[0].cd()

    x1 = h1.GetXaxis().GetXmin()
    x2 = h1.GetXaxis().GetXmax()
    
    h1.Draw('e1 x0')

    h1.Fit(fun, '', '0')
    fun.Draw('same')
    chi2 = fun.GetChisquare()
    ndf = fun.GetNDF()
    ltex = ROOT.TLatex(0.14, 0.195, '#chi^{2}/n.d.f. = ' + '{:1.2f}/{:} = {:1.2f}'.format(chi2,ndf,chi2/ndf))
    ltex.SetNDC()
    ltex.SetTextColor(ROOT.kRed)
    ltex.SetTextSize(0.04)
    ltex.Draw()
    
    # 
    pads[1].cd()
    ratio = MakeFitRatioHisto(h1, fun, 'ratio')
    delta = 0.33
    y1 = 1. - delta
    y2 = 1. + delta
    ratio.SetMinimum(y1)
    ratio.SetMaximum(y2)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetTitle('Data / fit ')
    ratio.GetYaxis().SetTitleOffset(0.35)
    ratio.GetYaxis().SetTitleSize(0.12)

    ratio.Draw('e1x0')
    unitline = ROOT.TLine(x1, 1., x2, 1.)
    unitline.SetLineColor(ROOT.kRed)
    unitline.SetLineWidth(2)
    unitline.SetLineStyle(2)
    unitline.Draw() 
    upHelpHisto = ROOT.TH2D(h1.GetName() + '_upHelp', '',
                            h1.GetXaxis().GetNbins(), x1, x2,
                            100, y1, y2)
    
    sarrowsUp = DrawArrowForPointsOutsideYAxisRange(ratio, upHelpHisto, x1, x2)
    
    # significance

    pads[2].cd()
    sy1, sy2 = -3, 3
    signifh, ratioScaleHisto, pullh, signifLines = DrawFitSignificance(fun, h1, x1, x2, sy1, sy2)
    signifh.GetXaxis().SetTitleSize(0.12)
    signifh.GetYaxis().SetTitle('Data-fit signif.')
    signifh.GetYaxis().SetTitleOffset(0.35)
    signifh.GetYaxis().SetTitleSize(0.12)

    #signifh.GetYaxis().SetLabelSize(0.12)

    signifh.Draw("hist")
    for sline in signifLines:
        sline.Draw()

    # now go back to the upper histogram
    # and draw the histogram of fit residuals or pulls
    pads[0].cd()
    inset.Draw()
    inset.cd()
    # for debug
    #inset.SetFillColor(ROOT.kTeal)
    pullh.SetLineWidth(2)
    #pullh.SetStats(0)
    pullh.SetName('pull')
    pullh.GetXaxis().SetTitleSize(0.06)
    pullh.GetYaxis().SetTitleSize(0.06)
    pullh.GetXaxis().SetTitleOffset(0.64)
    pullh.GetYaxis().SetTitleOffset(0.64)
    pullh.Draw()
    ymin = pullh.GetMinimum()
    ymax = pullh.GetMaximum()
    vlines = MakeVerticalLines([-1,0,1], ymin*1.055, ymax*1.055, ROOT.kBlack)
    for vline in vlines:
        if vlines.index(vline) == 1:
            vline.SetLineStyle(1)
        vline.Draw()
    adjustStats(pullh)

    stuffDict = { 'pads' : pads,
                  'inset' : inset,
                  'ratio' : ratio,
                  'pullh' : pullh,
                  'signifh' : signifh,
                  'ratioScaleHisto' : ratioScaleHisto,
                  'pullh' : pullh,
                  'signifLines' : signifLines,
                  'vlines' : vlines,
                  'chi2tex' : ltex,
                  'unitline' : unitline,
                  'sarrowsUp' : sarrowsUp} 
    
    return stuffDict

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
def MakeFitRatioHisto( data, fit, newname = 'clone' ):
    ratio = data.Clone(newname)
    ratio.Reset()
    CopyStyle(data, ratio, False)
    nbins = data.GetNbinsX()
    #print 'nbins: %i' % (nbins,)
    i = 0
    for n in range( nbins ):
        y_data = ctypes.c_double()
        x_data = ctypes.c_double()
        y_err = ctypes.c_double()
        x_data = data.GetBinCenter( n+1 )
        y_data = data.GetBinContent( n+1 )
        y_err = data.GetBinError( n+1 )
        y_fit = fit.Eval(x_data)
        ratio.SetBinContent( n+1, y_data/y_fit )
        ratio.SetBinError( n+1, y_err / y_fit)
        
        i += 1
    ratio.Scale(1.)
    return ratio




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

def DrawFitSignificance(fit, hdata, hxmin, hxmax, yMin, yMax, iplot = 0, ratioTag = 'Signal signif.', adjust = True, drawopt = 'hist same X0', same = False):
            
        signifh = hdata.Clone(hdata.GetName() + '_signif{}'.format(iplot))
        signifh.Reset()
        pullh = ROOT.TH1D(hdata.GetName() + '_pull', ';fit pull;bins', 35, -3.5, 3.5)
        for i in range(1,hdata.GetXaxis().GetNbins()+1):
            hval = hdata.GetBinContent(i) - fit.Eval(hdata.GetBinCenter(i))
            herr = hdata.GetBinError(i)
            bgerr = 0.
            if bgerr + herr > 0:
                err = sqrt( pow(herr,2) + pow(bgerr,2) )
                signifh.SetBinContent(i, hval/err)
                pullh.Fill(hval/err)
                signifh.SetBinError(i, 0.)
            else:
                signifh.SetBinContent(i, 0.)
                signifh.SetBinError(i, 0.)            
                print('ERROR: in DivideByErrorBars of histo {} hbg error is {}!'.format(hdata.GetName(), bgerr))
        signifh.Scale(1.)
        #print('signifh:')
        #PrintBinContent(signifh)
        ratioScaleHisto = ROOT.TObject()
        if not same:        
            ratioScaleHisto = ROOT.TH2D(signifh.GetName() + '_tmp', signifh.GetName() + '_tmp' + ';;' + ratioTag,
                                        signifh.GetNbinsX(), signifh.GetXaxis().GetXmin(), signifh.GetXaxis().GetXmax(),
                                        100, yMin, yMax)
            ratioScaleHisto.SetStats(0)
            ratioScaleHisto.GetXaxis().SetTitle(MakePrettyTitle(signifh.GetXaxis().GetTitle()))
            if adjust:
                ratioScaleHisto.GetYaxis().SetTitleOffset(0.45)
                ratioScaleHisto.GetXaxis().SetLabelSize(0.085)
                ratioScaleHisto.GetYaxis().SetLabelSize(0.085)
                ratioScaleHisto.GetXaxis().SetTitleSize(0.15)
                ratioScaleHisto.GetYaxis().SetTitleSize(0.095)

            ratioScaleHisto.Draw()
            ratioScaleHisto.GetXaxis().SetRangeUser(hxmin, hxmax)

        line0 = ROOT.TLine(hxmin, 0., hxmax, 0.)
        line0.SetLineColor(ROOT.kBlack)
        #line0.Draw()
        line1p = ROOT.TLine(hxmin, 1., hxmax, 1.)
        line1p.SetLineColor(ROOT.kBlack)
        line1p.SetLineStyle(2)
        #line1p.Draw()
        line1n = ROOT.TLine(hxmin, -1., hxmax, -1.)
        line1n.SetLineColor(ROOT.kBlack)
        line1n.SetLineStyle(2)
        #line1n.Draw()

        signifh.SetFillColor(ROOT.kGreen+2)
        signifh.SetFillStyle(1111)
        signifh.GetXaxis().SetLabelSize(0.12)
        signifh.GetYaxis().SetLabelSize(0.12)
        #signifh.SetFillStyle(-1)

        
        signifh.Draw(drawopt)
        
        lines = [line0, line1p, line1n]
        
        return signifh, ratioScaleHisto, pullh, lines
