#!/usr/bin/python

import random
import ROOT


from consts import *
from ctypes import c_double

##########################################
##########################################
##########################################
import ROOT
import math


##########################################
def makeGrRatio(gr, refgr, xtolerance):
    ratio = ROOT.TGraphErrors()
    ratio.SetLineStyle(gr.GetLineStyle())
    ratio.SetLineColor(gr.GetLineColor())
    ratio.SetLineWidth(gr.GetLineWidth())
    
    ratio.SetMarkerStyle(gr.GetMarkerStyle())
    ratio.SetMarkerColor(gr.GetMarkerColor())
    ratio.SetMarkerSize(gr.GetMarkerSize())
    
    xref = c_double(0.)
    yref = c_double(0.)
    x = c_double(0.)
    y = c_double(0.)

    i = 0
    iref = 0
    ip = 0
    N = gr.GetN()
    Nref = refgr.GetN()
            
    for j in range( max(N, Nref) ):
        gr.GetPoint(i, x, y)
        refgr.GetPoint(iref, xref, yref)
        while abs(x.value - xref.value) > xtolerance:
            if x.value < xref.value:
                i += 1
                gr.GetPoint(i, x, y)
            else:
                iref += 1
                refgr.GetPoint(iref, xref, yref)
            if i >= N:
                break
            if iref >= Nref:
                break


        if yref.value > 0:
            val = y.value / yref.value
            print(y.value, yref.value)
            err = gr.GetErrorY(i)
            errref = gr.GetErrorY(iref)
            rerr = 0.
            if err > 0:
                rerr += pow(err, 2)
            if errref > 0:
                rerr += pow(errref, 2)
            if rerr > 0:
                rerr = sqrt(rerr) / yref.value
            ratio.SetPoint(ip, x.value, val)
            ratio.SetPointError(ip, 0., rerr)
            ip += 1
        i += 1
        iref += 1
    return ratio

##########################################
def makeRatioGraphs(grs, refkey, xtolerance):
    print(grs)
    ratios = []
    for key,gr in grs.items():
        if key == refkey:
            continue
        ratio = makeGrRatio(gr, grs[refkey], xtolerance)
        ratios.append(ratio)
    return ratios


##########################################
def shiftX(gr, dx):
    x = c_double(0.)
    y = c_double(0.)
    for ip in range(gr.GetN()):
        gr.GetPoint(ip, x, y)
        gr.SetPoint(ip, x.value + dx, y.value)
    return

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

##########################################
# 10.7.2025
# custom quadratic * exp PDF for energy distribution of hadrons

def ymax_pdf(x0, lmb):
    return custom_pdf(xmax_pdf(x0, lmb), x0, lmb)

def xmax_pdf(x0, lmb):
    return lmb + x0/2. - math.sqrt( math.pow(lmb, 2) + math.pow(x0/2., 2))

def custom_pdf(x, x0, lmb):
    y = 1. / (  2*lmb**3*(1 - math.exp(-x0/lmb)) - lmb**2*x0*(1 + math.exp(-x0/lmb)) ) * x * (x - x0) * math.exp(-x/lmb)
    return y 

def sample_from_custom_pdf(x0, lmb, ymax):
    while True:
        x = random.uniform(0., x0)
        y = random.uniform(0., ymax)
        if y < custom_pdf(x, x0, lmb):
            return x

def sample_vonNeumann_pairProduction(x0 = 0, x1 = 1, ymax = 9./7.):
    while True:
        x = random.uniform(x0, x1)
        y = random.uniform(0., ymax)
        if y < (1 - 4./3.*x*(1. - x) ) * 9./7.:
            return x

def sample_vonNeumann_brehmsElEnergyFrac(x0 = 0, x1 = 1, ymax = 4./3.):
    while True:
        x = random.uniform(x0, x1)
        y = random.uniform(0., ymax)
        if y < (4./3. - 4./3.*(1-x) + (1-x)**2):
            return x
    
        
## Example: Generate 10 samples
#samples = [sample_from_custom_pdf() for _ in range(10)]
#print(samples)


