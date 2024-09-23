#!/usr/bin/python

# Út 17. září 2024, 08:54:12 CEST

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

    osobni = [77,
              77, 
              77,
              77,
              77,
              77,
              77,
              77,
              77,
              126.6,
              126.6,
              126.6,
              172,
              180.18,
              180.18,
              281.98,
              281.98,
              281.98,
              281.98,
              281.98,
              281.98]

    tags = ['Bc.', 'Mgr.', 'Ph.D.', 'Doc.', 'Prof.']
    tarif = [24, 27, 31, 41,	54.]

    gr = ROOT.TGraph()
    ip = 0
    for val in osobni:
        gr.SetPoint(ip, ip, val)
        ip = ip + 1
    lines = []

    x1,x2 = -1, len(osobni)+1
    h2 = ROOT.TH2D('tmp', ';mesic od I/2019;Mesicni osobni priplatek [kCZK]', 100, x1, x2, 100, 0, 500)
    h2.SetStats(0)

    cn = 'OsobniPriplatekRZ'
    can = ROOT.TCanvas(cn, cn, 0, 0, 1200, 800)
    h2.Draw()
    gr.SetMarkerColor(ROOT.kBlack)
    gr.SetLineColor(gr.GetMarkerColor())
    gr.SetLineWidth(2)
    gr.SetLineStyle(1)
    gr.SetMarkerSize(1.5)
    gr.SetMarkerStyle(29)
    gr.Draw('PL')

    lines = []
    cols = [ROOT.kBlack, ROOT.kGreen+2, ROOT.kBlue, ROOT.kMagenta, ROOT.kRed]
    leg = ROOT.TLegend(0.12, 0.50, 0.55, 0.88)
    leg.AddEntry(gr, 'Odebrany osobni priplatek elitniho chemika',  'PL')
    for col,tag,tar in zip(cols,tags,tarif):
        line = ROOT.TLine(x1, tar, x2, tar)
        line.SetLineColor(col)
        line.SetLineWidth(2)
        line.Draw()
        lines.append(line)
        leg.AddEntry(line, 'Tarif PrF ' + tag, 'L')
    leg.Draw()
    txt1 = ROOT.TLatex(0.02, 0.96, 'https://justice.cz/documents/d/krajsky-soud-v-ostrave/16co-120-2023')
    txt1.SetTextSize(0.03)
    txt2 = ROOT.TLatex(0.02, 0.93, 'https://www.dzurnal.cz/index.php/2023/04/24/nerovnosti-v-odmenovani-aneb-investice-do-excellence-podruhe/')
    txt2.SetTextSize(0.03)
    
    txt1.SetNDC()
    txt1.Draw()
    txt2.SetNDC()
    txt2.Draw()
    
    ROOT.gPad.Update()


    print(f'{sum(osobni[-6:-1])/5*12}')

    can.Print(can.GetName() + '.pdf')
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

