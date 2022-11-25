#!/snap/bin/pyroot
# Pá 25. listopadu 2022, 13:05:48 CET

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []



def PlotModel(canid = 0,
              m1 = 0., m2 = 3.,
              N = 1e5,
              alpha = 1.,
              M = 2.,
              Gamma = 0.3,
              Lambda = 3.1,
              edgew = 0.05,
              sig_f = 0.10,
              nb = 100):
    
    canname = 'BSM_illustration_{}'.format(canid)    
    dx,dy = 200, 200
    cw,ch = 800, 600
    can = ROOT.TCanvas(canname, canname, canid*dx, canid*dy, cw, ch)
    cans.append(can)
    
    hname = 'histo_h'
    
    bw = (m2 - m1) / nb
    h1 = ROOT.TH1D('hist_{}'.format(canid), ';m [TeV];events', nb, m1, m2)
   
    
    SM_fall = ROOT.TF1('fun_sm_{}'.format(canid), "[0]/[1]*exp(-x/[1])", m1, m2)
    SM_fall.SetParameters(N*(1-sig_f)*bw, alpha)
    BSM_sig = ROOT.TF1('bsm_fun_{}'.format(canid), "[0]/([2]*sqrt(2*TMath::Pi()))*exp(-(x-[1])^2/(2*[2]^2))", m1, m2)
    BSM_sig.SetParameters(N*sig_f*bw, M, Gamma)
    fun_total = ROOT.TF1('total_{}'.format(canid), "([0]/[1]*exp(-x/[1]) + [2]/([4]*sqrt(2*TMath::Pi()))*exp(-(x-[3])^2/(2*[4]^2))) * (1 - 1/(1+exp(-(x-[5])/[6])))", m1, m2)
    fun_total.SetParameters(N*(1-sig_f)*bw, alpha, N*sig_f*bw, M, Gamma, Lambda, edgew)

    if Lambda < m2:
        SM_fall.SetParameters(N*bw, alpha)
        fun_total.SetParameters(N*bw, alpha, N*sig_f*bw, M, Gamma, Lambda, edgew)
        h1.FillRandom('total_{}'.format(canid), int(N*1.1))  # need to compensate for the leak of sig below the cutoff
    else:
        h1.FillRandom('total_{}'.format(canid), int(N*1.0))

    
    h1.SetStats(0)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetMarkerStyle(20)
    h1.Draw('e1')

    npx = 500
    fun_total.SetLineColor(ROOT.kRed)
    fun_total.SetNpx(3*npx)
    fun_total.Draw('same')
    SM_fall.SetLineColor(ROOT.kBlack)
    #SM_fall.SetLineStyle(2)
    SM_fall.SetNpx(npx)
    SM_fall.Draw('same')
    BSM_sig.SetLineColor(ROOT.kBlue)
    #BSM_sig.SetLineStyle(2)
    BSM_sig.SetNpx(npx)
    BSM_sig.Draw('same')

    yy = h1.GetMaximum()
    line = ROOT.TLine(Lambda, 0., Lambda, yy)
    line.SetLineColor(ROOT.kMagenta)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    txt = ROOT.TLatex(Lambda - 0.22*(m2-m1), yy*1.03, 'Kinem. edge')
    txt.SetTextColor(ROOT.kMagenta)
    txt.SetTextSize(0.04)
    if Lambda < m2:
        line.Draw()
        txt.Draw()

    leg = ROOT.TLegend(0.30, 0.45, 0.55, 0.75)
    leg.AddEntry(h1, 'pseudo-data', 'P')
    leg.AddEntry(fun_total, 'total pdf', 'L')
    leg.AddEntry(SM_fall,   'SM pdf', 'L')
    leg.AddEntry(BSM_sig,   'BSM pdf', 'L')
    leg.SetBorderSize(0)
    leg.Draw()
    
    #ROOT.gPad.SetGridx(1)
    #ROOT.gPad.SetGridy(1)
    ROOT.gPad.Update()

    can.Print(canname + '.png')
    can.Print(canname + '.pdf')
    
    stuff.append([h1, fun_total, SM_fall, BSM_sig, line,txt,leg])
    


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
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.formatat(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.formatat(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.formatat(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.formatat(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))


    
    m1, m2 = 0., 14.
    dm = m2 - m1
    sig_fs = [0.40, 0.10, 0.10]
    canid = -1
    alphas = [0.5/3.*dm, 0.5/3.*dm, 0.5/3.*dm]
    Ms = [2.5/3.*dm, 2./3.*dm, 2./3.*dm]
    Gammas = [0.6/3.*dm, 0.3/3.*dm, 0.1/3.*dm]
    nbs = [42, 100, 100]
    Ns = [1e3, 1e3, 1e4]
    delta = 0.05
    Lambdas = [10./14.*m2, 0.883*m2, (1.-delta)*m2]
    edgew = 0.01/3.*dm  # width of the kinematic edge defind by the cutoff Lambda
    for M,Gamma,nb,N,alpha,Lambda,sig_f in zip(Ms, Gammas, nbs, Ns, alphas, Lambdas, sig_fs):
        canid = canid + 1   
        stuff.append ( PlotModel(canid, m1, m2, N, alpha, M, Gamma, Lambda, edgew, sig_f, nb) )


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

