#!/usr/bin/python

import random
import ROOT

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
def adjustStats(h):
    ROOT.gPad.Update()
    st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    st.SetX1NDC(0.65)
    st.SetX2NDC(0.85)
    st.SetY1NDC(0.65)
    st.SetY2NDC(0.85)
    
