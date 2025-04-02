#!/usr/bin/python

import ROOT

def makeGraph():
    gr = ROOT.TGraphErrors()
    gr.SetMarkerColor(ROOT.kBlack)
    gr.SetLineColor(gr.GetMarkerColor())
    gr.SetLineWidth(2)
    gr.SetLineStyle(1)
    gr.SetMarkerSize(1.)
    gr.SetMarkerStyle(20)
    return gr

