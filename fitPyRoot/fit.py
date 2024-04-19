#!/snap/bin/pyroot

import ROOT

from ctypes import c_double

stuff = []

# Define your fitting function in Python
def gaussian(x, par):
    mean = par[0]
    sigma = par[1]
    #return (par[2] / (sigma * ROOT.TMath.Sqrt(2 * ROOT.TMath.Pi()))) * ROOT.TMath.Exp(-0.5 * ((x[0] - mean) / sigma)**2)
    #return par[2] * ROOT.TMath.Exp(-0.5 * ((x[0] - mean) / sigma)**2)
    return par[2] * ROOT.TMath.Exp(-0.5 * ((x[0] - mean) / sigma)**2)

# Create a histogram and fill it with data
hist = ROOT.TH1F("hist", "Example Histogram", 100, -5, 5)
N = 10000
for _ in range(N):
    hist.Fill(ROOT.gRandom.Gaus(0, 1))

# Define a fitting function in ROOT using TF1 and the Python function
fit_func = ROOT.TF1("fit_func", gaussian, -5, 5, 3)
fit_func.SetParameters(0., 1., N/3)  # Initial guess for mean and sigma

# Perform the fit
hist.Fit(fit_func)

# Draw histogram and fit
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
hist.Draw()
fit_func.Draw("same")

# Print fit results
print("Fit Results:")
print("Mean:", fit_func.GetParameter(0))
print("Sigma:", fit_func.GetParameter(1))

# Show the canvas
canvas.Draw()
canvas.Update()

stuff.append([fit_func, canvas, hist])

ROOT.gApplication.Run()
