#!/usr/bin/env python3

# 2024 (c) code by Petr Hamal, modified by Jiri Kvita

import ROOT


# --- FAST detector position - in meters ---
fast_x = -18047.0
fast_y = -27415.0
fast_z = 0

# --- input file ---
# zubr:
#infname = "/astroparticle/FAST/Simulations/ntels_1_core_in_fov_auger/ntels_1_core_in_fov_auger.root"

# JK:
infname='/scratch/FAST/sim/ntels_1_core_in_fov_auger.root'


# ROOT.gROOT.SetBatch(True)

if __name__ == "__main__":
    ROOT.gSystem.Load("libFastEvent.so")
    
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

    hTraces = list()
    nb, t1, t2 =  5000, 0., 5000.
    for i in range(4):
        hname = f"hTracePMT{i}"
        hTraces.append(ROOT.TH1D(hname, "", nb, t1, t2))

    # JK: todo: create a heat map of the signals;)
    hn = 'h_heatmap'
    nbA, A1, A2 = 120, -2, 10.
    nb2 = 1000
    h2 = ROOT.TH2D(hn, ';bin;A', nb2, t1, t2, nbA, A1, A2)
        
    for entry in range(nentries):


        if entry % 1000 == 0:
            print(f'Processing {entry} / {nentries}')

        if entry >= 10000: break
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

        hAzimuth.Fill(azimuth)
        hZenith.Fill(zenith)
        hEnergy.Fill(energy)
        hXmax.Fill(xmax)
        hCorex.Fill(corex)
        hCorey.Fill(corey)



        # --- information from PMTs ---
        pixels = event.GetPixels()
        # print(f"entry, pixel size: {entry}, {len(pixels)}")

        for pixel in pixels:
            absid = pixel.GetAbsPixelId()
            telid = pixel.GetTelId()
            pixid = pixel.GetPixId()
            ped = pixel.GetPedestal()
            trace = pixel.GetTrace()
            #print(f"entry, absId, telId, pixId, trace.size, trace: {entry}, {absid}, {telid}, {pixid}, {len(trace)}, {trace[0:3]}")
            for i, tr in enumerate(trace):
                if entry == 0:
                    hTraces[pixid].Fill(i, tr)
                # for all events:
                # extraxt features:
                # t0, amplitude, area, skew = getFeatures()
                # fill to a structure or a class and save/dump to ascii?
                # heatmap
                h2.Fill(i, tr)
                
    ROOT.gStyle.SetPalette(1)
    c1 = ROOT.TCanvas("c1", "c1", 1200, 800)

    c1.Clear()
    c1.Divide(2, 2)
    for i in range(4):
        c1.cd(i+1)
        hTraces[i].SetLineColor(i+1)
        hTraces[i].Draw("hist")
    c1.Print("hTraces.png")

    c1.Clear()
    c1.Divide(3,2)
    c1.cd(1)
    hAzimuth.Draw()
    c1.cd(4)
    hZenith.Draw()
    c1.cd(2)
    hEnergy.Draw()
    c1.cd(5)
    hXmax.Draw()
    c1.cd(3)
    hCorex.Draw()
    c1.cd(6)
    hCorey.Draw()
    c1.Print("fast_simulation.png")

    c1.Close()

    cn = 'heatmap'
    c2 = ROOT.TCanvas(cn, cn, 100, 100, 1000, 800)
    c2.cd()
    h2.Draw('colz')

    ROOT.gApplication.Run()
