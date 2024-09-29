#!/usr/bin/env python3

# 2024 (c) code by Petr Hamal, modified by Jiri Kvita

# TODO:
# x,y map
# E, xmax map
# etc

import sys, os
import ROOT


# --- FAST detector position - in meters ---
fast_x = -18047.0
fast_y = -27415.0
fast_z = 0

cans = []

###########################################################
def plotHistos(hTraces, hs, h2s):
    
    c1 = ROOT.TCanvas("hTraces", "hTraces", 0, 0, 1200, 800)
    c1.Divide(2, 2)
    for i in range(4):
        c1.cd(i+1)
        hTraces[i].SetLineColor(i+1)
        hTraces[i].Draw("hist")

    c2 = ROOT.TCanvas("fast_simulation", "fast_simulation", 50, 50, 1200, 800)
    c2.Divide(3, 2)
    fcols = [ROOT.kYellow, ROOT.kGreen, ROOT.kGray, ROOT.kCyan, ROOT.kMagenta, ROOT.kTeal]
    for col,h in zip(fcols,hs):
        c2.cd(hs.index(h)+1)
        h.SetFillStyle(1111)
        h.SetFillColor(col)
        h.Draw()

    cn = 'heatmap'
    c3 = ROOT.TCanvas(cn, cn, 100, 100, 1000, 1000)
    c3.Divide(2,2)

    for h2 in h2s:
        c3.cd(h2s.index(h2)+1)
        h2.Draw('colz')

    return [c1, c2, c3]


###########################################################
###########################################################
###########################################################

def main(argv):

    ROOT.gSystem.Load("libFastEvent.so")

    gBatch = True

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    # zubr:
    #infname = "/astroparticle/FAST/Simulations/ntels_1_core_in_fov_auger/ntels_1_core_in_fov_auger.root"
    # JK:
    infname='/scratch/FAST/sim/ntels_1_core_in_fov_auger.root'

    infile = ROOT.TFile(infname, 'READ')
    tree = infile.Get('tree')

    event = ROOT.FASTEvent()
    tree.SetBranchAddress("event", event)

    nentries = tree.GetEntries()
    print(f"nentries: {nentries}")

    hAzimuth = ROOT.TH1D("azimuth", ";azimuth [deg]", 100, -200, 200)   
    hZenith = ROOT.TH1D("zenith", ";zenith [deg]", 100, 0, 100)   
    hEnergy = ROOT.TH1D("energy", ";log(E) [-]", 160, 17, 21)   
    hXmax = ROOT.TH1D("xmax", ";xmax [gcm-2]", 110, 200, 1300)
    hCorex = ROOT.TH1D("corex", ";core x [m]", 100, -30000, -5000)   
    hCorey = ROOT.TH1D("corey", ";core y [m]", 100, -30000, -5000)   

    hXmaxVsEnergy = ROOT.TH2D("XmaxVsEnergy", ";xmax [gcm-2];log(E) [-]", 80, 17, 21, 110, 50, 1300)

    
    hTraces = list()
    nb, t1, t2 =  500, 0., 5000.
    #nb, t1, t2 =  5000, 0., 5000.
    for i in range(4):
        hname = f"hTracePMT{i}"
        hTraces.append(ROOT.TH1D(hname, "", nb, t1, t2))

    # JK: create a heat map of the signals;)
    hn = 'h_heatmap'
    nbA, A1, A2 = 120, -2, 10.
    nb2 = 500
    h2 = ROOT.TH2D(hn, ';time bin;A', nb2, t1, t2/4, nbA, A1, A2)

    # particle type
    A = 1 # protons
    
    ###############
    # EVENT LOOP! #
    ###############
    breakN = 5000
    verb = 1000
    if breakN < 10000:
        verb = 100
    outfname = 'ascii.txt'
    outfile = open(outfname, 'w')
    for entry in range(nentries):
        if entry % verb == 0:
            print(f'Processing {entry} / {breakN} / {nentries}')

        if entry >= breakN: break
        
        tree.GetEntry(entry)
        # --- information about the setup of the simulation ---
        # --- the object structure follows the original C++ structure, see FASTEventIO in https://github.com/FASTCollaboration/FastFramework
        # zenith : 0 - 90 [deg]
        # azimuth : -180 - +180 [deg]
        # energy : [log(E)]
        # xmax : [gcm-2]
        # x0: [gcm-2]
        # core x,y,z : [m]
        simu = event.GetShowerSimData()

        zenith = simu.GetZenith()
        azimuth = simu.GetAzimuth()
        energy = simu.GetEnergy()
        xmax = simu.GetXmax()
        x0 = simu.GetXzero()
        _lambda = simu.GetLambda()
        corex = simu.GetCoreX()
        corey = simu.GetCoreY()
        corez = simu.GetCoreZ()
        # print(f"entry, energy, xmax, zenith, azimuth, x, y: {entry:7d} {energy:6.2f} {xmax:7.1f} {zenith:5.1f} {azimuth:6.1f} {corex:9.1f} {corey:9.1f}")

        # 1D
        hAzimuth.Fill(azimuth)
        hZenith.Fill(zenith)
        hEnergy.Fill(energy)
        hXmax.Fill(xmax)
        hCorex.Fill(corex)
        hCorey.Fill(corey)
        # 2D
        hXmaxVsEnergy.Fill(energy, xmax)
        
        # --- information from PMTs ---
        pixels = event.GetPixels()
        # print(f"entry, pixel size: {entry}, {len(pixels)}")
        outfile.write(f'#Evt={entry},A={A},logE={energy},Xmax={xmax},Azimuth={azimuth},Zenith={zenith},Corex={corex},Corey={corey}\n')
        for pixel in pixels:
            absid = pixel.GetAbsPixelId()
            telid = pixel.GetTelId()
            pixid = pixel.GetPixId()
            ped = pixel.GetPedestal()
            trace = pixel.GetTrace()
            #print(f"entry, absId, telId, pixId, trace.size, trace: {entry}, {absid}, {telid}, {pixid}, {len(trace)}, {trace[0:3]}")
            for i, tr in enumerate(trace):
                #if entry == 0:
                hTraces[pixid].Fill(i+1, tr)
                # for all events:
                # extraxt features:
                # t0, amplitude, area, skew = getFeatures()
                # fill to a structure or a class and save/dump to ascii?
                # heatmap
                h2.Fill(i+1, tr)
        # dump data to ascii
        # dump beginning of the trace
        for ipixel in range(0,len(pixels)):
            bin2 = hTraces[ipixel].GetXaxis().FindBin(1000.)
            #print(bin2)
            outfile.write(f'{ipixel}: ')
            for ibin in range(1, bin2):
                outfile.write('{:f}'.format(hTraces[ipixel].GetBinContent(ibin)))
                if ibin < bin2-1:
                    outfile.write(',')
            outfile.write('\n')
        # clear histos
        if entry != nentries-1 and  entry != breakN-1:
            for ipixel in range(0,len(pixels)):
                hTraces[ipixel].Reset()
    # event loop
    outfile.close()
    # PLOTTING            
    ROOT.gStyle.SetPalette(1)
    hs = [ hAzimuth, hZenith, hEnergy, hXmax, hCorex, hCorey ]
    h2s = [h2, hXmaxVsEnergy]
    cs = plotHistos(hTraces, hs, h2s)
    cans.extend(cs)
    for can in cans:
        can.Print(can.GetName() + '.png')
        can.Print(can.GetName() + '.pdf')

    if not gBatch:
        ROOT.gApplication.Run()

###########################################################
###########################################################
###########################################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)

###########################################################
###########################################################
###########################################################
