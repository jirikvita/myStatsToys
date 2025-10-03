#!/usr/bin/python

import ROOT
import csv



stuff = []

# input: zubr
# /astroparticle/FAST/MachineLearning/

# Parameters
csv_file = "best_model_test_data.csv"

Xmax1, Xmax2 = 600, 1050
logE1, logE2 = 17, 21
nbinsE = 80
nbinsXmax = 70

h2_Xmax = ROOT.TH2D('Xmax',';true X_{max} [g/cm^{2}];predicted X_{max} [g/cm^{2}];,', nbinsXmax, Xmax1, Xmax2, nbinsXmax, Xmax1, Xmax2)
h2_logE = ROOT.TH2D('logE',';true log_{10}(E/eV);predicted log_{10}(E/eV);', nbinsE, logE1, logE2, nbinsE, logE1, logE2)

rmin = -0.2
rmax = -rmin
hres_Xmax = ROOT.TH2D('Xmax_res',';true X_{max} [g/cm^{2}];(predicted-true)/true;,', 100, Xmax1, Xmax2, 100, rmin, rmax)
rmin = -0.02
rmax = -rmin
hres_logE = ROOT.TH2D('logE_res',';true log_{10}(E/eV);(predicted-true)/true;', 100, logE1, logE2, 100, rmin, rmax) 


# Read CSV and fill histogram
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
            h2_logE.Fill(logE_true, logE_pred)
        except ValueError:
            continue  # skip bad rows

# Draw

h2s = { h2_Xmax : 'Xmax',
        h2_logE : 'logE'
       }

cans = []
ROOT.gStyle.SetPalette(1)

for h2,tag in h2s.items():
    canname = f'cmp_{tag}'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1200, 800)
    h2.SetStats(0)
    h2.Draw('colz')

    line = ROOT.TLine(h2.GetXaxis().GetXmin(), h2.GetYaxis().GetXmin(), h2.GetXaxis().GetXmax(), h2.GetYaxis().GetXmax())
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
    txt = ROOT.TLatex(0.12, 0.92, f'Pearson #rho={rho:1.3f}')
    txt.SetNDC()
    txt.Draw()


    # Make residuals graph (Profile vs diagonal)
    residuals = ROOT.TGraphErrors()
    residuals.SetName(f'gr_{tag}')
    ip = 0
    for i in range(1, prof.GetNbinsX() + 1):
        x_center = prof.GetBinCenter(i)
        y_mean   = prof.GetBinContent(i)
        if prof.GetBinEntries(i) > 0:  # only valid bins
            res = (y_mean - x_center) / x_center
            err = prof.GetBinError(i) / x_center
            # print(f'res: {res}')
            residuals.SetPoint(ip, x_center, res)
            residuals.SetPointError(ip, 0, err)
            ip += 1

    canname = f'residuals_{tag}'
    rcan = ROOT.TCanvas(canname, canname, 200, 200, 1200, 800)
    rcan.cd()
    rcan.SetLeftMargin(0.15)
    rcan.SetGridx(1)
    rcan.SetGridy(1)
    residuals.SetLineColor(ROOT.kBlack)
    residuals.SetMarkerSize(1)
    residuals.SetMarkerColor(ROOT.kBlack)
    residuals.SetMarkerStyle(20)

    if 'Xmax' in tag:
        hres_Xmax.SetStats(0)
        hres_Xmax.Draw()
    else:
        hres_logE.SetStats(0)
        hres_logE.Draw()

    
    line1 = ROOT.TLine(h2.GetXaxis().GetXmin(), 0., h2.GetXaxis().GetXmax(), 0.)
    line1.SetLineStyle(2)
    line1.SetLineWidth(4)
    line1.SetLineColor(ROOT.kMagenta)
    line1.Draw()

    residuals.Draw('P')


    stuff.append([can, rcan, prof, line, line1, txt, residuals])

    can.Update()
    rcan.Update()
    
    can.SaveAs(f'cmp_{tag}.png')
    rcan.SaveAs(f'res_{tag}.png')

    can.SaveAs(f'cmp_{tag}.pdf')
    rcan.SaveAs(f'res_{tag}.pdf')

    cans.append(can)


ROOT.gApplication.Run()
