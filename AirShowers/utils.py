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
