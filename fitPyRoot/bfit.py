#!/snap/bin/pyroot

import ROOT

from math import fabs

stuff = []

######################################################################################
# Define your fitting function in Python
#  function written by Marie Princova, updated by JK; Feb 2024
def bifurcated_gaussian(x, params):
    mu = params[0]
    sigma1 = params[1]
    sigma2 = params[2]
    norm = params[3] / (sigma1 + sigma2) * ROOT.TMath.Sqrt(2 / ROOT.TMath.Pi())
    if x[0] < mu:
        return norm * ROOT.TMath.Exp(-0.5 * ((x[0] - mu) / sigma1) ** 2)
    else:
        return norm * ROOT.TMath.Exp(-0.5 * ((x[0] - mu) / sigma2) ** 2)

######################################################################################

N = 10000
# Define a fitting function in ROOT using TF1 and the Python function

x1, x2 = -5, 10
func = ROOT.TF1("bifgaus", bifurcated_gaussian, x1, x2, 4)
func.SetParameters(0., 1., 3., N/3)  # Initial guess for mean and sigma

# Create a histogram and fill it with data
hist = ROOT.TH1F("hist", "Example Histogram;X [unit];events", 100, x1, x2)

hist.FillRandom("bifgaus", N)

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


# Draw histogram and fit
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
canvas.cd()

# Perform the fit
hist.Fit(func, '0')

hist.Draw("e1 x0")
hist.SetMarkerColor(ROOT.kBlack)
hist.SetLineColor(ROOT.kBlack)
hist.SetMarkerStyle(20)
hist.SetMarkerSize(1.2)
func.Draw("same")

y1 = 0
y2 = 1.11*hist.GetMaximum()
line = ROOT.TLine(0., y1, 0., y2)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kBlue)
line.Draw()

# Print fit results
print("Fit Results:")
print("Mean:", func.GetParameter(0))
print("Sigma:", func.GetParameter(1))

# Show the canvas
canvas.Draw()
canvas.Update()

canvas.Print('BiFurkFit.png')
canvas.Print('BiFurkFit.pdf')

stuff.append([func, canvas, hist, line])

ROOT.gApplication.Run()

######################################################################################
######################################################################################
######################################################################################
