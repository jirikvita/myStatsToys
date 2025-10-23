#!/usr/bin/python

# jk Oct 2025

import ROOT

import os, sys
import csv
from math import sqrt


##########################################
def adjustStats(h, x1 = 0.7, y1 = 0.7, x2 = 0.9, y2 = 0.9):
    ROOT.gPad.Update()
    st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    st.SetX1NDC(x1)
    st.SetY1NDC(y1)
    st.SetX2NDC(x2)
    st.SetY2NDC(y2)
    
##########################################
    
stuff = []

# input: zubr
# /astroparticle/FAST/MachineLearning/


##########################################
def main(argv):

    ROOT.gStyle.SetOptStat(1110)
    ROOT.gStyle.SetPadLeftMargin(0.17)
    ROOT.gStyle.SetPadRightMargin(0.17)
    #ROOT.gStyle.SetPalette(ROOT.kThermometer)
    ROOT.gStyle.SetPalette(ROOT.kLightTemperature)

    os.system('mkdir -p png pdf')

    if len(argv) < 2:
        print(f'Usage: {argv[0]} file.csv')
        return 1
    
    # Parameters
    csv_file = argv[1]

    Xmax1, Xmax2 = 600, 1050
    logE1, logE2 = 17, 21
    nbinsE = 80
    nbinsXmax = 70

    h2_Xmax = ROOT.TH2D('XmaxScatter',';true X_{max} [g/cm^{2}];predicted X_{max} [g/cm^{2}];', nbinsXmax, Xmax1, Xmax2, nbinsXmax, Xmax1, Xmax2)
    rmin = -0.2
    rmax = -rmin
    h2_XmaxBias = ROOT.TH2D('XmaxBias',';true X_{max} [g/cm^{2}];bias=(predicted-true)/true;', nbinsXmax, Xmax1, Xmax2, 100, rmin, rmax)
    h1_XmaxBias = ROOT.TH1D('XmaxBias1',';X_{max} bias=(predicted-true)/true;', 100, rmin, rmax)
    #h2_XmaxBiasWeighted = ROOT.TH2I('XmaxBiasWeighted',';true X_{max} [g/cm^{2}];bias=(predicted-true)/true;', nbinsXmax, 0, nbinsXmax, 50, rmin, rmax)
    h2_XmaxBiasWeighted = ROOT.TH2F('XmaxBiasWeighted',';true X_{max} [g/cm^{2}];bias=(predicted-true)/true;', nbinsXmax, Xmax1, Xmax2, 50, rmin, rmax)
    hres_Xmax = ROOT.TH2D('Xmax_res_helpOnly',';true X_{max} [g/cm^{2}];bias=(predicted-true)/true;', 100, Xmax1, Xmax2, 100, rmin, rmax)


    h2_logE = ROOT.TH2D('logEScatter',';true log_{10}(E/eV);predicted log_{10}(E/eV);', nbinsE, logE1, logE2, nbinsE, logE1, logE2)
    rmin = -0.03
    rmax = -rmin
    h2_logEBias = ROOT.TH2D('logEBias',';true log_{10}(E/eV);bias=(predicted-true)/true;', nbinsE, logE1, logE2, 100, rmin, rmax)
    h1_logEBias = ROOT.TH1D('logEBias1',';log_{10}(E/eV) bias=(predicted-true)/true;', 100, rmin, rmax)
    #h1_logEBiasWeighted = ROOT.TH2I('logEBiasWeighted',';true log_{10}(E/eV);bias=(predicted-true)/true;', nbinsE, 0, nbinsE, 50, rmin, rmax)
    h2_logEBiasWeighted = ROOT.TH2F('logEBiasWeighted',';true log_{10}(E/eV);bias=(predicted-true)/true;', nbinsE, logE1, logE2, 50, rmin, rmax)
    hres_logE = ROOT.TH2D('logE_res_helpOnly',';true log_{10}(E/eV);(predicted-true)/true;', 100, logE1, logE2, 100, rmin, rmax) 


    h2_XmaxVsLogE_true = ROOT.TH2D('XmaxVsLogE_true',';true log_{10}(E/eV);true X_{max} [g/cm^{2}];', nbinsE, logE1, logE2, nbinsXmax, Xmax1, Xmax2)
    h2_XmaxVsLogE_predicted = ROOT.TH2D('XmaxVsLogE_predicted',';predicted log_{10}(E/eV);predicted X_{max} [g/cm^{2}];', nbinsE, logE1, logE2, nbinsXmax, Xmax1, Xmax2)
    
    
    # Read CSV and fill histograms
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header if exists
        for row in reader:
            try:

                # evtID,pred_LogE,pred_Xmax,true_LogE,true_Xmax

                ievt = int(row[0])
                Xmax_true = float(row[4])
                Xmax_pred = float(row[2])
                logE_true = float(row[3])
                logE_pred = float(row[1])

                h2_Xmax.Fill(Xmax_true, Xmax_pred)
                h2_XmaxBias.Fill(Xmax_true, (Xmax_pred - Xmax_true) / Xmax_true)
                h1_XmaxBias.Fill( (Xmax_pred - Xmax_true) / Xmax_true)
                #h2_XmaxBiasWeighted.Fill( h2_Xmax.GetXaxis().FindBin(Xmax_true), (Xmax_pred - Xmax_true) / Xmax_true)
                h2_XmaxBiasWeighted.Fill( Xmax_true, (Xmax_pred - Xmax_true) / Xmax_true)

                h2_logE.Fill(logE_true, logE_pred)
                h2_logEBias.Fill(logE_true, (logE_pred - logE_true) / logE_true)
                h1_logEBias.Fill( (logE_pred - logE_true) / logE_true)
                #h2_logEBiasWeighted.Fill(h2_logE.GetXaxis().FindBin(logE_true), (logE_pred - logE_true) / logE_true)
                h2_logEBiasWeighted.Fill(logE_true, (logE_pred - logE_true) / logE_true)

                h2_XmaxVsLogE_predicted.Fill(logE_pred, Xmax_pred)
                h2_XmaxVsLogE_true.Fill(logE_true, Xmax_true)

            except ValueError:
                continue  # skip bad rows

    # Draw
    cans = []

    # ___________________________________________________________
    # draw the weighted TH2 biases as candles
    h2s = {
        h2_XmaxBiasWeighted : 'Xmax',
        h2_logEBiasWeighted : 'logE',
    }

    cw, ch = 1300, 1000

    for h2,tag in h2s.items():

        canname = f'bias_{tag}'
        bcan = ROOT.TCanvas(canname, canname, 400, 400, 1100, 1000)
        bcan.SetLeftMargin(0.15)
        bcan.SetRightMargin(0.10)

        bcan.cd()

        if 'Xmax' in tag:
            hres_Xmax.SetStats(0)
            hcp = hres_Xmax.DrawCopy()
            stuff.append(hcp)
        else:
            hres_logE.SetStats(0)
            hcp = hres_logE.DrawCopy()
            stuff.append(hcp)
        #print('Drawing candle plot...')
        h2.SetStats(0)
        h2.SetBarWidth(1.);
        h2.SetBarOffset(0.);
        h2.SetFillColor(ROOT.kGreen);
        h2.SetFillStyle(1001);
        h2.SetLineStyle(1);
        ROOT.TCandle.SetWhiskerRange(0.90)


        opt = 'candlex1'
        #opt = 'candle2'
        #opt = 'candleX(112111)'
        h2.Draw(opt) 
        #h2.Draw('violin') 

        x1, y1, x2, y2 = h2.GetXaxis().GetXmin(), 0., h2.GetXaxis().GetXmax(), 0.
        line = ROOT.TLine(x1, y1, x2, y2)
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        line.SetLineColor(ROOT.kBlack) # Magenta)
        line.Draw()
        #h2.Draw(opt + 'same') 

        stuff.append(line)

        bcan.Update()
        cans.append(bcan)


    # ___________________________________________________________
    # play with 2D, profiles, and biases
    h2s = { h2_Xmax : 'Xmax',
            h2_logE : 'logE',
            h2_XmaxBias : 'XmaxBias',
            h2_logEBias : 'logEBias',
            h2_XmaxVsLogE_true : 'XmaxVsLogE_true',
            h2_XmaxVsLogE_predicted : 'XmaxVsLogE_predicted'
           }

    for h2,tag in h2s.items():
        canname = f'cmp_{tag}'
        can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
        cans.append(can)
        h2.SetStats(0)
        h2.Draw('colz')

        x1, y1, x2, y2 = h2.GetXaxis().GetXmin(), h2.GetYaxis().GetXmin(), h2.GetXaxis().GetXmax(), h2.GetYaxis().GetXmax()
        if 'Bias' in tag:
            x1, y1, x2, y2 = h2.GetXaxis().GetXmin(), 0., h2.GetXaxis().GetXmax(), 0.

        line = None
        if not 'Vs' in tag:
            line = ROOT.TLine(x1, y1, x2, y2)
            line.SetLineStyle(2)
            line.SetLineWidth(4)
            line.SetLineColor(ROOT.kMagenta)
            line.Draw()

        prof = h2.ProfileX()
        prof.SetMarkerSize(1)
        prof.SetMarkerColor(ROOT.kBlack)
        prof.SetMarkerStyle(20)
        prof.SetLineColor(ROOT.kBlack)
        prof.Draw('same e1 x0')

        rho = h2.GetCorrelationFactor()
        txt = ROOT.TLatex(0.18, 0.92, f'Pearson #rho={rho:1.3f}')
        txt.SetTextSize(0.04)
        txt.SetNDC()
        txt.Draw()

        stuff.append([can, prof, rho, txt, line])

        canname = f'residuals_{tag}'
        rcan = ROOT.TCanvas(canname, canname, 200, 200, cw, ch)
        rcan.cd()
        rcan.SetLeftMargin(0.15)
        rcan.SetRightMargin(0.05)

        rcan.SetGridx(1)
        rcan.SetGridy(1)
        cans.append(rcan)

        if 'Xmax' in tag:
            hres_Xmax.SetStats(0)
            hcp = hres_Xmax.DrawCopy()
            stuff.append(hcp)
        else:
            hres_logE.SetStats(0)
            hcp = hres_logE.DrawCopy()
            stuff.append(hcp)

        if 'Bias' in tag:
            rcan.cd()
            prof.Draw('e1 same')

        else:
            # Make residuals graph (Profile vs diagonal)
            residuals = ROOT.TGraphErrors()
            residuals.SetName(f'gr_{tag}')
            ip = 0
            for i in range(1, prof.GetNbinsX() + 1):
                x_center = prof.GetBinCenter(i)
                y_mean   = prof.GetBinContent(i)
                N   = prof.GetBinEntries(i)
                if N > 0:  # only valid bins
                    res = (y_mean - x_center) / x_center
                    err = sqrt(N) * prof.GetBinError(i) / x_center
                    # print(f'res: {res}')
                    residuals.SetPoint(ip, x_center, res)
                    residuals.SetPointError(ip, 0, err)
                    ip += 1
            residuals.SetLineColor(ROOT.kBlack)
            residuals.SetMarkerSize(1)
            residuals.SetMarkerColor(ROOT.kBlack)
            residuals.SetMarkerStyle(20)

            residuals.Draw('P')
            stuff.append([residuals])


        line1 = ROOT.TLine(h2.GetXaxis().GetXmin(), 0., h2.GetXaxis().GetXmax(), 0.)
        line1.SetLineStyle(2)
        line1.SetLineWidth(4)
        line1.SetLineColor(ROOT.kMagenta)
        line1.Draw()

        stuff.append([line1, residuals])

    # ___________________________________________________________
    # integrated bias:
    canname = f'bias_integrated'
    can1 = ROOT.TCanvas(canname, canname, 0, 0, 1500, 600)
    can1.Divide(2,1)
    cans.append(can1)
    h1s = {
        h1_logEBias : ['logEbias', ROOT.kMagenta],
        h1_XmaxBias : ['Xmaxbias', ROOT.kCyan]
    }
    ih = 0
    for h1,opts in h1s.items():
        ih += 1
        h1.SetFillColor(opts[1])
        can1.cd(ih)
        ROOT.gPad.SetRightMargin(0.1)
        h1.Draw('hist')
        adjustStats(h1)
        ROOT.gPad.Update()


    # ___________________________________________________________
    # print PDFs
    for can in cans:
        can.Update()
        can.SaveAs(f'png/{can.GetName()}.png')
        can.SaveAs(f'pdf/{can.GetName()}.pdf')


    ROOT.gApplication.Run()



###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################
