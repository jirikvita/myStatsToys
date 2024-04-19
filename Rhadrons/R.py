#!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Pá 19. dubna 2024, 15:47:53 CEST

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []

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
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.format(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.format(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.format(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.format(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    canname = 'rhadrons'
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)

    gr = ROOT.TGraph()
    
    infile = open('data_processed.txt', 'r')
    ip = -1
    for xline in infile.readlines():
        ip = ip + 2
        line = xline[:-1]
        E,R = float(line.split()[0]), float(line.split()[1])
        gr.SetPoint(ip, E, R)

    gr.SetMarkerColor(ROOT.kBlue)
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(0.5)
    gr.Draw('AP')
    gr.GetXaxis().SetTitle('E_{c.m.} [GeV]')
    gr.GetYaxis().SetTitle('R')
    gr.GetXaxis().SetMoreLogLabels()
    gr.GetXaxis().SetRangeUser(.2, 2e2)
    gr.GetYaxis().SetRangeUser(1e-2, 1e4)
    ROOT.gPad.SetLogy(1)
    ROOT.gPad.SetLogx(1)
    ROOT.gPad.SetGridx(1)
    ROOT.gPad.SetGridy(1)
    ROOT.gPad.Update()
    can.Print(can.GetName() + '.pdf')
    can.Print(can.GetName() + '.C')
    can.Print(can.GetName() + '.png')
    
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

