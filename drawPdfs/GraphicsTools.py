#!/usr/bin/python

import ROOT


def SetColStyle(fun, col, style = 1, width = 1):
    fun.SetLineColor(col)
    fun.SetLineStyle(style)
    fun.SetLineWidth(width)
def SetMarkStyle(gr, col, style = 20, size = 1.):
    gr.SetMarkerColor(col)
    gr.SetLineColor(col)
    gr.SetMarkerStyle(style)
    gr.SetMarkerSize(size)