##########################################
def makeHistoFromGraph(gr, tag):
    x, y = c_double(0), c_double(0)
    xs = []
    for ip in range(gr.GetN()):
        gr.GetPoint(ip, x, y)
        xs.append(1.*x.value)
    x1 = xs[0]
    x2 = xs[-1]
    n = len(xs)-1
    name = tag + ''
    title = ''
    h = ROOT.TH1D(name, title, n, x1, x2);
    for ip in range(gr.GetN()):
        gr.GetPoint(ip, x, y)
        yval = y.value
        if yval > 0:
            h.SetBinContent(ip+1, yval)
            ey = math.sqrt(yval)
            h.SetBinError(ip+1, ey)
    h.SetLineColor(gr.GetLineColor())
    #h.SetLineColor(gr.GetLineColor())
    h.Scale(1.)
    return h


##########################################
def makeHistosFromGraphs(grs, basetag):
    hs = []
    for igr,gr in enumerate(grs):
        h = makeHistoFromGraph(gr, basetag + f'_{igr}')
        hs.append(h)
    return hs

##########################################
def getGrMaxima(grs):
    maxy = -1
    x, y = c_double(0), c_double(0)
    for gr in grs:
        for ip in range(gr.GetN()):
            gr.GetPoint(ip, x, y)
            if y.value > maxy:
                maxy = 1.*y.value
    return maxy

##########################################
def getMaxima(hs):
    maxy = -1
    for h in hs:
        val = h.GetMaximum()
        if val > maxy:
            maxy = 1.*val
    return maxy


##########################################
def getConexShowerGraphs(tree, E):
    # Loop through entries in the tree
    print(f'Getting conex graphs for E={E}...')
    graphs = []
    for i, entry in enumerate(tree):
        x_array = entry.X  # Replace with your branch name
        y_array = entry.N  # Replace with your branch name

        # Assuming x_array and y_array are the same length
        n_points = len(x_array)

        # Create a TGraph for this event
        graph = ROOT.TGraph(n_points)

        for j in range(n_points):
            graph.SetPoint(j, x_array[j], y_array[j])

        graph.SetTitle(f"ConexShower {i} E={E}")
        graph.SetLineColorAlpha(ROOT.kCyan, 0.1)
        #graph.SetMarkerColorAlpha(ROOT.kRed, 0.1)
        #graph.SetMarkerSize(0.)
        #graph.SetMarkerStyle(20)
        graphs.append(graph)

    return graphs


##########################################
def getChi2(g1, g2):
    n1 = g1.GetN()
    n2 = g2.GetN()

    if n1 != n2:
        raise ValueError(f"Graphs have different number of points! {n1} vs {n2}")

    chi2 = 0.0
    ndf = 0

    for i in range(n1):
        x1 = c_double(0.)
        y1 = c_double(0.)
        x2 = c_double(0.)
        y2 = c_double(0.)

        g1.GetPoint(i, x1, y1)
        g2.GetPoint(i, x2, y2)

        if abs(x1.value - x2.value) > 1e-6:
            print(f"Warning: x-values differ at point {i}: {x1.value} vs {x2.value}")
            continue

        ey1 = g1.GetErrorY(i)
        ey2 = g2.GetErrorY(i)

        sigma2 = ey1**2 + ey2**2
        if sigma2 <= 0:
            continue  # skip this point

        chi2 += (y1.value - y2.value)**2 / sigma2
        ndf += 1

    if ndf == 0:
        raise ValueError("No valid points to compare")

    #chi2_ndf = chi2 / ndf
    #print(f"Chi2 / ndf = {chi2_ndf:.4f}")
    return chi2, ndf


##########################################
def makeGrStyle(gr, col = ROOT.kAzure-3):
    gr.SetMarkerColor(col)
    gr.SetMarkerSize(1.5)
    gr.SetMarkerStyle(20)
    gr.SetLineColor(gr.GetMarkerColor())
    gr.SetLineWidth(1)
    gr.SetLineStyle(1)


        
