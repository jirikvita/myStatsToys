#!/usr/bin/python
# was: #!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Čt 31. října 2024, 11:43:44 CET

import ROOT
import os, sys, getopt

from NoiseTools import *

from numpy import random

# see $PYTHONPATH
from mystyle import *



##########################################
##########################################
##########################################

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

   
    SetDarkStyle()


    
    # random noise and multi gauss transient

    # number of time bins
    N = 500

    # mean of the constant noise baseline
    c = 0.

    # noise amplitude!
    A = 5.
    H1s = []

    Nh = 4
    maxA = 20
    canname = 'can_transient'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)
    can.Divide(2,2)
    cans.append(can)
    cols = [ROOT.kMagenta, ROOT.kCyan, ROOT.kYellow, ROOT.kGreen]
    

    # number of random events:
    nEvts = 10
    for ievt in range(0, nEvts):
        h1s = []
        for ih in range(0,Nh):
            # get the random constant histo
            h1 = getRandomHisto(f'h1_{ievt}_{ih}', ';time bin;Amplitude', N, 0, N, c, A)
            h1s.append(h1)
            #####################################
            # add some gaussians as signal:
            mus= [N/3]#, N/2, N]
            sigmas = [20]#, 30, 50]
            As = [maxA]#, 1.3, 0.5]
            for mu, sigma, a in zip(mus, sigmas, As):
                rand_mu = random.uniform(0, mu)
                rand_sigma = random.uniform(0, sigma)
                rand_a = random.uniform(0, a)
                addRandomGauss(h1, rand_mu, rand_sigma, rand_a)



        stuff.append(h1s)
        H1s.append(h1s)


     
        for i,h1 in enumerate(h1s):
            can.cd(i+1)
            h1.SetMaximum(maxA*1.2)
            h1.SetMinimum(-maxA*1.2)
            h1.SetStats(0)
            h1.SetLineColor(cols[i])
            h1.SetLineWidth(4)
            h1.Draw('hist')
            makeWhiteAxes(h1)


        for can in cans:
            can.Print(can.GetName() + f'_{ievt}.pdf')
            can.Print(can.GetName() + f'_{ievt}.png')
            ROOT.gPad.Update()

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

