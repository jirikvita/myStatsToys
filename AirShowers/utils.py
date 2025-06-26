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
def makeWhiteAxes(h2):
    h2.SetStats(0)
        
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