##########################################
def makeDarkAxes(h2):
    #h2.SetStats(0)
        
    h2.GetXaxis().SetAxisColor(ROOT.kBlack)
    h2.GetXaxis().SetLabelColor(ROOT.kBlack)
    h2.GetXaxis().SetTitleColor(ROOT.kBlack)

    h2.GetYaxis().SetAxisColor(ROOT.kBlack)
    h2.GetYaxis().SetLabelColor(ROOT.kBlack)
    h2.GetYaxis().SetTitleColor(ROOT.kBlack)

    h2.GetZaxis().SetAxisColor(ROOT.kBlack)
    h2.GetZaxis().SetLabelColor(ROOT.kBlack)
    h2.GetZaxis().SetTitleColor(ROOT.kBlack)

##########################################
def makeWhiteAxes(h2):

    try:
        h2.SetStats(0)
    except:
        pass
        
    h2.GetXaxis().SetAxisColor(ROOT.kWhite)
    h2.GetXaxis().SetLabelColor(ROOT.kWhite)
    h2.GetXaxis().SetTitleColor(ROOT.kWhite)

    h2.GetYaxis().SetAxisColor(ROOT.kWhite)
    h2.GetYaxis().SetLabelColor(ROOT.kWhite)
    h2.GetYaxis().SetTitleColor(ROOT.kWhite)

    h2.GetZaxis().SetAxisColor(ROOT.kWhite)
    h2.GetZaxis().SetLabelColor(ROOT.kWhite)
    h2.GetZaxis().SetTitleColor(ROOT.kWhite)


##########################################

def SetMyStyle():
    ROOT.gStyle.SetPalette(1)

    ROOT.gStyle.SetCanvasColor(ROOT.kBlack)
    ROOT.gStyle.SetPadColor(ROOT.kBlack)

    ROOT.gStyle.SetLegendFillColor(ROOT.kBlack)
    ROOT.gStyle.SetStatColor(ROOT.kBlack)
    ROOT.gStyle.SetStatTextColor(ROOT.kWhite)

    ROOT.gStyle.SetTitleTextColor(ROOT.kWhite)
    ROOT.gStyle.SetTitleColor(ROOT.kWhite)

    ROOT.gStyle.SetLabelColor(ROOT.kWhite)

    ROOT.gStyle.SetAxisColor(ROOT.kWhite)
    ROOT.gStyle.SetFrameLineColor(ROOT.kWhite)
    ROOT.gStyle.SetGridColor(ROOT.kWhite)

    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

##########################################
def getMaxGen(particles):
    maxg = -1
    for part in particles:
        if part.gen > maxg:
            maxg = 1.*part.gen
    return maxg
    
##########################################
def getMaxX(particles):
    jmax = -1
    maxx = -1.
    ipart = -1
    for part in particles:
        ipart = ipart + 1
        if part.x > maxx:
            jmax = 1*ipart
            maxx = 1.*part.x
    return jmax, maxx

##########################################
def getRndSign():
    if random.random() < 0.5:
        return 1
    else:
        return -1

##########################################
def chooseFrom(x, y):
    if random.random() < 0.5:
        return x
    else:
        return y
##########################################
def adjustStats(h):
    ROOT.gPad.Update()
    st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    st.SetX1NDC(0.65)
    st.SetX2NDC(0.85)
    st.SetY1NDC(0.65)
    st.SetY2NDC(0.85)


##########################################
def makePtctLabels(x,y,dy = 0.03, counts = {}, ny = 2, dx = 0.15):
    txts = []
    i = -1
    for lab in glabel:
        i = i+1
        count = ''
        try:
            count = f': {counts[lab]:,}'
        except:
            pass
        ddx = 1*dx
        #if i > 3:
        #    ddx = ddx*0.85
        txt = ROOT.TLatex(x + ((i) // 2)*ddx, y - ( (i) % 2)*dy, glabel[lab] + count)
        txt.SetTextColor(gcol[lab])
        #txt.SetTextSize(0.03)
        txt.SetNDC()
        txts.append(txt)
        txt.Draw()
    return txts

##########################################
##########################################
##########################################
