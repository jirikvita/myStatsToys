#!/usr/bin/python

import ROOT

##########################################
def makeDarkLegend(leg):
    #h2.SetStats(0)
        
    leg.SetTextColor(ROOT.kWhite)

##########################################
def makeWhiteAxes(h2):
    #h2.SetStats(0)
        
    h2.GetYaxis().SetAxisColor(ROOT.kWhite)
    h2.GetYaxis().SetLabelColor(ROOT.kWhite)
    h2.GetYaxis().SetTitleColor(ROOT.kWhite)

    h2.GetZaxis().SetAxisColor(ROOT.kWhite)
    h2.GetZaxis().SetLabelColor(ROOT.kWhite)
    h2.GetZaxis().SetTitleColor(ROOT.kWhite)


##########################################

def SetDarkStyle():
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
