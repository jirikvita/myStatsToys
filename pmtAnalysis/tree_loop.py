#!/usr/bin/python

#/snap/bin/pyroot
# was: #!/usr/bin/python3
# jk Út 30. ledna 2024, 14:16:31 CET

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []

##########################################
def InitTrees(rfile, trs):
    trees = {trn : rfile.Get(trn) for trn in trs}
    return trees

##########################################
def ReadEntry(trs, i):
    for trn, tr in trs.items():
        tr.GetEntry(i)

##########################################
def main(argv):

    fname = "KM66024.root"
    rfile = ROOT.TFile(fname, 'read')

    treenames = [ 'singlephotons/pmtaf_tree'
                 ]
    refname = treenames[-1]

    print('Will analyze the following trees:')
    print(treenames)
    
    nbins = 50
    kenergy = "energy"
    ktime_over_threshold_ns = "time_over_threshold_ns"
    hbasenames = {  kenergy: [50, 250., 350., ROOT.kYellow], ktime_over_threshold_ns : [50, 0., 100., ROOT.kCyan] }
    histos = {}
    for treename in treenames:
        histos[treename] = {}
        for hbase,bins in hbasenames.items():
            hname = f'{treename}_{hbase}'
            htitle = hname + f';{hbase};events;'
            histos[treename][hbase] = ROOT.TH1D(hname, htitle, bins[0], bins[1], bins[2])
            histos[treename][hbase].SetFillColor(bins[3])
            histos[treename][hbase].SetFillStyle(1111)

    histos2d = {}
    print('Creating h2s...')
    for n1 in hbasenames:
        for n2 in hbasenames:
            if n1 == n2:
                continue
            print('vars: ',n1,n2)
            h2name = f'{n2}_vs_{n1}'
            print(h2name)
            htitle = h2name + f';{n1};{n2};'
            bins1 = hbasenames[n1]
            bins2 = hbasenames[n2]
            histos2d[h2name] = ROOT.TH2D(h2name, htitle, bins1[0], bins1[1], bins1[2], bins2[0], bins2[1], bins2[2])
            histos2d[h2name].SetStats(0)

    print(histos2d)
    trees = InitTrees(rfile, treenames)
    Nevt = trees[refname].GetEntries()
    # HACK!!!
    
    #Nevt = int (Nevt / 100.)
    for ievt in range(0,Nevt):
        if ievt % 10000 == 0: print(f'processing {ievt}/{Nevt}')
        ReadEntry(trees, ievt)
        for treename,tree in trees.items():
            histos[treename][kenergy].Fill(tree.energy)
            histos[treename][ktime_over_threshold_ns].Fill(tree.time_over_threshold_ns)
            #for h2 in histos2d:
            histos2d['energy_vs_time_over_threshold_ns'].Fill(tree.time_over_threshold_ns, tree.energy)
            histos2d['time_over_threshold_ns_vs_energy'].Fill(tree.energy, tree.time_over_threshold_ns)


    for treename in treenames:
        canname = f'canvas'
        print(f'Making canvas {canname}')
        can = ROOT.TCanvas(canname, canname)
        can.Divide(len(hbasenames),1)
        cans.append(can)
        i = 0
        for hbase,h in histos[treename].items():
            i = i + 1
            can.cd(i)
            h.Draw('hist')
            ROOT.gPad.Update()
        can.Update()


    canname = f'can2d'
    can2d = ROOT.TCanvas(canname, canname, 0, 0, 1200, 800)
    can2d.Divide(2,1)
    cans.append(can2d)
    #ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
    ic = 0
    for hn,h2 in histos2d.items():
        ic = ic+1
        can2d.cd(ic)
        h2.Draw('colz')
    
    for can in cans:
        try:
            can.Print(can.GetName() + '.png')
            can.Print(can.GetName() + '.pdf')
        except:
            print('Error')
        
    stuff.append(histos)
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

